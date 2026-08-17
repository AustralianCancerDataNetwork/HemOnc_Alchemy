from .base import Base, EntityBase
from .entities import Conditions, Drugs, Sigs, Studies, VariantEligibility, Variants, StudyResults, drugs_Canmed_major_classMap, drugs_Canmed_minor_classMap, variants_StudyMap, variants_StudyMap

__all__ = [
    "Base",
    "Conditions",
    "Drugs",
    "EntityBase",
    "Sigs",
    "Studies",
    "StudyResults",
    "VariantEligibility",
    "Variants",
    "drugs_Canmed_major_classMap",
    "drugs_Canmed_minor_classMap",
    "variants_StudyMap",
]

# Import order matters and must come after the block above
# 
# relationships.py attaches soft relationships onto the entity classes 
# via post-hoc assignment (`Variants.component_sigs = relationship(...)`), 
# so entities must already be imported first. 
# 
# Importing `hemonc_alchemy.model` (or the top-level `hemonc_alchemy` package) 
# is what guarantees this; reaching directly into `hemonc_alchemy.model.entities` 
# without going through here would skip it. 
#
# Kept as its own statement (not merged into the block above) specifically 
# so an import-sorter can't reorder it earlier.
from . import relationships  # noqa: F401