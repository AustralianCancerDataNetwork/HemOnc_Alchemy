"""Post-generation structural validation — new in this rewrite (US-8).

hemonc_import had no validation step after writing generated files: nothing
checked the output was syntactically valid Python, or that every declared
primary-key column actually existed on its table. This module is that
missing gate.

Two implementation paths, in order of preference:

1. Reuse orm_loader.registry.validation's `Validator` protocol (US-21):
   `ColumnPresenceValidator`, `ColumnNullabilityValidator`,
   `PrimaryKeyValidator`, `ForeignKeyShapeValidator` already exist there and
   are spec-format-agnostic — write a HemOnc `TableSpec`/`FieldSpec` adapter
   (loaders/spec_adapter.py) rather than reimplementing validator plumbing.
2. Where orm_loader's validators don't cover something HemOnc-specific
   (e.g. denormalised map-table shape), add a narrow, purpose-built check
   here rather than growing the adapter to fake a generic case.

Minimum bar before `hemonc-alchemy regen` can report success:
- the freshly generated model/entities.py parses (`ast.parse`)
- every table's declared primary-key column(s) actually exist among its
  generated columns
- every enum referenced by a column exists in model/enums.py
"""

from __future__ import annotations
