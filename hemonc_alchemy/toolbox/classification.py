"""Clinical/domain classification rules.

Tier 3 of the split from hemonc_import's final_model/relationships.py
(US-17) -- not a relationship at all, but domain classification, comparable
to SCOOP's protocols/classification/. Plain functions taking a `Variants`
instance explicitly, not monkey-patched properties -- see toolbox/linking.py's
module docstring for why.

`RAD_SIG_CLASS_VALUE` is a named constant rather than the original's inline
`"rad sig"` string literal. Confirmed real and stable: `Sigs.class_field` is
a proper enum column (`Sigs_Class_fieldEnum.RAD_SIG = 'rad sig'` in
model/enums.py) -- comparing against the string constant works because
`Sigs_Class_fieldEnum(str, Enum)` members compare equal to their string
value, without this module needing to import the generated enums module
directly.
"""

from __future__ import annotations

RAD_SIG_CLASS_VALUE = "rad sig"


def _sig_class_value(sig_or_value):
    value = getattr(sig_or_value, "class_field", sig_or_value)
    return getattr(value, "value", value)


def has_radiation_sig(variant) -> bool:
    """Whether any of a variant's component sigs are a radiation sig."""
    return any(_sig_class_value(sig) == RAD_SIG_CLASS_VALUE for sig in variant.component_sigs)


def has_non_radiation_sig(variant) -> bool:
    """Whether any of a variant's component sigs are NOT a radiation sig."""
    return any(_sig_class_value(sig) != RAD_SIG_CLASS_VALUE for sig in variant.component_sigs)


def is_concurrent_chemort(variant) -> bool:
    """Whether a variant mixes radiation and non-radiation sigs (concurrent chemoradiotherapy)."""
    return has_radiation_sig(variant) and has_non_radiation_sig(variant)


def is_rt_only(variant) -> bool:
    """Whether a variant is radiation-only (no non-radiation component sigs)."""
    return has_radiation_sig(variant) and not has_non_radiation_sig(variant)
