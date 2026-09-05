"""Standalone treatment selection contracts and query builders."""

from .specs import CategoryRequirement, ComponentRequirement, TreatmentSelectionSpec
from .variants import (
    VariantQueryArtifacts,
    build_variant_query_artifacts,
    build_variant_statement,
    select_variants,
)

__all__ = [
    "CategoryRequirement",
    "ComponentRequirement",
    "TreatmentSelectionSpec",
    "VariantQueryArtifacts",
    "build_variant_query_artifacts",
    "build_variant_statement",
    "select_variants",
]
