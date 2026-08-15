"""Declarative ORM relationships ONLY — tier 1 of the four-tier split found
in hemonc_import's final_model/relationships.py (US-16,
_design/hemonc-alchemy-spec.md).

That file mixed four things in one module: (1) real declarative
`relationship()`/`association_proxy` FK-like joins, (2) fuzzy cross-entity
resolvers that parse free text and issue ad hoc queries, (3) clinical
classification logic, and (4) schedule properties attached from a different
file entirely. Tiers 2 and 3 now live in ../../toolbox/ (linking.py,
classification.py); tier 4 is attached from model/schedule/ itself, not
reached into from here.

Pending entities.py being generated (see entities.py's docstring), this
module cannot yet declare its relationships against real classes. Once it
can, prefer declaring them directly in the generated class bodies (in
compiler/generate.py's templates) over the old pattern of
`Cls.attr = free_function; Cls.attr.__set_name__(...)` monkey-patching after
the fact (US-4) — that pattern made relationships invisible to
`dir()`/IDE autocomplete and turned a missed `__set_name__` call into a
cryptic runtime error instead of an import-time one.

Relationships to port once entities.py exists (source:
hemonc_import/src/hemonc_import/final_model/relationships.py:183-244):
- Variants.component_sigs      (Sigs.variant_cui == Variants.variant_cui)
- Drugs.sigs                   (Sigs.component_cui == Drugs.drug_cui)
- Sigs.variant_object / Sigs.drug_object
- Conditions.studies           (Studies.condition_cui == Conditions.condition_cui)
- variants_StudyMap.study_objects / .variant_objects
- Studies.variants             (secondary="variants_study")
- Variants.drugs                (association_proxy over component_sigs -> drug_object)

Before porting: resolve the confirmed variant_cui type mismatch first
(Sigs.variant_cui is Float, Variants.variant_cui is BigInteger,
VariantEligibility.variant_cui is String — hemonc-import-audit.md). Pick one
canonical type in the compiler-generated schema rather than porting the
FLOAT=BIGINT join comparison as-is.
"""

from __future__ import annotations


def dedupe_by(items, key_fn):
    """Deduplicate an iterable by a derived key, preserving first-seen order.

    Skips None items and items whose key_fn returns None. Ported verbatim
    from the original relationships.py's `_dedupe_by` — pure, no entity
    dependency, used throughout the toolbox resolvers.
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
