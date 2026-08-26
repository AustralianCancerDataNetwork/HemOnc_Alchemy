"""Following HemOnc's cross-references between sigs, studies, variants and
conditions.

Some of these links are only recorded as free text — a `study` field holding
several study names separated by `|`, for example — so resolving them means
splitting that text and looking the names up. That is a best-effort match on
what the source wrote, not a guaranteed join, and a name that doesn't resolve
is simply absent from the result rather than raising.

Each function takes an entity and returns the related entities, deduplicated.
Several issue their own queries, so the entity must be attached to a session.
"""

from __future__ import annotations

from typing import cast

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
            # cast: attached in model.relationships, so invisible statically.
            study_objects = cast(list[Studies], study_map_row.study_objects)
            studies.extend(study_objects)

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
