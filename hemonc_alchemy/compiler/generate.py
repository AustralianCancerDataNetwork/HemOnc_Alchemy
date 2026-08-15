"""The one schema/model generator (US-11).

hemonc_import had two competing, divergent generators:
registry_version/dataclasses.py's `render_sa_models` (used by the real entry
point) and registry_version/sa_create.py's `generate_sqlalchemy_from_registry`
(driven ad hoc from a notebook, and confirmed to crash outright —
`write_entity_class` references `rel_lines` before it's assigned, an
UnboundLocalError on any table with an FK-like column, i.e. exactly the case
the feature exists for). This module replaces both with one path.

Port from dataclasses.py, taking the correct piece from sa_create.py where
dataclasses.py was wrong:

- PK default bug (dataclasses.py:246): `default=-1` applied to a primary key
  regardless of column type. CONFIRMED already manifested in checked-in
  hemonc_import output — `String` primary keys on HemoncClasses, HemoncRels,
  Exclusions, SigBranchTypes, Units got an int default. sa_create.py:64-67
  already has the correct type-branching logic (`-1` for int PKs, `''` for
  string PKs) — port that branch, not dataclasses.py's unconditional one.
- Nullable/type-hint mismatch (dataclasses.py:208 vs :245): the Python type
  hint's `Optional[...]` and the SQL `nullable=` flag are computed from two
  different values. CONFIRMED manifested: `Mapped[Optional[str]] =
  mapped_column(..., nullable=False, ...)`. Derive both from the same
  adjusted-for-PK nullable value.
- `EnumSpec.tablename` bug (dataclasses.py:435): sets `tablename=col_name`
  instead of the table name, corrupting `registry.json`/schema previews
  (doesn't affect generated code directly, but corrupts the schema metadata
  that compiler/diff.py and audit.py rely on being accurate).

Output target: model/entities.py (inheriting model.base.EntityBase),
model/enums.py, schema/hemonc.linkml.yaml (see schema/README.md — the LinkML
generation is NOT `gen-sqla`, which was tested against this project's data
and found too generic: plain `Column()`, no `Mapped[]`, no EntityBase mixin,
no denormalisation/map-table pattern — this module's job is to combine the
LinkML schema shape with infer.py's HemOnc-specific inference to produce
that shape directly).
"""

from __future__ import annotations
