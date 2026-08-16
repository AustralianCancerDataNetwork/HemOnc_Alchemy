"""Fuzzy cross-entity resolution: sig <-> study <-> variant <-> condition.

Tier 2 of the split from hemonc_import's final_model/relationships.py
(US-16). These resolvers parse pipe-delimited free text and issue ad hoc
`session.execute(select(...))` queries -- best-effort cross-referencing,
not guaranteed-correct FK joins, which is exactly why they don't belong in
model/relationships.py.

Deliberately plain functions taking the entity as an explicit argument
(`sig_study_tokens(sig)`), not properties monkey-patched onto the entity
classes (`sig.study_tokens`). The original attached these via
`Cls.attr = free_function; Cls.attr.__set_name__(Cls, "attr")` --
`cached_property` specifically *requires* `__set_name__` to know its own
storage key, and that call is only made automatically by the interpreter
during class-body execution, not on a post-hoc setattr. A plain function is
just as discoverable (`dir(toolbox.linking)`, normal imports) without that
fragility, directly serving US-4.

One real bug fixed during the port, not reproduced: the original's
`variant_condition_objects` (bound to `Variants.condition_objects`) and
`sig_study_objects` both referenced `variant.study_objects` -- but no such
attribute was ever defined anywhere on `Variants` (only
`Studies.variant_objects` and `variants_StudyMap.study_objects` exist).
`variant_condition_objects` would have raised `AttributeError` on first
real use; `sig_study_objects` silently degraded via `getattr(..., [])`.
Both are fixed here by routing through the actual relationship chain:
`variant.study_items` (the raw per-token child rows) -> each row's
`.study_objects` (resolved Studies matching that token).

Also removed: `sig_variant_context`'s manual `int(variant_cui)` cast. It
existed specifically because `Sigs.variant_cui` (Float) and
`Variants.variant_cui` (BigInteger) used to disagree -- now that both are
BigInteger (US-18, compiler/infer.py's detect_numeric fix), the cast is
unneeded.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import object_session

from ..model.entities import Studies, Variants
from ..model.relationships import dedupe_by, split_pipe_values


def study_condition_object(study):
    """A study's resolved condition, preferring the condition_cui-keyed
    match over the condition-name-keyed one."""
    return study.condition_cui_obj or study.condition_obj


def study_variant_objects(study):
    """A study's distinct resolved variants, deduped by variant_cui."""
    return dedupe_by(study.variants, lambda variant: getattr(variant, "variant_cui", None))


def variant_condition_objects(variant):
    """A variant's distinct resolved conditions, via its raw study tokens."""
    conditions = (
        study_condition_object(study)
        for study_map_row in variant.study_items
        for study in study_map_row.study_objects
    )
    return dedupe_by(
        conditions,
        lambda condition: (getattr(condition, "condition_cui", None), getattr(condition, "condition", None)),
    )


def condition_variant_objects(condition):
    """A condition's distinct resolved variants, via its resolved studies."""
    variants = []
    for study in condition.studies:
        variants.extend(study_variant_objects(study))
    return dedupe_by(variants, lambda variant: getattr(variant, "variant_cui", None))


def sig_study_tokens(sig) -> list[str]:
    """A sig's raw pipe-delimited `study` field, split and deduped."""
    return split_pipe_values(getattr(sig, "study", None))


def sig_variant_context(sig) -> Variants | None:
    """The most recent Variants row matching a sig's `variant_cui`, if any.

    Requires the sig to be attached to a session (this issues a query).
    """
    variant_cui = getattr(sig, "variant_cui", None)
    session = object_session(sig)
    if session is None or variant_cui is None:
        return None
    return (
        session.execute(
            select(Variants).where(Variants.variant_cui == variant_cui).order_by(Variants.version.desc(), Variants.id.desc())
        )
        .scalars()
        .first()
    )


def sig_study_objects(sig) -> list[Studies]:
    """A sig's resolved Studies: those reachable via its variant context,
    plus any remaining raw study tokens resolved by direct name lookup."""
    studies = []
    variant = sig_variant_context(sig)
    if variant is not None:
        for study_map_row in variant.study_items:
            studies.extend(study_map_row.study_objects)

    tokens = set(sig_study_tokens(sig))
    tokens.difference_update({getattr(study, "study", None) for study in studies if getattr(study, "study", None)})

    session = object_session(sig)
    if session is not None and tokens:
        studies.extend(session.execute(select(Studies).where(Studies.study.in_(sorted(tokens)))).scalars().all())

    return dedupe_by(
        studies,
        lambda study: (getattr(study, "id", None), getattr(study, "study", None), getattr(study, "condition_cui", None)),
    )


def sig_condition_objects(sig):
    """A sig's resolved conditions: via its variant context, plus via its resolved studies."""
    variant = sig_variant_context(sig)
    conditions = []
    if variant is not None:
        conditions.extend(variant_condition_objects(variant))
    conditions.extend(study_condition_object(study) for study in sig_study_objects(sig))
    return dedupe_by(
        conditions,
        lambda condition: (getattr(condition, "condition_cui", None), getattr(condition, "condition", None)),
    )
