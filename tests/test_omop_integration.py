"""Unit checks for the optional OMOP integration boundary."""

from __future__ import annotations

import pytest
import sqlalchemy as sa
from sqlalchemy.pool import StaticPool

from hemonc_alchemy.integrations.omop import (
    condition_to_snomed,
    coverage_report,
    drug_to_rxnorm_ingredient,
    load_omop_binding,
    map_to_standard,
    omop_available,
    resolve_hemonc_concepts,
    vocabulary_versions,
)


def _sqlite_omop_session():
    engine = sa.create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    metadata = sa.MetaData()
    concept = sa.Table(
        "concept", metadata,
        sa.Column("concept_id", sa.Integer, primary_key=True),
        sa.Column("concept_name", sa.String), sa.Column("domain_id", sa.String),
        sa.Column("vocabulary_id", sa.String), sa.Column("concept_class_id", sa.String),
        sa.Column("standard_concept", sa.String), sa.Column("concept_code", sa.String),
        sa.Column("valid_start_date", sa.Date), sa.Column("valid_end_date", sa.Date),
        sa.Column("invalid_reason", sa.String),
    )
    relationship = sa.Table(
        "concept_relationship", metadata,
        sa.Column("concept_id_1", sa.Integer), sa.Column("concept_id_2", sa.Integer),
        sa.Column("relationship_id", sa.String), sa.Column("valid_start_date", sa.Date),
        sa.Column("valid_end_date", sa.Date), sa.Column("invalid_reason", sa.String),
    )
    vocabulary = sa.Table(
        "vocabulary", metadata,
        sa.Column("vocabulary_id", sa.String, primary_key=True),
        sa.Column("vocabulary_name", sa.String), sa.Column("vocabulary_reference", sa.String),
        sa.Column("vocabulary_version", sa.String), sa.Column("vocabulary_concept_id", sa.Integer),
    )
    with engine.connect() as connection:
        metadata.create_all(connection)
        connection.execute(concept.insert(), [
            {"concept_id": 1, "concept_name": "Classical Hodgkin lymphoma", "domain_id": "Condition", "vocabulary_id": "HemOnc", "concept_class_id": "Condition", "concept_code": "614", "invalid_reason": None},
            {"concept_id": 2, "concept_name": "Hodgkin disease", "domain_id": "Condition", "vocabulary_id": "SNOMED", "concept_class_id": "Disorder", "standard_concept": "S", "concept_code": "118599009", "invalid_reason": None},
            {"concept_id": 3, "concept_name": "Cisplatin", "domain_id": "Drug", "vocabulary_id": "HemOnc", "concept_class_id": "Component", "concept_code": "105", "invalid_reason": None},
            {"concept_id": 4, "concept_name": "cisplatin", "domain_id": "Drug", "vocabulary_id": "RxNorm", "concept_class_id": "Ingredient", "standard_concept": "S", "concept_code": "2555", "invalid_reason": None},
            {"concept_id": 5, "concept_name": "Retired source", "domain_id": "Condition", "vocabulary_id": "HemOnc", "concept_class_id": "Condition", "concept_code": "999", "invalid_reason": "D"},
        ])
        connection.execute(relationship.insert(), [
            {"concept_id_1": 1, "concept_id_2": 2, "relationship_id": "Maps to"},
            {"concept_id_1": 3, "concept_id_2": 4, "relationship_id": "Maps to"},
            {"concept_id_1": 5, "concept_id_2": 2, "relationship_id": "Maps to"},
        ])
        connection.execute(vocabulary.insert(), [
            {"vocabulary_id": "HemOnc", "vocabulary_version": "test-hemonc"},
            {"vocabulary_id": "SNOMED", "vocabulary_version": "test-snomed"},
            {"vocabulary_id": "RxNorm", "vocabulary_version": "test-rxnorm"},
        ])
        connection.commit()
    return engine, sa.orm.Session(engine)


def test_absent_omop_is_a_noop():
    engine = sa.create_engine("sqlite://")
    session = sa.orm.Session(engine)
    assert not omop_available(session)
    assert resolve_hemonc_concepts(session, [614]) == []
    assert map_to_standard(session, [614]) == []
    session.close()
    engine.dispose()


def test_present_omop_preserves_identifiers_and_mapping_rows():
    if load_omop_binding() is None:
        pytest.skip("the optional omop extra is not installed")
    engine, session = _sqlite_omop_session()
    try:
        resolved = resolve_hemonc_concepts(session, [614])
        assert resolved[0].hemonc_cui == "614"
        assert resolved[0].concept.concept_id == 1
        condition = condition_to_snomed(session, [614])
        assert condition[0].target is not None
        assert condition[0].target.concept_id == 2
        drug = drug_to_rxnorm_ingredient(session, [105])
        assert drug[0].target is not None
        assert drug[0].target.concept_code == "2555"
        assert resolve_hemonc_concepts(session, [999]) == []
        report = coverage_report(session, [614, 999], target_vocabulary="SNOMED")
        assert report.requested_cuis == 2
        assert report.resolved_cuis == 1
        assert report.mapped_cuis == 1
        assert report.unmatched_cuis == ("999",)
        assert {v.vocabulary_id for v in vocabulary_versions(session)} == {"HemOnc", "SNOMED", "RxNorm"}
    finally:
        session.close()
        engine.dispose()
