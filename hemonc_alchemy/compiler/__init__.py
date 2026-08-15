"""Author-facing schema compiler — NOT part of the runtime.

Installed only via `hemonc-alchemy[author]` (US-23). Reads the real HemOnc
data dictionary workbook and CSV snapshots and produces
schema/hemonc.linkml.yaml plus the generated files in ../model/ (entities.py,
enums.py). Never imported by ../model/ or ../toolbox/ — that dependency
direction is exactly what's being fixed relative to hemonc_import, where
model/entity_base.py imported CSV-casting primitives from the generator
package (registry_version), so a consumer wanting just the ORM transitively
pulled in the entire schema-generation toolchain.

Migration source: hemonc_import/src/hemonc_import/registry_version/ in the
sibling checkout (956+326+537+330+175 lines across dataclasses.py, infer.py,
natural_key_audit.py, sa_create.py, load_helpers.py). See each module here
for what specifically carries over, what's fixed in the process, and what's
new.
"""
