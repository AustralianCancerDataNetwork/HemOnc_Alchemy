"""
Base class for all hemonc-alchemy entity tables.

Mirrors ``omop_alchemy.cdm.base.CDMTableBase``: the same orm-loader
interfaces provide chunked, staged CSV loading (merge strategies, not
insert-only), and serialisation, for free (US-19, US-20). Verified to
compose cleanly against orm-loader>=1.0.0 — see
_design/hemonc-alchemy-spec.md TS-6 step 4.

What this class does NOT provide, because orm-loader is deliberately
domain-agnostic and has no equivalent (US-19's "what stays custom"):

- Pipe-delimited denormalisation / explode handling (a HemOnc sig/regimen
  row can expand into N child rows), and natural-key-based FK resolution
  at load time for surrogate-PK tables. Both built in
  `toolbox/loading.py` (`load_denormalised`), verified end-to-end against
  real HemOnc data on both SQLite and Postgres.

Type casting itself is NOT re-implemented here -- reuses
`orm_loader.loaders.data.converters.perform_cast`/`cast_scalar` directly
(US-20), which already tracks per-column cast failures via
`TableCastingStats` instead of hemonc_import's old `-1`/`-1.0`
sentinel-on-failure behaviour. Enum-from-CSV casting (US-22) is the one
type `perform_cast`'s built-in `CastRule`s never handled at all (`sa.Enum`
is itself a subclass of `sa.String`, so a bad value used to pass straight
through as a plain string rather than being caught) -- `register_enum_casts`
below closes that gap via `orm_loader`'s `register_column_cast_rule`
(https://github.com/AustralianCancerDataNetwork/orm-loader/issues/36),
still without reimplementing any casting logic itself.
"""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from types import ModuleType
from typing import Any

import sqlalchemy as sa
import sqlalchemy.orm as so
from orm_loader.tables import CSVLoadableTableInterface, SerialisableTableInterface


class Base(so.DeclarativeBase):
    pass


class EntityBase(Base, CSVLoadableTableInterface, SerialisableTableInterface):
    """Abstract base for every generated HemOnc entity class."""

    __abstract__ = True


def register_enum_casts() -> None:
    """Register a validating cast rule for every generated `sa.Enum` column,
    across every table (including generated map/denormalised tables --
    several of those have `sa.Enum` value columns too, e.g.
    `indications_biomarker2.biomarker2`).

    Fully generic: `col.type.python_type` already gives the exact right
    Python `Enum` class per column, so this needs no per-table or
    per-column list to keep in sync -- after any `regen`, whatever enum
    columns exist just get picked up here automatically.

    Uses `scalar`, not the `enum_type` shortcut: `compiler/schema_model.py`'s
    `EnumSpec.enum_class` builds every member's `.value` from
    `v.strip().lower()`, deliberately canonicalising case-only near-duplicates
    (the same mechanism behind the enum-collision warnings during `regen`) --
    but real CSV data keeps its original casing (`"Procedure"`, not
    `"procedure"`). `enum_type`'s exact-match default would fail against
    every such column, universally, not as an edge case (confirmed against
    real data: 100% of `canonicaltriples.class_1` values failed before this
    was normalised the same way here). The `scalar` callable below applies
    the identical `.strip().lower()` before matching, so casting agrees
    with whatever the compiler actually generated rather than a second,
    independently-drifting assumption about it. Stores the matching
    member's `.name` -- `sa.Enum`'s own default column-storage convention,
    which every generated enum column here uses (no `values_callable`
    customisation). An unmatched value is recorded via the existing
    `TableCastingStats`/on_error path and the column is set to `None`,
    instead of the previous behaviour of silently passing an unrecognised
    string straight through.

    Idempotent and cheap to call on every load (`toolbox/loading.py` does),
    rather than at import time -- so merely importing this module doesn't
    silently alter orm-loader's global cast behaviour for the whole process.
    """
    from orm_loader.loaders.data.converters import register_column_cast_rule

    def _make_scalar(enum_type: type[Enum]) -> Callable[[Any], Any]:
        def _scalar(value: Any) -> Any:
            if value is None:
                return None
            s = str(value).strip().lower()
            if not s:
                return None
            return enum_type(s).name  # raises on no matching member
        return _scalar

    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, sa.Enum):
                register_column_cast_rule(table.name, col.name, scalar=_make_scalar(col.type.python_type))


def is_concrete_entity(obj: object) -> bool:
    """True for a real, mapped entity class -- not `Base` itself, and not an
    abstract class like `EntityBase`.

    Checks `"__abstract__" in obj.__dict__`, not `getattr(obj, "__abstract__",
    False)`: the latter follows normal attribute inheritance, so a concrete
    subclass of an abstract base (e.g. `Sigs(EntityBase, Base)`) incorrectly
    reports `__abstract__ == True` too, inherited from `EntityBase`, even
    though `Sigs` itself is genuinely mapped. Confirmed directly: `getattr(
    Sigs, "__abstract__", False)` is `True`, but `"__abstract__" in
    Sigs.__dict__` is `False`. SQLAlchemy only ever checks a class's own
    `__dict__` when deciding whether to map it -- this must too, or every
    concrete entity class gets silently excluded.
    """
    return (
        isinstance(obj, type)
        and issubclass(obj, Base)
        and obj is not Base
        and not obj.__dict__.get("__abstract__", False)
    )


def concrete_entities(module: ModuleType) -> list[type]:
    """All concrete, mapped entity classes defined in a generated model module."""
    return [obj for obj in vars(module).values() if is_concrete_entity(obj)]
