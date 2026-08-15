"""Base class for all hemonc-alchemy entity tables.

Mirrors ``omop_alchemy.cdm.base.CDMTableBase``: the same orm-loader
interfaces provide chunked, staged CSV loading (merge strategies, not
insert-only), and serialisation, for free (US-19, US-20). Verified to
compose cleanly against orm-loader>=1.0.0 — see
_design/hemonc-alchemy-spec.md TS-6 step 4.

What this class does NOT provide, because orm-loader is deliberately
domain-agnostic and has no equivalent (US-19's "what stays custom"):

- Pipe-delimited denormalisation / explode handling (a HemOnc sig/regimen
  row can expand into N child rows). Port from hemonc_import's
  final_model/entity_base.py: `_prepare_denorm_dataframe`,
  `__load_denormalised__`.
- Enum-from-CSV-snapshot casting. Port from
  hemonc_import's registry_version/load_helpers.py `_to_enum_literal`,
  fixed per US-22 to surface unknown values rather than silently return
  None.
- Natural-key business logic / `_lookup_parent_ids`-style resolution by
  business key rather than surrogate FK.

Type casting itself should NOT be re-implemented here — reuse
`orm_loader.data.converters.perform_cast`/`cast_scalar` directly (US-20),
which already tracks per-column cast failures via `TableCastingStats`
instead of hemonc_import's old `-1`/`-1.0` sentinel-on-failure behaviour.
"""

from __future__ import annotations

import sqlalchemy.orm as so
from orm_loader.tables import CSVLoadableTableInterface, SerialisableTableInterface


class Base(so.DeclarativeBase):
    pass


class EntityBase(Base, CSVLoadableTableInterface, SerialisableTableInterface):
    """Abstract base for every generated HemOnc entity class."""

    __abstract__ = True
