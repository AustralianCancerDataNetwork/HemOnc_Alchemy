"""Natural-key duplicate audit and enum-threshold proximity checks.

Ports hemonc_import/src/hemonc_import/registry_version/natural_key_audit.py
(537 lines) — the strongest module in the original registry_version package
(clear AuditResult model, reasonable status taxonomy). Two fixes to apply
during the port:

- Value comparison (source natural_key_audit.py:102-109): the audit compares
  business-key values via raw `repr(value)`, while the actual runtime loader
  (`perform_cast`) canonicalizes numeric-looking values to one string form
  specifically to avoid over-counting distinct values. CONFIRMED real
  disagreement in the real data: `contexttable` (key=`contextraw`) — the
  repr()-based audit reports 0 duplicates, a canonicalized comparison
  reports 1, caused by `"Relapsed_or_refractory"` vs
  `"Relapsed_or_Refractory"` (case-only). Share one canonicalization
  function between this audit and orm_loader's `perform_cast`/`cast_scalar`
  (US-20) rather than maintaining two independent value-normalisation
  implementations that can disagree.
- Boilerplate (source natural_key_audit.py:125-206,238-291): five near-
  identical ~14-field `AuditResult(...)` constructions, and a decision-
  application function that re-lists all 14 fields to change 2 of them.
  Use `dataclasses.replace` instead of re-listing every field each time.

New in this module, not present in the original (US-8, US-15):

- Enum-threshold proximity warning: flag any enum column within N (default
  3) values of infer.py's `MAX_ENUM_UNIQUE` cliff, so a Schema Author gets
  advance warning before the next HemOnc release silently demotes an enum
  to plain string. Currently 3 real columns would be flagged:
  `conditions.condition_type` (19/20), `units.unit_type` (19/20),
  `studies.registry` (17/20).

Also worth revisiting during the port: `TABLE_DECISIONS`
(natural_key_audit.py:14-36) hardcodes per-table review exceptions directly
in source. If this audit is meant to be reusable, that should become
external config, not a Python literal.
"""

from __future__ import annotations
