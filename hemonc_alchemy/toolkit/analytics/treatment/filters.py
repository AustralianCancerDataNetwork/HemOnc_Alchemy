"""Composable treatment-specific filters."""

from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from ....model import (
    Sigs,
    Studies,
    sigs_StudyMap,
)
from ....model.enums import Sigs_Class_fieldEnum


def _condition_cuis(condition_cuis: Iterable[int]) -> tuple[int, ...]:
    result = tuple(dict.fromkeys(condition_cuis))
    if not result:
        raise ValueError("At least one condition CUI is required.")
    return result


def standalone_radiation_sig_statement(
    condition_cuis: Iterable[int],
) -> Select:
    """Select standalone radiation sigs associated with given conditions.

    “Standalone” follows the existing SCOOP rule: the sig is marked as a
    radiation sig, is named ``Radiation therapy``, and has no variant CUI.
    Study membership is resolved through the normalized ``sigs_study`` map.
    """
    return (
        select(Sigs)
        .join(sigs_StudyMap, sigs_StudyMap.parent_id == Sigs.id)
        .join(Studies, Studies.study == sigs_StudyMap.study)
        .where(
            Studies.condition_cui.in_(_condition_cuis(condition_cuis)),
            Sigs.class_field == Sigs_Class_fieldEnum.RAD_SIG,
            Sigs.regimen == "Radiation therapy",
            Sigs.variant_cui.is_(None),
        )
        .distinct()
    )


def studies_with_standalone_radiation_sigs_statement(
    condition_cuis: Iterable[int],
) -> Select:
    """Select ``Studies.id`` values containing a standalone radiation sig.

    ``Studies.study`` is not globally unique in the generated model, so
    distinctness applies to entity IDs rather than source study names.
    """
    return (
        select(Studies.id)
        .join(sigs_StudyMap, sigs_StudyMap.study == Studies.study)
        .join(Sigs, Sigs.id == sigs_StudyMap.parent_id)
        .where(
            Studies.condition_cui.in_(_condition_cuis(condition_cuis)),
            Sigs.class_field == Sigs_Class_fieldEnum.RAD_SIG,
            Sigs.regimen == "Radiation therapy",
            Sigs.variant_cui.is_(None),
        )
        .distinct()
    )


def find_standalone_radiation_sigs(
    session: Session,
    condition_cuis: Iterable[int],
) -> list[Sigs]:
    """Execute :func:`standalone_radiation_sig_statement`."""
    return list(
        session.execute(standalone_radiation_sig_statement(condition_cuis)).scalars()
    )


def find_studies_with_standalone_radiation_sigs(
    session: Session,
    condition_cuis: Iterable[int],
) -> list[int]:
    """Execute the standalone-radiation study-ID query."""
    return list(
        session.execute(
            studies_with_standalone_radiation_sigs_statement(condition_cuis)
        ).scalars()
    )
