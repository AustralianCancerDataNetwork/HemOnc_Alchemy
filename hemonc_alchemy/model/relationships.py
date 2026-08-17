"""Declarative ORM relationships ONLY — tier 1 of the four-tier split found
in hemonc_import's final_model/relationships.py (US-16,
_design/hemonc-alchemy-spec.md).

That file mixed four things in one module: (1) real declarative
`relationship()`/`association_proxy` FK-like joins, (2) fuzzy cross-entity
resolvers that parse free text and issue ad hoc queries, (3) clinical
classification logic, and (4) schedule properties attached from a different
file entirely. Tiers 2, 3, and 4 now live in ../../toolbox/ (linking.py,
classification.py, schedule/) -- none of them are declarative ORM shape,
so none of them belong here.

These are NOT redundant with the compiler's auto-inferred soft
relationships (the `*_obj`/`*_objects` viewonly relationships already
declared directly on the generated classes in entities.py, e.g.
`Studies.condition_cui_obj`): that inference only fires when a column name
matches another table's *unique* `source_defined_keys` exactly. It
deliberately does not cover:
- differently-named FK-like columns (`Sigs.component_cui` -> `Drugs.drug_cui`,
  `Sigs.variant_cui` -> `Variants.variant_cui`)
- joins onto a non-unique column (`Variants.variant_cui` isn't globally
  unique per row -- multiple versions share it -- so it can never appear in
  any table's `source_defined_keys`, and the same is true of `Studies.study`)
- the reverse (one-to-many) direction of an auto-inferred relationship
  (`Conditions.studies`, the reverse of `Studies.condition_cui_obj`)

Ported from
hemonc_import/src/hemonc_import/final_model/relationships.py:183-244,
confirmed against the real generated classes (all column names/types
checked directly against model/entities.py, not assumed). One thing
changed from the original: `Variants.component_sigs`'s join no longer needs
a manual int() cast anywhere -- the confirmed variant_cui Float/BigInteger/
String type mismatch across Sigs/Variants/VariantEligibility (US-18) is
fixed at the source (compiler/infer.py's detect_numeric + the
`_cui`-placeholder handling in compiler/schema_model.py), so all three are
now BigInteger.
"""

from __future__ import annotations

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import foreign, relationship

from .entities import Conditions, Drugs, Sigs, Studies, Variants, variants_StudyMap


def dedupe_by(items, key_fn):
    """Deduplicate an iterable by a derived key, preserving first-seen order.

    Skips None items and items whose key_fn returns None. Pure, no entity
    dependency -- used throughout toolbox/linking.py's resolvers.
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
