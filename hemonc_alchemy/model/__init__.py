from .base import Base, EntityBase

__all__ = [
    "Base",
    "EntityBase",
]

# Entity classes (Drugs, Sigs, Studies, Variants, Conditions, ...) are added
# here once compiler/generate.py has produced entities.py — see that
# module's docstring. Import them explicitly by name as they land; don't
# `from .entities import *`, which is exactly the leaky-namespace problem
# this rewrite is meant to fix (US-1).
