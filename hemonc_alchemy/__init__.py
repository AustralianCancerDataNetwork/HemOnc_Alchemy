"""hemonc-alchemy: SQLAlchemy models and tooling for the HemOnc.org oncology terminology.

Sibling to omop-alchemy — shares its infrastructure (oa-configurator,
orm-loader) but not its ORM models. See _design/hemonc-alchemy-spec.md for
the full rationale and TS-5 for why the two are not coupled directly.

This is the curated public surface (US-1). Everything a consumer needs is
importable from here; anything else is an implementation detail. As entities
are ported in, add them here explicitly rather than doing `import *` from a
submodule.
"""

from .config import HemOncAlchemyConfig

__all__ = [
    "HemOncAlchemyConfig",
]
