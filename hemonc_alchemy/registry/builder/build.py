
from pathlib import Path

import pandas as pd

from .read_dictionary import norm_cols
from ..heuristics import table_to_class, safe_identifier, parse_unique_key
from ..registry_model import TableMeta
from .enrich import enrich_registry
from .io import load_folder

CONTENT_COL = "Content Tables"
LOOKUP_COL = "Lookup and Metadata Tables"

MATURITY_COL = "Maturity"
N_FIELDS_COL = "No. of Fields"
DESC_COL = "Description"
UNIQUE_COL = "Unique Key"
IDENTITY_COL = "Identity Key"

def build_registry_from_dictionary(
    path: Path,
    data_dir: Path | None = None,
) -> dict[str, TableMeta]:
    """
    Build a registry from the HemOnc data dictionary.

    The dictionary supplies table and field intent. If ``data_dir`` is
    provided, the matching CSV extracts are also used to infer observed
    column types, enums, denormalised fields, keys, and normalisation groups.
    Without ``data_dir``, dictionary-declared field metadata is still loaded.
    """

    content_df = pd.read_excel(path, sheet_name="Content")
    lookup_df = pd.read_excel(path, sheet_name="Lookup")

    content_df = norm_cols(content_df)
    lookup_df = norm_cols(lookup_df)

    registry: dict[str, TableMeta] = {}

    sheets = {
        CONTENT_COL: ("content", content_df),
        LOOKUP_COL: ("lookup", lookup_df),
    }

    for table_col, (kind, df) in sheets.items():
        df = df.fillna("")

        for _, row in df.iterrows():
            raw_name = str(row.get(table_col, "")).strip()

            # skip headers / blanks
            if not raw_name or raw_name.lower().startswith(table_col.lower()):
                continue

            table_name = safe_identifier(raw_name)
            classname = table_to_class(table_name)

            maturity = str(row.get(MATURITY_COL, "")).strip() or "draft"
            description = str(row.get(DESC_COL, "")).strip()

            pk_columns = parse_unique_key(str(row.get(UNIQUE_COL, "")))

            identity_raw = str(row.get(IDENTITY_COL, "")).strip()
            identity_keys = parse_unique_key(identity_raw.replace(",", " + "))

            meta = TableMeta(
                name=table_name,
                classname=classname,
                kind=kind,                 # type: ignore[arg-type]
                maturity=maturity,         # type: ignore[arg-type]
                description=description,
                pk_columns=pk_columns,
                identity_keys=identity_keys,
                filename=f"{table_name}.csv",
                columns={},
                enums={},
                denormalised_columns=[],
                derived_columns=[],
                source_defined_keys=pk_columns.copy(),
                normalisation_groups=[],
            )

            registry[table_name] = meta

    dataframes = load_folder(data_dir) if data_dir is not None else None
    return enrich_registry(registry, dictionary_path=path, dataframes=dataframes)
