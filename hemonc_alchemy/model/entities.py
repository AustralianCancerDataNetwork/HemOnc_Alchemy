"""Generated ORM entity classes — DO NOT hand-edit.

Produced by compiler/generate.py from schema/hemonc.linkml.yaml, inheriting
from model.base.EntityBase. Empty until the compiler is ported and run for
the first time against the real HemOnc data dictionary
(_design/hemonc-alchemy-spec.md TS-6, steps 3-4).

The original (1650 lines, with several confirmed generation bugs already
fixed in the compiler rewrite plan — see hemonc-alchemy-spec.md US-9
through US-13) lives at
hemonc_import/src/hemonc_import/final_model/entities.py in the sibling
checkout. That file is the migration reference, not something to copy
verbatim: it should be regenerated fresh by the new compiler once that
exists, not hand-ported, since the whole point of fixing the compiler first
is that the output changes (filename-mapping fixes recover 4 tables that
were previously silently skipped, the default=-1/nullable-mismatch bugs are
gone, column-group ordering is deterministic).
"""
