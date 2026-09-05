"""Classifying a regimen variant by treatment modality.

HemOnc records radiotherapy as a sig like any other, distinguished by its
`class` field. So whether a variant is radiotherapy alone, systemic therapy
alone, or the two given together is read off its component sigs.
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
