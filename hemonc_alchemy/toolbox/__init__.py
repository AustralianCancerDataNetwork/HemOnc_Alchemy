"""Helpers that work across entities.

Three kinds of thing, none of which is a plain database lookup:

- `classification` — treatment-level judgements, such as whether a variant is
  radiotherapy only or concurrent chemoradiotherapy.
- `linking` — following HemOnc's free-text cross-references between sigs,
  studies, variants and conditions. Best-effort, not guaranteed joins.
- `schedule` — reading dosing schedules out of a sig's `alldays` expression.

These are functions you call on an entity, rather than attributes on it, so it
is always visible where a query or an inference is happening.
"""

from .classification import (
    has_non_radiation_sig,
    has_radiation_sig,
    is_concurrent_chemort,
    is_rt_only,
)
from .linking import (
    condition_variant_objects,
    sig_condition_objects,
    sig_study_objects,
    sig_study_tokens,
    sig_variant_context,
    study_condition_object,
    study_variant_objects,
    variant_condition_objects,
)

__all__ = [
    "condition_variant_objects",
    "has_non_radiation_sig",
    "has_radiation_sig",
    "is_concurrent_chemort",
    "is_rt_only",
    "sig_condition_objects",
    "sig_study_objects",
    "sig_study_tokens",
    "sig_variant_context",
    "study_condition_object",
    "study_variant_objects",
    "variant_condition_objects",
]
