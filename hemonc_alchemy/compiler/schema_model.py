"""Registry metadata objects: TableMeta, ColumnSpec, EnumSpec, Registry.

Ported from hemonc_import/src/hemonc_import/registry_version/dataclasses.py
(956 lines — renamed here to avoid shadowing the stdlib `dataclasses`
module, which the original name did). This is the data model shared by
enrichment (infer.py-driven), rendering (generate.py), and validation
(audit.py, validate.py).

Three confirmed bugs fixed during the port (see hemonc_import's
_design/hemonc-import-audit.md and _design/refactor-followups.md):

- `ColumnSpec.sa_column_line` (source dataclasses.py:246): applied
  `default=-1` to every primary key regardless of column type. CONFIRMED
  already manifested in checked-in hemonc_import output — String primary
  keys on HemoncClasses, HemoncRels, Exclusions, SigBranchTypes, Units all
  got an int default. Fixed by branching on the Python type, the same way
  sa_create.py (now deleted, US-11) already did correctly: `-1` for int
  PKs, `''` for string PKs, no default otherwise.
- `ColumnSpec.sa_python_type` vs `sa_column_line` (source dataclasses.py:208
  vs :245): the Python type hint's `Optional[...]` and the SQL `nullable=`
  flag were computed from two different values (raw `self.nullable` vs. a
  PK-adjusted local variable). CONFIRMED manifested:
  `Mapped[Optional[str]] = mapped_column(..., nullable=False, ...)`. Both
  are now derived from one `effective_nullable` computation.
- `EnumSpec.tablename` (source dataclasses.py:435, in
  `enrich_field_metadata`): set to the *column* name instead of the table
  name, corrupting registry metadata (didn't affect generated code, which
  uses the `table` argument passed to `enum_type`/`enum_class` directly,
  but corrupted anything reading `EnumSpec.tablename` itself, e.g. registry
  previews). Fixed to use the table's own name.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field, is_dataclass
from html import escape
from pathlib import Path
from typing import Any, Literal, Protocol, runtime_checkable

import pandas as pd

from .infer import (
    detect_boolean,
    detect_datetime,
    detect_enum,
    detect_numeric,
    infer_pipe_groups,
    looks_denormalised_text,
    max_string_length,
    safe_enum_key,
    safe_identifier,
)
from .load_helpers import get_data_type, norm_cols

ColumnType = str
TableKind = Literal["lookup", "content"]
Maturity = Literal["dev", "prod", "prod-"]

# Tokens that mean "not yet assigned" on an identifier column specifically.
# Deliberately scoped to `_cui`-suffixed columns only (see
# `_clean_identifier_placeholders`) -- the same words are genuine
# categorical values elsewhere, e.g. Authors_Site_typeEnum has a real "TBD"
# member, so this must not become a blanket na_values addition.
_IDENTIFIER_PLACEHOLDER_TOKENS = {"tba", "tbd", "pending"}


def _clean_identifier_placeholders(series: pd.Series, col_name: str) -> pd.Series:
    """For `_cui`-suffixed identifier columns, treat known "not yet
    assigned" placeholder tokens as missing when inferring type/nullability
    (US-18). CONFIRMED against real data: `variant_eligibility.variant_cui`
    contains a literal "TBA" value alongside otherwise-clean integer IDs,
    which is why it was the one `_cui` mismatch `detect_numeric`'s
    float64-with-NaN fix didn't already resolve -- "TBA" prevents the
    column from parsing as numeric at all, so it never reaches that fix.

    Nulling the placeholder alone isn't enough: pandas keeps the column at
    object/string dtype (a single non-numeric token is enough to block
    numeric dtype inference for the whole column), and `detect_numeric`
    inspects dtype, not values. So also attempt numeric coercion here --
    but only adopt it if every remaining (non-placeholder) value actually
    converts; a `_cui` column that's genuinely alphanumeric throughout
    falls back to staying textual rather than being forced into silently
    dropping real data as NaN.
    """
    if not col_name.endswith("_cui"):
        return series
    is_placeholder = series.astype(str).str.strip().str.lower().isin(_IDENTIFIER_PLACEHOLDER_TOKENS)
    cleaned = series.where(~is_placeholder)
    coerced = pd.to_numeric(cleaned, errors="coerce")
    if coerced.notna().sum() >= cleaned.notna().sum():
        return coerced
    return cleaned


def dataclass_to_dict(obj: Any) -> Any:
    """Recursively convert nested dataclass structures into JSON-safe values."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: dataclass_to_dict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(v) for v in obj]
    else:
        return obj


def registry_to_json(registry: Registry) -> str:
    """Serialise a `Registry` into a stable, pretty-printed JSON string.

    Interim schema representation until schema/hemonc.linkml.yaml is
    authored (US-14, pending the slot-scoping prototype — see
    _design/hemonc-alchemy-spec.md open questions). compiler/diff.py
    operates on this JSON for now.
    """
    return json.dumps(dataclass_to_dict(registry), indent=2, sort_keys=True)


def save_registry_json(registry: Registry, path: Path) -> None:
    """Write a registry snapshot to disk."""
    path.write_text(registry_to_json(registry), encoding="utf-8")


def load_registry_json(path: Path) -> Registry:
    """Load a registry snapshot previously written by `save_registry_json`."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return Registry.from_dict(raw)


def sa_import_block() -> str:
    """Return the import block used at the top of generated SQLAlchemy models.

    Explicit, not `from .entity_base import *` (the original's approach,
    and exactly the leaky-namespace pattern US-1 fixes -- a consumer doing
    `from hemonc_alchemy.model.entities import *` would otherwise inherit
    whatever `entity_base`/`base` happened to import, e.g. `os`, `re`,
    `Path`). Every name the generated column/relationship lines actually
    reference must be listed here explicitly instead.

    entities.py is generated directly into hemonc_alchemy/model/, alongside
    base.py and enums.py -- these are sibling-module imports (single dot),
    not `..model.x` (which would also resolve correctly here but is
    needlessly roundabout for a same-package import).
    """
    return (
        "from __future__ import annotations\n\n"
        "from datetime import datetime\n"
        "from typing import Optional\n\n"
        "import sqlalchemy as sa\n"
        "from sqlalchemy import (\n"
        "    BigInteger,\n"
        "    Boolean,\n"
        "    DateTime,\n"
        "    Enum,\n"
        "    Float,\n"
        "    ForeignKey,\n"
        "    ForeignKeyConstraint,\n"
        "    String,\n"
        "    Text,\n"
        ")\n"
        "from sqlalchemy.orm import Mapped, foreign, mapped_column\nfrom sqlalchemy.orm import relationship as sa_relationship\n\n"
        "from .base import Base, EntityBase\n"
    )


def enum_import_block() -> str:
    """Return the import block used at the top of generated enum classes."""
    return "from enum import Enum\n"


@runtime_checkable
class HtmlRenderable(Protocol):
    """Protocol for metadata objects that provide notebook HTML rendering."""

    def _repr_html_(self) -> str: ...


def render_html(obj: object) -> str:
    """Render registry metadata objects in notebooks, with a safe fallback."""
    if isinstance(obj, HtmlRenderable):
        return obj._repr_html_()
    return f"<pre>{escape(repr(obj))}</pre>"


@dataclass
class EnumSpec:
    """Describes an inferred or declared enum attached to a table column."""

    name: str
    tablename: str
    values: list[str]

    def __repr__(self) -> str:
        return f"EnumSpec(name={self.name!r}, tablename={self.tablename!r}, n_values={len(self.values)})"

    @classmethod
    def from_dict(cls, raw: dict) -> EnumSpec:
        return cls(**raw)

    def _repr_html_(self) -> str:
        preview = ", ".join(f"<code>{escape(v)}</code>" for v in self.values[:8])
        more = f" <i>(+{len(self.values) - 8} more)</i>" if len(self.values) > 8 else ""
        enum_cls = f"{escape(self.tablename)}_{safe_identifier(self.name).capitalize()}Enum"
        return (
            f'<div style="border:1px solid #ddd; padding:6px; margin:4px 0; background:#fafafa">'
            f"<b>Enum:</b> <code>{escape(self.name)}</code> "
            f"<small>({len(self.values)} values)</small><br/>"
            f"<b>Type:</b> <code>{enum_cls}</code><br/>"
            f"<b>Values:</b> {preview}{more}"
            f"</div>"
        )

    def enum_type(self, table: TableMeta) -> str:
        return f"{table.classname}_{safe_identifier(self.name).capitalize()}Enum"

    def enum_class(self, table: TableMeta) -> str:
        values = [v.strip().lower() for v in self.values]
        value_map = {safe_enum_key(v): v for v in dict.fromkeys(values)}

        enum_name = self.enum_type(table)
        lines = [f"class {enum_name}(str, Enum):"]
        for key, val in value_map.items():
            lines.append(f"    {key} = '{val}'")
        return "\n".join(lines)


@dataclass
class ColumnSpec:
    """Represents the inferred SQLAlchemy-facing shape of a single column."""

    name: str
    type: ColumnType
    nullable: bool = True
    length: int | None = None
    enum: str | None = None

    def __repr__(self) -> str:
        extras: list[str] = []
        if not self.nullable:
            extras.append("nullable=False")
        if self.length is not None:
            extras.append(f"length={self.length}")
        if self.enum is not None:
            extras.append(f"enum={self.enum!r}")
        extra_str = ", " + ", ".join(extras) if extras else ""
        return f"ColumnSpec(name={self.name!r}, type={self.type!r}{extra_str})"

    @classmethod
    def from_dict(cls, raw: dict) -> ColumnSpec:
        return cls(**raw)

    def _repr_html_(self) -> str:
        flags: list[str] = ["NULL" if self.nullable else "<b style='color:#b00'>NOT NULL</b>"]
        if self.length:
            flags.append(f"len={self.length}")
        if self.enum:
            flags.append(f"enum=<code>{escape(self.enum)}</code>")
        return (
            f"<tr><td><code>{escape(self.name)}</code></td>"
            f"<td>{escape(self.type)}</td><td>{' | '.join(flags)}</td></tr>"
        )

    def python_type(self) -> str:
        t = self.type.lower()
        if t == "boolean":
            return "bool"
        if t == "datetime":
            return "datetime"
        if t.startswith("string") or t == "text":
            return "str"
        if t.startswith("int"):
            return "int"
        if t.startswith(("float", "double", "decimal")):
            return "float"
        if t == "enum":
            return self.enum or "Enum"
        return "Any"

    def is_primary_key(self, table: TableMeta) -> bool:
        """Whether this column is the (natural) primary key on the generated
        class — i.e. declared as PK *and* the table isn't using a surrogate
        `id` PK instead. Shared by sa_python_type/sa_column_line so both
        derive nullability from the same fact (the bug this fixes)."""
        is_natural_pk = self.name in table.pk_columns
        use_surrogate = table.use_surrogate_pk and table.kind == "content"
        return is_natural_pk and not use_surrogate

    def effective_nullable(self, table: TableMeta) -> bool:
        """Nullability actually enforced on the generated column: never
        nullable if this column is the primary key, regardless of what was
        inferred from the data snapshot."""
        return self.nullable and not self.is_primary_key(table)

    def sa_python_type(self, table: TableMeta, *, force_not_null: bool = False) -> str:
        """`force_not_null` overrides `effective_nullable`'s parent-relative PK
        check: needed when rendering a denormalised column onto its own
        generated map/child table (see `normalised_table_class`), where the
        column is always part of *that* table's composite primary key
        regardless of whether it's a natural key column on `table` (the
        parent). CONFIRMED via compiler/spec_adapter.py's PrimaryKeyValidator
        integration to matter: every map table's value column was rendered
        `Optional[...]`/nullable, an inherently inconsistent
        `primary_key=True, nullable=True` declaration on every single one.
        """
        t = self.type.lower()
        if t == "boolean":
            base = "bool"
        elif t == "datetime":
            base = "datetime"
        elif t.startswith("string") or t == "text":
            base = "str"
        elif t.startswith("int"):
            base = "int"
        elif t.startswith("float"):
            base = "float"
        elif t == "enum":
            base = f"{table.classname}_{safe_identifier(self.name).capitalize()}Enum"
        else:
            base = "Any"
        nullable = False if force_not_null else self.effective_nullable(table)
        return f"Optional[{base}]" if nullable else base

    def sa_column_type(self, table: TableMeta) -> str:
        t = self.type.lower()

        if t == "boolean":
            return "Boolean"
        if t == "datetime":
            return "DateTime"
        if t.startswith("int"):
            return "BigInteger"
        if t.startswith(("float", "double", "decimal")):
            return "Float"
        if t.startswith("string"):
            if self.length:
                return f"String({self.length})"
            return "String(255)"
        if t == "text":
            return "Text"
        if t == "enum":
            enum_cls = f"{table.classname}_{safe_identifier(self.name).capitalize()}Enum"
            return f"Enum({enum_cls})"
        return "String(255)"

    def sa_column_line(self, table: TableMeta) -> str:
        py_type = self.sa_python_type(table)
        sa_type = self.sa_column_type(table)

        is_pk = self.is_primary_key(table)
        nullable = self.effective_nullable(table)

        pk_str = ", primary_key=True" if is_pk else ""
        nullable_str = f", nullable={nullable!s}"

        default_str = ""
        if is_pk:
            base_py_type = self.python_type()
            if base_py_type == "int":
                default_str = ", default=-1"
            elif base_py_type == "str":
                default_str = ", default=''"

        return (
            f"    {self.name}: Mapped[{py_type}] = mapped_column("
            f"{sa_type}{pk_str}{nullable_str}{default_str})"
        )


@dataclass
class NormalisationGroup:
    """Groups denormalised columns that should be exploded together."""

    columns: list[str]

    def __repr__(self) -> str:
        return f"NormalisationGroup(columns={self.columns})"

    def _repr_html_(self) -> str:
        cols = ", ".join(f"<code>{escape(c)}</code>" for c in self.columns)
        return f"<li>{cols}</li>"

    @classmethod
    def from_dict(cls, raw: dict) -> NormalisationGroup:
        return cls(columns=list(raw["columns"]))


@dataclass
class NormalisedTable:
    """Metadata for an exploded child table derived from a denormalised column."""

    parent: str
    column: str

    @property
    def name(self) -> str:
        return f"{self.parent}_{self.column}"

    @property
    def classname(self) -> str:
        return f"{self.parent}_{safe_identifier(self.column).capitalize()}Map"

    @classmethod
    def from_dict(cls, raw: dict) -> NormalisedTable:
        return cls(parent=raw["parent"], column=raw["column"])


@dataclass
class ForeignLikeRef:
    """A view-only relationship inferred from a shared business-identifying column."""

    local_column: str
    target_table: str
    target_column: str


@dataclass
class SoftManyToManyRef:
    """A view-only many-to-many relationship through a generated normalised map table."""

    local_table: str
    map_table: str
    map_column: str
    target_table: str
    target_column: str


@dataclass
class TableMeta:
    """All metadata required to generate and load one logical table.

    `pk_columns` carries the declared business/natural key from the
    workbook. `source_defined_keys` and `identity_keys` are used as
    relationship targets when inferring proxy-style links between generated
    ORM classes.
    """

    name: str
    description: str
    kind: TableKind
    maturity: Maturity

    pk_columns: list[str]

    columns: dict[str, ColumnSpec] = field(default_factory=dict)

    source_defined_keys: list[str] = field(default_factory=list)
    identity_keys: list[str] = field(default_factory=list)

    enums: dict[str, EnumSpec] = field(default_factory=dict)

    denormalised_columns: list[str] = field(default_factory=list)
    derived_columns: list[str] = field(default_factory=list)
    normalisation_groups: list[NormalisationGroup] = field(default_factory=list)

    normalised_tables: list[NormalisedTable] = field(default_factory=list)
    soft_relationships: list[ForeignLikeRef] = field(default_factory=list)
    soft_m2m_relationships: list[SoftManyToManyRef] = field(default_factory=list)
    use_surrogate_pk: bool = True

    # Set by Registry.finalise_table_metadata_from_data once the real source
    # file is located (may differ from f"{name}.csv" — see infer.py's
    # resolve_source_csv and this module's docstring, US-13).
    source_filename: str | None = None

    @property
    def has_surrogate_pk(self) -> bool:
        return self.kind == "content"

    @property
    def classname(self) -> str:
        return "".join(part.capitalize() for part in self.name.split("_"))

    @property
    def relationship_target_keys(self) -> list[str]:
        return list(dict.fromkeys([*self.source_defined_keys, *self.identity_keys]))

    @property
    def filename(self) -> str:
        """Fallback naive filename — overridden by `source_filename` once
        Registry.finalise_table_metadata_from_data resolves the real file
        via infer.py's resolve_source_csv (US-13 fix)."""
        return self.source_filename or f"{self.name}.csv"

    @classmethod
    def from_dict(cls, raw: dict) -> TableMeta:
        return cls(
            name=raw["name"],
            description=raw["description"],
            kind=raw["kind"],
            maturity=raw["maturity"],
            pk_columns=list(raw["pk_columns"]),
            columns={k: ColumnSpec.from_dict(v) for k, v in raw["columns"].items()},
            source_defined_keys=list(raw.get("source_defined_keys", [])),
            identity_keys=list(raw.get("identity_keys", [])),
            enums={k: EnumSpec.from_dict(v) for k, v in raw.get("enums", {}).items()},
            denormalised_columns=list(raw.get("denormalised_columns", [])),
            derived_columns=list(raw.get("derived_columns", [])),
            normalisation_groups=[
                NormalisationGroup.from_dict(g) for g in raw.get("normalisation_groups", [])
            ],
            normalised_tables=[
                NormalisedTable.from_dict(nt) for nt in raw.get("normalised_tables", [])
            ],
            source_filename=raw.get("source_filename"),
        )

    @staticmethod
    def _relationship_name(base: str, target_table: str, counts: Counter, suffix: str) -> str:
        if counts[base] > 1:
            return f"{base}_{target_table}_{suffix}"
        return f"{base}_{suffix}"

    def _map_primary_join(self, map_table: str) -> str:
        if self.use_surrogate_pk and self.kind == "content":
            return f"{self.classname}.id == {map_table}.c.parent_id"

        pk_conds = [f"{self.classname}.{pk} == {map_table}.c.{pk}" for pk in self.pk_columns]
        if len(pk_conds) == 1:
            return pk_conds[0]
        return f"and_({', '.join(pk_conds)})"

    def enrich_field_metadata(self, df_dict: pd.DataFrame) -> None:
        df_dict = norm_cols(df_dict)

        for _, row in df_dict.iterrows():
            val = row["Variable"] if "Variable" in row and pd.notna(row["Variable"]) else ""
            r = str(val).strip()

            if not r or r.lower().startswith("note:") or r.lower().startswith("note "):
                continue

            col_name = safe_identifier(r).lower()
            type_str = get_data_type(str(row.get("Type", "")))
            multival = str(row.get("Multiple Values Allowed", "")).lower()
            allowed_fmt = str(row.get("Allowed Values/Format", "")).strip().lower()

            if col_name not in self.columns:
                self.columns[col_name] = ColumnSpec(name=col_name, type=type_str, nullable=True)

            enum_values: list[str] = []
            if "enum" in type_str.lower():
                raw = str(row.get("Allowed Values/Format", ""))
                if ";" in raw and "Any" not in raw:
                    enum_values = [v.strip() for v in raw.split(";") if v.strip()]

            if enum_values:
                # Fix: tablename is this table's own name, not the column
                # name (source dataclasses.py:435 bug).
                self.enums[col_name] = EnumSpec(name=col_name, tablename=self.name, values=enum_values)
                self.columns[col_name].type = "Enum"

            is_multi = "yes" in multival.lower() or "pipe" in allowed_fmt or "semicolon" in allowed_fmt

            if is_multi and "html" not in col_name and col_name not in self.pk_columns and "alldays" not in col_name:
                self.denormalised_columns.append(col_name)

            if "valid" in col_name or "count_" in col_name or "total" in col_name or "num_" in col_name:
                self.derived_columns.append(col_name)

    def finalise_from_data(self, df_data: pd.DataFrame | None) -> None:
        """
        Introspect real data to finalise:
        - column types
        - inferred enums
        - denormalised columns
        - derived columns
        - source-defined keys
        - normalisation groups
        """
        if df_data is None or df_data.empty:
            return

        df_data = norm_cols(df_data)

        for col in df_data.columns:
            safe_col = safe_identifier(col).lower()
            s = df_data[col]
            s_typed = _clean_identifier_placeholders(s, safe_col)

            if detect_boolean(s_typed):
                inferred_type = "Boolean"
            elif detect_datetime(s_typed):
                inferred_type = "DateTime"
            elif (num := detect_numeric(s_typed)) is not None:
                inferred_type = num
            else:
                mn = max_string_length(s_typed)
                inferred_type = "Text" if mn > 255 else f"String({mn})"

            is_nullable = bool(s_typed.isna().any())

            if safe_col not in self.columns:
                self.columns[safe_col] = ColumnSpec(name=safe_col, type=inferred_type, nullable=is_nullable)
            else:
                self.columns[safe_col].type = inferred_type
                self.columns[safe_col].nullable = is_nullable

            enum_inferred = detect_enum(safe_col, s)
            if enum_inferred is not None:
                self.enums[safe_col] = EnumSpec(
                    name=safe_col,
                    tablename=self.name,
                    values=list(enum_inferred.values),
                )
                self.columns[safe_col].type = "Enum"
                self.columns[safe_col].enum = safe_col

            if (
                looks_denormalised_text(s)
                and safe_col not in self.pk_columns
                and safe_col not in self.source_defined_keys
                and "html" not in safe_col
                and "alldays" not in safe_col
            ):
                self.denormalised_columns.append(safe_col)

            if s.is_unique and safe_col not in self.source_defined_keys:
                self.source_defined_keys.append(safe_col)

        groups = infer_pipe_groups(df_data, self.denormalised_columns)

        flattened_multi = {c for g in groups if len(g) > 1 for c in g}
        final_groups = [g for g in groups if not (len(g) == 1 and g[0] in flattened_multi)]

        self.normalisation_groups = [NormalisationGroup(columns=g) for g in final_groups]

        self.denormalised_columns = sorted(set(self.denormalised_columns))
        self.derived_columns = sorted(set(self.derived_columns))
        self.source_defined_keys = list(dict.fromkeys(self.source_defined_keys))

        self.normalised_tables = [
            NormalisedTable(parent=self.name, column=c) for c in self.denormalised_columns
        ]

    def normalised_table_class(self, nt: NormalisedTable) -> str:
        """Render the SQLAlchemy class for one generated exploded child table."""
        parent = self
        class_name = nt.classname
        table_name = nt.name

        lines: list[str] = [f"class {class_name}(EntityBase, Base):", f"    __tablename__ = '{table_name}'", ""]

        if parent.use_surrogate_pk and parent.kind == "content":
            lines.append(
                f"    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('{parent.name}.id'), primary_key=True)"
            )
        else:
            for pk in parent.pk_columns:
                col = parent.columns[pk]
                py_type = col.sa_python_type(parent)
                sa_type = col.sa_column_type(parent)
                lines.append(f"    {pk}: Mapped[{py_type}] = mapped_column({sa_type}, primary_key=True)")

            fk_cols = ", ".join(f"'{pk}'" for pk in parent.pk_columns)
            ref_cols = ", ".join(f"'{parent.name}.{pk}'" for pk in parent.pk_columns)

            lines.append("")
            lines.append("    __table_args__ = (")
            lines.append(f"        ForeignKeyConstraint([{fk_cols}], [{ref_cols}]),")
            lines.append("    )")

        col_name = nt.column
        col_spec = parent.columns[col_name]

        # force_not_null=True: this column is always part of *this* map
        # table's own composite primary key (parent_id + value), regardless
        # of whether it happens to also be a natural key on the parent --
        # see sa_python_type's docstring for the confirmed bug this fixes.
        py_type = col_spec.sa_python_type(parent, force_not_null=True)
        sa_type = col_spec.sa_column_type(parent)

        lines.append(f"    {col_name}: Mapped[{py_type}] = mapped_column({sa_type}, primary_key=True, nullable=False)")
        lines.append("")
        lines.append(f"    parent: Mapped['{parent.classname}'] = sa_relationship(back_populates='{nt.column}_items')")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"TableMeta(name={self.name!r}, kind={self.kind!r}, maturity={self.maturity!r}, "
            f"pk={self.pk_columns}, n_columns={len(self.columns)}, n_enums={len(self.enums)}, "
            f"n_norm_groups={len(self.normalisation_groups)})"
        )

    def _repr_html_(self) -> str:
        col_rows = "".join(render_html(c) for c in self.columns.values())
        enum_blocks = "".join(render_html(e) for e in self.enums.values())
        norm_groups = "".join(render_html(g) for g in self.normalisation_groups)

        return f"""
        <div style="border:2px solid #ccc; padding:10px; margin:12px 0; border-radius:6px">
            <h3 style="margin-top:0"><code>{escape(self.name)}</code>
                <small style="color:#666">({self.kind}, {self.maturity})</small></h3>
            <p style="margin:4px 0 8px 0"><i>{escape(self.description)}</i></p>
            <p><b>Primary key:</b> {", ".join(f"<code>{escape(pk)}</code>" for pk in self.pk_columns)}</p>
            <p><b>Denormalised cols:</b> {", ".join(f"<code>{escape(col)}</code>" for col in self.denormalised_columns)}</p>
            <details open><summary><b>Columns ({len(self.columns)})</b></summary>
                <table border="1" cellpadding="4" cellspacing="0" style="margin-top:6px">
                    <thead><tr><th>Name</th><th>Type</th><th>Flags</th></tr></thead>
                    <tbody>{col_rows}</tbody>
                </table>
            </details>
            <details><summary><b>Enums ({len(self.enums)})</b></summary>{enum_blocks or "<i>None</i>"}</details>
            <details><summary><b>Normalisation Groups ({len(self.normalisation_groups)})</b></summary>
                <ul>{norm_groups or "<li><i>None</i></li>"}</ul>
            </details>
            <details><summary><b>Keys</b></summary>
                <p><b>Source-defined:</b> {", ".join(map(escape, self.source_defined_keys)) or "<i>None</i>"}</p>
                <p><b>Identity:</b> {", ".join(map(escape, self.identity_keys)) or "<i>None</i>"}</p>
            </details>
        </div>
        """

    def table_class(self, registry: Registry) -> str:
        """Render the main SQLAlchemy class for this table.

        The generated class includes:
        - file/load metadata
        - the natural-key `UniqueConstraint`
        - exploded denormalised child relationships
        - view-only proxy relationships inferred from business-rule keys
        """
        lines: list[str] = []

        if len(self.columns) == 0:
            return ""

        class_name = self.classname

        lines.append(f"class {class_name}(EntityBase, Base):")
        lines.append(f"    __tablename__ = '{self.name}'")
        if self.use_surrogate_pk and self.kind == "content":
            lines.append("    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)")
            lines.append("")
        lines.append(f"    filename = '{self.filename}'")
        if self.use_surrogate_pk and self.kind == "content":
            lines.append("    pk_columns = ['id']")
        else:
            lines.append(f"    pk_columns = {self.pk_columns!r}")
        lines.append(f"    source_defined_keys = {self.source_defined_keys!r}")
        lines.append(f"    identity_keys = {self.identity_keys!r}")
        lines.append(f"    denormalised_columns = {self.denormalised_columns!r}")
        lines.append(f"    derived_columns = {self.derived_columns!r}")
        lines.append("")

        if self.enums:
            lines.append("    enum_lookup = {")
            for col, enum in self.enums.items():
                enum_cls = enum.enum_type(self)
                lines.append(f"        '{col}': {enum_cls},")
            lines.append("    }")
        else:
            lines.append("    enum_lookup = {}")

        lines.append("")

        if self.use_surrogate_pk and self.kind == "content" and self.pk_columns:
            uniq_cols = ", ".join(f"'{c}'" for c in self.pk_columns)
            lines.append("    __table_args__ = (")
            lines.append(f"        sa.UniqueConstraint({uniq_cols}, name='uq_{self.name}_natural_key'),")
            lines.append("    )")
            lines.append("")

        for col in sorted(self.columns.values(), key=lambda c: c.name):
            if col.name in self.denormalised_columns or col.name in self.derived_columns:
                continue
            lines.append(col.sa_column_line(self))

        lines.append("")
        lines.append("    normalisation_groups = [")
        for g in self.normalisation_groups:
            lines.append(f"        {list(g.columns)!r},")
        lines.append("    ]")
        for nt in self.normalised_tables:
            rel_name = f"{nt.column}_items"
            child_cls = nt.classname
            lines.append(
                f"    {rel_name}: Mapped[list['{child_cls}']] = sa_relationship("
                f"back_populates='parent', lazy='selectin', cascade='all, delete-orphan')"
            )

        soft_rel_counts = Counter(rel.local_column for rel in self.soft_relationships)
        for rel in self.soft_relationships:
            target_cls = registry.tables[rel.target_table].classname
            rel_name = self._relationship_name(rel.local_column, rel.target_table, soft_rel_counts, "obj")
            join_expr = f"{self.classname}.{rel.local_column} == foreign({target_cls}.{rel.target_column})"

            lines.append(f"    {rel_name}: Mapped[Optional['{target_cls}']] = sa_relationship(")
            lines.append(f"        '{target_cls}',")
            lines.append(f'        primaryjoin="{join_expr}",')
            lines.append("        lazy='selectin',")
            lines.append("        viewonly=True,")
            lines.append("    )")
            lines.append("")

        soft_m2m_counts = Counter(rel.map_column for rel in self.soft_m2m_relationships)
        for rel in self.soft_m2m_relationships:
            target_cls = registry.tables[rel.target_table].classname
            map_table = rel.map_table
            col = rel.map_column

            rel_name = self._relationship_name(col, rel.target_table, soft_m2m_counts, "objects")

            primary_join = self._map_primary_join(map_table)
            secondary_join = f"{target_cls}.{rel.target_column} == {map_table}.c.{col}"

            lines.append(f"    {rel_name}: Mapped[list['{target_cls}']] = sa_relationship(")
            lines.append(f"        '{target_cls}',")
            lines.append(f"        secondary='{map_table}',")
            lines.append(f'        primaryjoin="{primary_join}",')
            lines.append(f'        secondaryjoin="{secondary_join}",')
            lines.append("        lazy='selectin',")
            lines.append("        viewonly=True,")
            lines.append("    )")
            lines.append("")

        return "\n".join(lines)


@dataclass
class Registry:
    """Container for all table metadata plus generation/inference helpers."""

    tables: dict[str, TableMeta]

    @classmethod
    def from_dict(cls, raw: dict) -> Registry:
        return cls(tables={name: TableMeta.from_dict(meta) for name, meta in raw["tables"].items()})

    def get(self, name: str) -> TableMeta:
        return self.tables[name]

    def content_tables(self) -> list[TableMeta]:
        return [t for t in self.tables.values() if t.kind == "content"]

    def lookup_tables(self) -> list[TableMeta]:
        return [t for t in self.tables.values() if t.kind == "lookup"]

    def __repr__(self) -> str:
        n_content = sum(1 for t in self.tables.values() if t.kind == "content")
        n_lookup = sum(1 for t in self.tables.values() if t.kind == "lookup")
        return f"Registry(n_tables={len(self.tables)}, content={n_content}, lookup={n_lookup})"

    def _repr_html_(self) -> str:
        tables_html = "".join(render_html(t) for t in self.tables.values())
        n_content = sum(1 for t in self.tables.values() if t.kind == "content")
        n_lookup = sum(1 for t in self.tables.values() if t.kind == "lookup")
        return (
            f'<div style="font-family:sans-serif"><h2>Registry</h2>'
            f"<p><b>Total tables:</b> {len(self.tables)} | <b>Content:</b> {n_content} | "
            f"<b>Lookup:</b> {n_lookup}</p>{tables_html}</div>"
        )

    def enrich_table_metadata(self, dictionary_path: str | Path) -> None:
        """
        Enrich table metadata from table-specific dictionary sheets.

        This step fills in declared field-level semantics such as types,
        enum values, and whether a column appears to be denormalised.
        """
        xls = pd.ExcelFile(dictionary_path)

        for table_name, meta in self.tables.items():
            if table_name in xls.sheet_names:
                df_dict = pd.read_excel(xls, sheet_name=table_name)
                df_dict.columns = [str(c).strip() for c in df_dict.columns]
                df_dict = norm_cols(df_dict)
                meta.enrich_field_metadata(df_dict)
            else:
                # Kept as a warning, not an error -- schema often evolves
                # faster than dictionaries.
                print(f"Warning: no dictionary sheet for table '{table_name}'")

    def finalise_table_metadata_from_data(self, data_dir: str | Path) -> None:
        """
        Finalise metadata by introspecting the current CSV extracts.

        This is where inferred runtime details such as concrete SQL types,
        unique single-column candidates, and normalisation groups are
        derived from the live data.

        Uses infer.py's `resolve_source_csv` to find the real backing file
        even when it doesn't match the naive `f"{name}.csv"` convention
        (US-13 fix) -- the original used a direct path-exists check here,
        which is why 4 tables with real, available data were silently
        skipped.
        """
        from .infer import (
            resolve_source_csv,  # local import: avoids a cycle at module load
        )

        data_dir = Path(data_dir)

        for table_name, meta in self.tables.items():
            data_path, ambiguous = resolve_source_csv(data_dir, table_name)

            if ambiguous:
                print(f"Warning: ambiguous CSV matches for table '{table_name}': {', '.join(ambiguous)}")
                continue

            if data_path is None:
                print(f"Warning: no data file for table '{table_name}'")
                continue

            meta.source_filename = data_path.name

            df_data = pd.read_csv(data_path)
            df_data = norm_cols(df_data)

            meta.finalise_from_data(df_data)

    def render_enum_classes(self) -> tuple[str, str]:
        """Render enum class code plus the matching import block."""
        f = enum_import_block() + "\n\n"
        enum_labels: list[str] = []
        for table in self.tables.values():
            for enum in table.enums.values():
                f += enum.enum_class(table) + "\n\n"
                enum_labels.append(enum.enum_type(table))
        import_lines = ",\n    ".join(sorted(enum_labels))
        return f, f"from .enums import (\n    {import_lines},\n)" if enum_labels else "# no enums generated"

    def render_sa_models(self) -> tuple[str, str]:
        """Render the ORM model module and companion enum module content."""
        self.infer_soft_relationships()
        enum_classes, enum_import = self.render_enum_classes()
        f = f"{sa_import_block()}\n\n{enum_import}\n\n"
        for table in self.tables.values():
            f += f"{table.table_class(self)}\n\n"
            for nt in table.normalised_tables:
                f += table.normalised_table_class(nt) + "\n\n"

        return f, enum_classes

    def infer_soft_relationships(self) -> None:
        """Infer view-only business-key relationships across the registry.

        Two families are created:
        - direct soft relationships where a column matches another table's
          source-defined key
        - many-to-many proxy relationships where a generated normalised
          child table stores values matching another table's
          source-defined or identity key
        """
        unique_index: dict[tuple[str, str], str] = {}
        relationship_index: dict[tuple[str, str], str] = {}

        for t in self.tables.values():
            t.soft_relationships = []
            t.soft_m2m_relationships = []

            for key in t.source_defined_keys:
                unique_index[(t.name, key)] = t.name
            for key in t.relationship_target_keys:
                relationship_index[(t.name, key)] = t.name

        for table in self.tables.values():
            for col in table.columns:
                for (target_table, target_key) in unique_index:
                    if col == target_key and table.name != target_table:
                        table.soft_relationships.append(
                            ForeignLikeRef(local_column=col, target_table=target_table, target_column=target_key)
                        )

        for table in self.tables.values():
            for nt in table.normalised_tables:
                col = nt.column
                map_table = nt.name

                for (target_table, target_key) in relationship_index:
                    if col == target_key and table.name != target_table:
                        table.soft_m2m_relationships.append(
                            SoftManyToManyRef(
                                local_table=table.name,
                                map_table=map_table,
                                map_column=col,
                                target_table=target_table,
                                target_column=target_key,
                            )
                        )
