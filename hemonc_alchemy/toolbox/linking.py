"""Fuzzy cross-entity resolution: sig <-> study <-> variant <-> condition.

Tier 2 of the split from hemonc_import's final_model/relationships.py
(US-16). These resolvers parse pipe-delimited free text and issue ad hoc
`session.execute(select(...))` queries — best-effort cross-referencing, not
guaranteed-correct FK joins, which is exactly why they don't belong in
model/relationships.py.

Pending model/entities.py existing, these cannot be ported verbatim yet.
Source and required fix, ported from
hemonc_import/src/hemonc_import/final_model/relationships.py:47-154:

- `sig_study_tokens`   (line 85-87)   — pure, portable as-is once Sigs exists.
- `sig_variant_context` (line 90-101) — casts `int(variant_cui)` before
  querying Variants, specifically because Sigs.variant_cui (Float) and
  Variants.variant_cui (BigInteger) disagree — this is a workaround for the
  type mismatch flagged in model/relationships.py's docstring. Once the
  compiler emits one canonical type for variant_cui across Sigs, Variants,
  and VariantEligibility, this manual cast becomes unnecessary — don't port
  the cast forward without first checking whether it's still needed.
- `sig_study_objects`   (line 104-135)
- `sig_condition_objects` (line 138-154)
- `study_condition_object` / `study_variant_objects` (line 47-57)
- `variant_condition_objects` / `condition_variant_objects` (line 60-82)

All of the above use `dedupe_by`/`split_pipe_values` from
../model/relationships.py (already ported, pure, verified) for
deduplication and token parsing.
"""

from __future__ import annotations
