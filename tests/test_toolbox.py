"""Functional tests for toolbox/classification.py and model/relationships.py,
exercised against real ORM inserts on a live in-memory SQLite database --
not just "does it import"/"does configure_mappers() succeed". These
specifically catch the class of bug found while porting this module: a
declared relationship or a toolbox function that's syntactically fine but
resolves to the wrong rows (or, as with the original's dead
`variant.study_objects` reference, an attribute that was never actually
defined at all).
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so

from hemonc_alchemy.model.base import Base
from hemonc_alchemy.model.entities import Sigs, Variants
from hemonc_alchemy.toolbox import (
    has_non_radiation_sig,
    has_radiation_sig,
    is_concurrent_chemort,
    is_rt_only,
)

pytestmark = pytest.mark.skipif(
    len(Base.metadata.tables) == 0,
    reason="model/entities.py has no generated classes yet -- run `hemonc-alchemy regen` first",
)


@pytest.fixture
def session():
    engine = sa.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with so.Session(engine) as s:
        yield s


def _make_variant(session, variant_cui: int) -> Variants:
    variant = Variants(
        id=variant_cui,
        variant_cui=variant_cui,
        variant=f"variant-{variant_cui}",
        regimen_cui=1,
        regimen="R",
        version=1,
        cyclesigs=0,
        components=0,
        portions=0,
        branches=0,
        routes=0,
        sigs=0,
        timings=0,
        blob_version=0,
        fullyspecified=True,
        allsigshavecyclesigs=True,
        allsigshavedose=True,
        allsigshavedoseunit=True,
        allsigshaveduration=True,
        allsigshavedurationunit=True,
        allsigshavefrequency=True,
        allsigshaveroute=True,
        allsigshaveschedule=True,
        allsigshavesequence=True,
        date_added=datetime(2020, 1, 1, tzinfo=UTC),
    )
    session.add(variant)
    session.flush()
    return variant


def _make_sig(session, *, variant_cui: int, component_cui: int, class_field: str, component_role: str) -> Sigs:
    sig = Sigs(
        id=component_cui,
        variant_cui=variant_cui,
        component_cui=component_cui,
        class_field=class_field,
        component_role=component_role,
        branch="A",
        component=f"drug-{component_cui}",
        portion="1",
        regimen="R",
        regimen_cui=1,
        step_number="1",
        variant=f"variant-{variant_cui}",
        date_added=datetime(2020, 1, 1, tzinfo=UTC),
    )
    session.add(sig)
    session.flush()
    return sig


class TestClassificationAgainstRealJoins:
    """Sigs<->Variants join via Sigs.variant_cui == Variants.variant_cui --
    the exact join that used to require a manual int() cast because of the
    Float/BigInteger/String mismatch (US-18)."""

    def test_rad_sig_only_is_rt_only(self, session):
        variant = _make_variant(session, variant_cui=100)
        _make_sig(
            session,
            variant_cui=100,
            component_cui=1,
            class_field="rad sig",
            component_role="locoregional",
        )
        session.expire_all()

        assert has_radiation_sig(variant) is True
        assert has_non_radiation_sig(variant) is False
        assert is_rt_only(variant) is True
        assert is_concurrent_chemort(variant) is False

    def test_mixed_sigs_is_concurrent_chemort(self, session):
        variant = _make_variant(session, variant_cui=200)
        _make_sig(
            session,
            variant_cui=200,
            component_cui=2,
            class_field="rad sig",
            component_role="locoregional",
        )
        _make_sig(
            session,
            variant_cui=200,
            component_cui=3,
            class_field="iv intermittent canonical sig",
            component_role="primary systemic",
        )
        session.expire_all()

        assert has_radiation_sig(variant) is True
        assert has_non_radiation_sig(variant) is True
        assert is_concurrent_chemort(variant) is True
        assert is_rt_only(variant) is False

    def test_no_sigs_classifies_as_neither(self, session):
        variant = _make_variant(session, variant_cui=300)
        session.expire_all()

        assert has_radiation_sig(variant) is False
        assert has_non_radiation_sig(variant) is False
        assert is_rt_only(variant) is False
        assert is_concurrent_chemort(variant) is False

    def test_component_sigs_join_finds_only_matching_variant(self, session):
        # Confirms the join is scoped correctly -- a sig on a *different*
        # variant_cui must not show up.
        v1 = _make_variant(session, variant_cui=400)
        _make_variant(session, variant_cui=401)
        _make_sig(session, variant_cui=400, component_cui=4, class_field="rad sig", component_role="locoregional")
        _make_sig(
            session, variant_cui=401, component_cui=5, class_field="rad sig", component_role="locoregional"
        )
        session.expire_all()

        assert len(v1.component_sigs) == 1
        assert v1.component_sigs[0].component_cui == 4
