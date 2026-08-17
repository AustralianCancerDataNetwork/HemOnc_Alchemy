from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

TableKind = Literal["content", "lookup"]
Maturity = Literal["prod", "dev", "draft", "deprecated"]

ColumnType = Literal[
    "Integer",
    "Float",
    "Boolean",
    "DateTime",
    "String",
    "Text",
    "Enum",
]

EnumKind = Literal[
    "normal",        # ordinary categorical value
    "relationship",  # encodes a semantic relationship (e.g. "HasX")
]

NormalisationKind = Literal[
    "lookup",   # new lookup table generated
    "entity",   # references another entity table
]

@dataclass
class EnumInfo:
    """
    Description of an enum inferred or declared for a column.
    """
    values: list[str]
    kind: EnumKind = "normal"


@dataclass
class NormalisationGroup:
    """
    Describes a set of columns that represent a denormalised
    multi-valued concept and should be normalised.
    """
    columns: list[str]

    # How this group is normalised
    kind: NormalisationKind

    # Target entity name (for entity-based normalisation),
    # or None if a lookup table is generated
    target: Optional[str] = None


@dataclass
class ColumnSpec:
    """
    Fully resolved column description as it appears in the registry.
    """
    name: str
    dtype: ColumnType

    nullable: bool = True
    primary_key: bool = False

    enum: Optional[EnumInfo] = None
    derived: bool = False


@dataclass
class TableMeta:

    # identity
    name: str
    classname: str
    kind: TableKind
    maturity: Maturity
    description: str
    # keys
    pk_columns: list[str]
    identity_keys: list[str]

    # source artefacts
    filename: str

    # inferred / enriched
    columns: dict[str, ColumnSpec] | None = None
    enums: dict[str, EnumInfo] | None = None
    denormalised_columns: list[str] | None = None
    derived_columns: list[str] | None = None
    source_defined_keys: list[str] | None = None
    normalisation_groups: list[NormalisationGroup] | None = None