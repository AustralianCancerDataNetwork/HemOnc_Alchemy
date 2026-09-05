"""Contract tests for the model-facing toolkit query APIs."""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from hemonc_alchemy.toolkit.analytics.treatment.filters import (
    standalone_radiation_sig_statement,
)
from hemonc_alchemy.toolkit.analytics.treatment.selection import (
    CategoryRequirement,
    ComponentRequirement,
    TreatmentSelectionSpec,
    build_variant_statement,
)
from hemonc_alchemy.toolkit.core.conditions import condition_cui_statement
from hemonc_alchemy.toolkit.core.links import sig_study_tokens


def _sql(statement: sa.Select) -> str:
    return str(
        statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


def test_condition_lookup_is_composable_and_exact():
    sql = _sql(condition_cui_statement("Acute myeloid leukemia"))

    assert 'conditions.condition IN (\'Acute myeloid leukemia\')' in sql


def test_standalone_radiation_filter_uses_normalized_study_links():
    sql = _sql(standalone_radiation_sig_statement([123]))

    assert "JOIN sigs_study ON sigs_study.parent_id = sigs.id" in sql
    assert "sigs.class_field = 'RAD_SIG'" in sql
    assert "sigs.variant_cui IS NULL" in sql


def test_variant_selection_ranks_versions_and_normalizes_phase():
    spec = TreatmentSelectionSpec.for_conditions(
        [123],
        component_requirements=(ComponentRequirement.from_terms("cisplatin"),),
        category_requirements=(CategoryRequirement("cytotoxic", 1),),
        phase="adjuvant",
    )
    sql = _sql(build_variant_statement(spec))

    assert "row_number() OVER (PARTITION BY variants.variant_cui" in sql
    assert "variants_study.parent_id = variants.id" in sql
    assert "sigs.phase = 'ADJUVANT'" in sql
    assert "count(DISTINCT categorized_components.sig_id)" in sql


def test_sig_study_tokens_reads_current_normalized_map_rows():
    class StudyLink:
        def __init__(self, study: str):
            self.study = study

    class Sig:
        def __init__(self):
            self.study_items = [
                StudyLink("NCT-1"),
                StudyLink("NCT-2"),
                StudyLink("NCT-1"),
            ]

    assert sig_study_tokens(Sig()) == ["NCT-1", "NCT-2"]


def test_unknown_phase_fails_at_statement_boundary():
    spec = TreatmentSelectionSpec.for_conditions([123], phase="not-a-phase")

    try:
        build_variant_statement(spec)
    except ValueError as exc:
        assert str(exc) == "Unknown sig phase: 'not-a-phase'"
    else:
        raise AssertionError("an unknown generated enum value must be rejected")
