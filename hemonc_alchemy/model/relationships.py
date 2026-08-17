"""
Declarative ORM relationships ONLY 

Tiers 2, 3, and 4 live in ../../toolbox/ (linking.py, classification.py, 
schedule/). 

These are NOT redundant with the compiler's auto-inferred soft
relationships (the `*_obj`/`*_objects` viewonly relationships already
declared directly on the generated classes in entities.py, e.g.
`Studies.condition_cui_obj`). That inference will only fire when a column name
matches another table's *unique* `source_defined_keys` exactly. 

It deliberately does not cover:
- differently-named FK-like columns (`Sigs.component_cui` -> `Drugs.drug_cui`,
  `Sigs.variant_cui` -> `Variants.variant_cui`)
- joins onto a non-unique column (`Variants.variant_cui` isn't globally
  unique per row so it can never appear in any table's `source_defined_keys`, 
  and the same is true of `Studies.study`)
- the reverse (one-to-many) direction of an auto-inferred relationship
  (`Conditions.studies`, the reverse of `Studies.condition_cui_obj`)
"""

from __future__ import annotations

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import foreign, relationship

from .entities import Conditions, Drugs, Sigs, Studies, Variants, variants_StudyMap


def dedupe_by(items, key_fn):
    """
    Deduplicate an iterable by a derived key, preserving first-seen order.

    Skips None items and items whose key_fn returns None
    """
    seen = {}
    for item in items:
        if item is None:
            continue
        key = key_fn(item)
        if key is None:
            continue
        seen.setdefault(key, item)
    return list(seen.values())


def split_pipe_values(value):
    """Split a pipe-delimited free-text field into deduplicated, stripped tokens."""
    if value is None:
        return []
    return dedupe_by(
        (part.strip() for part in str(value).split("|")),
        lambda part: part or None,
    )


Variants.component_sigs = relationship(
    Sigs,
    primaryjoin=foreign(Sigs.variant_cui) == Variants.variant_cui,
    viewonly=True,
    lazy="selectin",
)

Drugs.sigs = relationship(
    Sigs,
    primaryjoin=foreign(Sigs.component_cui) == Drugs.drug_cui,
    viewonly=True,
    lazy="selectin",
)

Sigs.variant_object = relationship(
    Variants,
    primaryjoin=foreign(Sigs.variant_cui) == Variants.variant_cui,
    viewonly=True,
    lazy="select",
)

Sigs.drug_object = relationship(
    Drugs,
    primaryjoin=foreign(Sigs.component_cui) == Drugs.drug_cui,
    viewonly=True,
    lazy="selectin",
)

Conditions.studies = relationship(
    Studies,
    primaryjoin=foreign(Studies.condition_cui) == Conditions.condition_cui,
    viewonly=True,
    lazy="selectin",
)

variants_StudyMap.study_objects = relationship(
    Studies,
    primaryjoin=foreign(Studies.study) == variants_StudyMap.study,
    viewonly=True,
    lazy="selectin",
)

variants_StudyMap.variant_objects = relationship(
    Variants,
    primaryjoin=foreign(Variants.id) == variants_StudyMap.parent_id,
    viewonly=True,
    lazy="selectin",
)

Studies.variants = relationship(
    Variants,
    secondary="variants_study",
    primaryjoin=foreign(variants_StudyMap.study) == Studies.study,
    secondaryjoin=foreign(variants_StudyMap.parent_id) == Variants.id,
    viewonly=True,
    lazy="selectin",
)

Variants.drugs = association_proxy("component_sigs", "drug_object")
