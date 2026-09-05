"""Small model-backed treatment read models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VariantBundle:
    """A selected HemOnc variant and the sig rows used to describe it.

    The ORM rows are retained rather than copied into a second schema. This
    gives callers an immutable boundary for composing selection,
    classification, and scheduling.
    """

    variant: Any
    sigs: tuple[Any, ...]

    @classmethod
    def from_variant(cls, variant: Any) -> VariantBundle:
        return cls(
            variant=variant,
            sigs=tuple(getattr(variant, "component_sigs", ())),
        )

    @property
    def variant_cui(self) -> int | None:
        value = getattr(self.variant, "variant_cui", None)
        return int(value) if value is not None else None

    @property
    def version(self) -> int | None:
        value = getattr(self.variant, "version", None)
        return int(value) if value is not None else None

    @property
    def regimen(self) -> str | None:
        return getattr(self.variant, "regimen", None)

    @property
    def components(self) -> frozenset[str]:
        return frozenset(
            component
            for component in (getattr(sig, "component", None) for sig in self.sigs)
            if component is not None
        )
