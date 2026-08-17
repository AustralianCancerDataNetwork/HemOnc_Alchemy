"""Cross-entity enrichment layer — mirrors omop_alchemy's cdm/handlers/.

Tiers 2, 3, and 4 of the split described in ../model/relationships.py's
docstring: fuzzy cross-reference resolution (linking.py), clinical
classification (classification.py), and dosing-schedule parsing
(schedule/). All three consume the model but are not themselves
declarative ORM relationships -- that distinction is the whole point of
splitting them out (US-16, US-17).

Deliberately plain functions, not properties monkey-patched onto the entity
classes -- see linking.py's module docstring for why.
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
