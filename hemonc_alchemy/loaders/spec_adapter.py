"""HemOnc TableSpec/FieldSpec adapter over orm_loader.registry.validation.

New in this rewrite (US-21) — not a port of anything in hemonc_import, which
had no equivalent. orm_loader's `registry/registry.py`
(`ModelRegistry`, `ModelDescriptor.from_model`) and `registry/validation.py`
(`ColumnPresenceValidator`, `ColumnNullabilityValidator`, `PrimaryKeyValidator`,
`ForeignKeyShapeValidator`) already implement "does the generated ORM model
match its declared spec" — today coupled to OMOP-style CSV specs
(`cdmTableName`/`cdmFieldName`/`isRequired` columns via
`load_table_specs`/`load_field_specs`). The `Validator` protocol itself is
spec-format-agnostic.

This module's job: load HemOnc's own TableSpec/FieldSpec entries from
schema/hemonc.linkml.yaml (once it exists) rather than an OMOP CSV, and hand
them to orm_loader's existing validators. Used by
../compiler/validate.py — don't reimplement validator plumbing here.
"""

from __future__ import annotations
