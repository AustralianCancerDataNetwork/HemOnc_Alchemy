"""
Base class for all hemonc-alchemy entity tables.

Mirrors ``omop_alchemy.cdm.base.CDMTableBase``

This class does NOT provide pipe-delimited denormalisation / explode handling 
(a HemOnc sig/regimen row can expand into N child rows), and natural-key-based 
FK resolution at load time for surrogate-PK tables 

This is handled in `toolkit/loading.py` (`load_denormalised`).
"""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from types import ModuleType
from typing import Any

import sqlalchemy as sa
import sqlalchemy.orm as so
from orm_loader.tables import CSVLoadableTableInterface, SerialisableTableInterface

from ..naming import safe_enum_key


class Base(so.DeclarativeBase):
    pass


class EntityBase(Base, CSVLoadableTableInterface, SerialisableTableInterface):
    """Abstract base for every generated HemOnc entity class."""

    __abstract__ = True


def register_enum_casts() -> None:
    """
    
    Register a validating cast rule for every generated `sa.Enum` column,
    across every table (including generated map/denormalised tables)

    Uses `scalar`, instead of the `enum_type` default, because
    `compiler/schema_model.py`'s `EnumSpec.enum_class` builds `.value` from
    `v.strip().lower()`, deliberately canonicalising case-only near-duplicates
    but real CSV data keeps its original casing (`"Procedure"`, not
    `"procedure"`). `enum_type`'s exact-match default would fail against
    every such column.
    
    Stores the matching member's `.name` (per `sa.Enum` defaults),
    
    An unmatched value is recorded via the existing `TableCastingStats`
    on_error path and the column is set to `None`.
    """
    from orm_loader.loaders.data.converters import register_column_cast_rule

    def _make_scalar(enum_type: type[Enum]) -> Callable[[Any], Any]:
        def _scalar(value: Any) -> Any:
            if value is None:
                return None
            s = str(value).strip().lower()
            if not s:
                return None
            try:
                return enum_type(s).name  # exact value match
            except ValueError:
                # Fall back to the member *name*, because that is the
                # equivalence the compiler actually asserted. Where two source
                # spellings normalise to one `safe_enum_key`, only one of them
                # survives as a member value (the last seen, so effectively
                # decided by CSV row order), and an exact-value lookup nulls
                # every row carrying the other. 'CPS at least 10%' x3 lost to
                # 'CPS at least 10' x1; plain 'RMST' x12 lost to 'RMST:' x1.
                # Both spellings map to the same member here instead.
                try:
                    return enum_type[safe_enum_key(s)].name
                except KeyError as exc:
                    # Re-raised as ValueError so this rule has one failure
                    # type regardless of which lookup missed. orm-loader
                    # catches Exception and routes it to on_error either way,
                    # but callers testing the rule directly shouldn't have to
                    # know which of the two paths ran.
                    raise ValueError(
                        f"{value!r} matches no member of {enum_type.__name__}"
                    ) from exc
        return _scalar

    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, sa.Enum):
                enum_type = col.type.enum_class
                if enum_type is None:
                    continue
                register_column_cast_rule(table.name, col.name, scalar=_make_scalar(enum_type))


def is_concrete_entity(obj: object) -> bool:
    """
    True for a real, mapped entity class (not `Base` itself, and not an
    abstract class like `EntityBase`)
    
    This is required because SQLAlchemy only ever checks a class's 
    own `__dict__` when deciding whether to map it
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
