from __future__ import annotations

from pathlib import Path
import pandas as pd

from hemonc_alchemy.registry.registry_model.registry_types import (
    TableMeta,
    ColumnSpec,
    ColumnType,
    EnumInfo,
    NormalisationGroup,
)

from ..heuristics import (
    safe_identifier,
    detect_boolean,
    detect_datetime,
    detect_numeric,
    detect_enum,
    looks_denormalised_text,
    infer_pipe_groups,
)
from .read_dictionary import norm_cols, get_data_type

def _load_table_dictionary(name: str, xls: pd.ExcelFile) -> pd.DataFrame:
    sheet_name = next(
        (sheet for sheet in xls.sheet_names if safe_identifier(sheet) == safe_identifier(name)),
        None,
    )
    if sheet_name is not None:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.columns = [c.strip() for c in df.columns]
        return norm_cols(df)
    return pd.DataFrame()


def _dataframe_for_table(
    meta: TableMeta,
    dataframes: dict[str, pd.DataFrame],
) -> pd.DataFrame | None:
    """Find an observed frame despite punctuation or filename differences."""
    candidates = {meta.name, Path(meta.filename).stem}
    for name, frame in dataframes.items():
        if any(safe_identifier(name) == safe_identifier(candidate) for candidate in candidates):
            return frame
    return None

def is_reasonable_enum(values: list[str]) -> bool:
    if len(values) <= 1:
        return False
    if any(v.lower() in {"etc", "..."} for v in values):
        return False
    if any(len(v) > 60 for v in values):
        return False
    if any(v.lower().startswith(("if ", "when ", "where ")) for v in values):
        return False
    return True

def _should_normalise_as_lookup(
    meta: TableMeta,
    columns: list[str],
) -> bool:
    """
    Decide whether a denormalised group should become a lookup table.
    """

    # Conservative defaults
    if len(columns) != 1:
        return False

    col = columns[0]

    # Never normalise primary keys
    if col in meta.pk_columns:
        return False

    # Never normalise derived columns
    if col in (meta.derived_columns or []):
        return False

    # Never normalise free text
    spec = meta.columns.get(col) # type: ignore
    if spec and spec.dtype in {"Text"}:
        return False

    return True


def _enum_from_dictionary(row) -> EnumInfo | None:
    raw = str(row.get("Allowed Values/Format", ""))
    if ";" in raw and "any" not in raw.lower():
        values = [v.strip() for v in raw.split(";") if v.strip()]
        if values and is_reasonable_enum(values):
            return EnumInfo(values)
    return None


def _is_declared_multivalue(row) -> bool:
    return (
        "yes" in str(row.get("Multiple Values Allowed", "")).lower()
        or "pipe" in str(row.get("Allowed Values/Format", "")).lower()
        or "semicolon" in str(row.get("Allowed Values/Format", "")).lower()
    )

def _is_derived_column(col: str) -> bool:
    return any(
        key in col
        for key in ("valid", "count_", "total", "num_", "temp")
    )

def _can_be_enum(spec: ColumnSpec) -> bool:
    return spec.dtype != "Boolean"

def _infer_column_from_data(col: str, s: pd.Series) -> ColumnSpec:
    if detect_boolean(s):
        dtype: ColumnType = "Boolean"
    elif detect_datetime(s):
        dtype = "DateTime"
    elif (num := detect_numeric(s)) is not None:
        dtype = num  # type: ignore[assignment]
    else:
        max_len = s.dropna().astype(str).str.len().max() or 0
        dtype = "Text" if max_len > 255 else "String"

    return ColumnSpec(name=col, dtype=dtype)

def _enrich_table(
    meta: TableMeta,
    *,
    xls: pd.ExcelFile,
    df_data: pd.DataFrame | None,
) -> None:
    """
    Enrich a single TableMeta in place.
    """

    # Initialise containers
    columns: dict[str, ColumnSpec] = {}
    enums: dict[str, EnumInfo] = {}
    denorm: list[str] = []
    derived: list[str] = []
    source_keys = list(meta.pk_columns)

    df_dict = _load_table_dictionary(meta.name, xls)

    for _, row in df_dict.iterrows():
        raw = row.get("Variable")
        if not raw or str(raw).lower().startswith("note"):
            continue

        col = safe_identifier(str(raw)).lower()
        dtype = get_data_type(str(row.get("Type", "")))  # ColumnType

        spec = ColumnSpec(
            name=col,
            dtype=dtype,  # type: ignore[arg-type]
            primary_key=col in meta.pk_columns,
            derived=_is_derived_column(col),
        )

        # Dictionary enum declaration
        enum_info = _enum_from_dictionary(row)
        if enum_info and _can_be_enum(spec):
            spec.enum = enum_info
            enums[col] = enum_info
            spec.dtype = "Enum"  # type: ignore[assignment]

        columns[col] = spec

        # Multi-value declaration
        if _is_declared_multivalue(row):
            denorm.append(col)

        if spec.derived:
            derived.append(col)

    if df_data is not None:
        df_data = df_data.copy()

        # Unique keys from data
        for c in df_data.columns:
            if df_data[c].is_unique:
                source_keys.append(safe_identifier(c))

        for raw_col in df_data.columns:
            col = safe_identifier(raw_col).lower()

            if col in columns:
                spec = columns[col]
            else:
                spec = _infer_column_from_data(col, df_data[raw_col])
                columns[col] = spec

            # Enum inference
            if spec.enum is None:
                enum_info = detect_enum(col, df_data[raw_col])
                if enum_info:
                    spec.enum = EnumInfo(enum_info.values, enum_info.kind)
                    spec.dtype = "Enum"  # type: ignore[assignment]
                    enums[col] = spec.enum

            # Denormalisation inference
            if looks_denormalised_text(df_data[raw_col], col):
                denorm.append(col)

            if _is_derived_column(col):
                spec.derived = True
                derived.append(col)

        # Normalisation grouping
        groups = infer_pipe_groups(df_data, denorm)
        grouped_columns = {column for group in groups for column in group}
        groups.extend(
            [col]
            for col in sorted(set(denorm) - grouped_columns)
            if _should_normalise_as_lookup(meta, [col])
        )

        meta.normalisation_groups = [
            NormalisationGroup(columns=g, kind="lookup")
            for g in groups
            #if _should_normalise_as_lookup(meta, g)
        ]


    meta.columns = columns
    meta.enums = enums
    meta.denormalised_columns = sorted(set(denorm))
    meta.derived_columns = sorted(set(derived))
    meta.source_defined_keys = list(dict.fromkeys(source_keys))


def enrich_registry(
    registry: dict[str, TableMeta],
    *,
    dictionary_path: Path,
    dataframes: dict[str, pd.DataFrame] | None = None,
) -> dict[str, TableMeta]:
    """
    Phase 2: Enrich a Phase 1 registry using dictionary field metadata
    and observed CSV data.

    This step populates:
      - columns (ColumnSpec)
      - enums (EnumInfo)
      - denormalised columns
      - derived columns
      - source-defined keys
      - normalisation groups
    """

    xls = pd.ExcelFile(dictionary_path)

    for table_name, meta in registry.items():
        _enrich_table(
            meta,
            xls=xls,
            df_data=_dataframe_for_table(meta, dataframes) if dataframes else None,
        )

    return registry
