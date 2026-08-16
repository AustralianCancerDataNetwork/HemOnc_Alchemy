"""Author-facing schema compiler — NOT part of the runtime.

Installed only via `hemonc-alchemy[author]` (US-23). Reads the real HemOnc
data dictionary workbook and CSV snapshots and produces the interim JSON
registry snapshot (schema/registry.json — schema/hemonc.linkml.yaml is the
eventual replacement, pending the slot-scoping prototype, US-14) plus the
generated files in ../model/ (entities.py, enums.py). Never imported by
../model/ or ../toolbox/.

Migrated from hemonc_import/src/hemonc_import/registry_version/ (the
original registry_main.py + sa_create.py + dataclasses.py + infer.py +
natural_key_audit.py + load_helpers.py, ~2300 lines total):

- infer.py       — HemOnc-specific inference (type/enum/key/pipe-group),
                   with the parenthetical-stripping and non-deterministic-
                   ordering bugs fixed (US-9, US-10), plus the new
                   `resolve_source_csv` (US-13).
- load_helpers.py — trimmed to the two dictionary-facing helpers the
                   compiler needs; the runtime CSV-casting helpers moved
                   to (pending) model/base.py work, per US-19/US-20.
- schema_model.py — TableMeta/ColumnSpec/EnumSpec/Registry (renamed from
                   the original's `dataclasses.py`, which shadowed the
                   stdlib module), with the default=-1 and nullable/type
                   mismatch bugs fixed (part of US-8's rendering
                   correctness).
- generate.py    — the one generator (US-11); sa_create.py deleted.
- audit.py       — natural-key audit with the canonicalization fix (US-12)
                   and the new enum-threshold check (US-15).
- validate.py    — new (US-8): structural + syntactic validation.
- diff.py        — new (US-8): registry diff against the last committed
                   version.
- spec_adapter.py — new (US-21): HemOnc TableSpec/FieldSpec over
                   orm_loader.registry.validation's always-on validators,
                   run as a second, stronger validation layer by cli.py's
                   `validate` command (requires the generated model to
                   actually import and map, not just parse).
"""
