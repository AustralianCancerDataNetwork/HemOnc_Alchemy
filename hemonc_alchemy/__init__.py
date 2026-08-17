"""hemonc-alchemy: SQLAlchemy models and tooling for the HemOnc.org oncology terminology.

Sibling to omop-alchemy — shares its infrastructure (oa-configurator,
orm-loader) but not its ORM models. See _design/hemonc-alchemy-spec.md for
the full rationale and TS-5 for why the two are not coupled directly.

This is the curated public surface (US-1) — covers exactly what SCOOP's
`_load_hemonc_models()` reaches for today (US-28), so a consumer repointing
from hemonc_import doesn't need to know anything about this package's
internal module layout. Anything else is reachable by submodule import but
isn't advertised here.
"""

from .config import HemOncAlchemyConfig, create_hemonc_engine, get_hemonc_context
from .model import Conditions, Drugs, Sigs, Studies, VariantEligibility, Variants
from .toolbox.schedule import resolve_all_days

__all__ = [
    "Conditions",
    "Drugs",
    "HemOncAlchemyConfig",
    "Sigs",
    "Studies",
    "VariantEligibility",
    "Variants",
    "create_hemonc_engine",
    "get_hemonc_context",
    "resolve_all_days",
]
