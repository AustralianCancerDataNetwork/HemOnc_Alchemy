"""Schedule summaries, against real rows in a real database.

These went unexercised for long enough to silently break -- the module read a
`sigs.branch` column that had been dropped upstream -- so they are tested
through real inserts and real relationship traversal rather than stubs.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
import sqlalchemy as sa
import sqlalchemy.event
import sqlalchemy.orm as so

from hemonc_alchemy.model.base import Base
from hemonc_alchemy.model.entities import Drugs, Sigs, Variants
from hemonc_alchemy.toolkit.schedule import (
    administration_frame,
    administration_matrix,
    cancer_services_drugs,
    cancer_services_sigs_by_drug,
    home_administered_drugs,
    schedule_events,
)

pytestmark = pytest.mark.skipif(
    len(Base.metadata.tables) == 0,
    reason="model/entities.py has no generated classes yet -- run `hemonc-alchemy regen` first",
)

_D = datetime(2020, 1, 1, tzinfo=UTC)


@pytest.fixture
def session():
    engine = sa.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with so.Session(engine) as s:
        yield s


def _variant(session, variant_cui: int) -> Variants:
    variant = Variants(
        id=variant_cui, variant_cui=variant_cui, variant=f"v{variant_cui}",
        regimen_cui=1, regimen="R", version=1, cyclesigs=0, components=0, portions=0,
        routes=0, sigs=0, blob_version=0, fullyspecified=True,
        allsigshavecyclesigs=True, allsigshavedose=True, allsigshavedoseunit=True,
        allsigshaveduration=True, allsigshavedurationunit=True, allsigshavefrequency=True,
        allsigshaveroute=True, allsigshaveschedule=True, allsigshavesequence=True,
        date_added=_D,
    )
    session.add(variant)
    session.flush()
    return variant


def _drug(session, drug_cui: int, name: str) -> Drugs:
    drug = Drugs(
        id=drug_cui, drug_cui=drug_cui, drug=name,
        investigational=False, multiagent=False, date_added=_D,
    )
    session.add(drug)
    session.flush()
    return drug


def _sig(session, *, sig_id: int, variant_cui: int, drug_cui: int, route: str, alldays: str) -> Sigs:
    sig = Sigs(
        id=sig_id, variant_cui=variant_cui, component_cui=drug_cui, component=f"c{drug_cui}",
        class_field="iv intermittent canonical sig", component_role="primary systemic",
        portion="1", regimen="R", regimen_cui=1, step_number="1", divided=False,
        phase_step=1, variant=f"v{variant_cui}", route=route, alldays=alldays, date_added=_D,
    )
    session.add(sig)
    session.flush()
    return sig


class TestScheduleEvents:
    def test_one_event_per_sig_with_its_days_resolved(self, session):
        variant = _variant(session, 1)
        _drug(session, 1, "cisplatin")
        _sig(session, sig_id=1, variant_cui=1, drug_cui=1, route="INTRAVENOUS", alldays="1,8,15")
        session.expire_all()

        events = schedule_events(variant)
        assert len(events) == 1
        assert [day.value for day in events[0].days] == [1, 8, 15]
        assert events[0].route_group == "IV"
        assert events[0].drug_object.drug == "cisplatin"

    def test_an_indefinite_schedule_is_flagged_not_dropped(self, session):
        variant = _variant(session, 2)
        _drug(session, 1, "capecitabine")
        _sig(session, sig_id=1, variant_cui=2, drug_cui=1, route="ORAL", alldays="1,(+c)")
        session.expire_all()

        event = schedule_events(variant)[0]
        assert event.indefinite is not None
        assert [day.value for day in event.days] == [1]


class TestAdministrationFrame:
    def _nsclc_ish(self, session):
        variant = _variant(session, 10)
        _drug(session, 1, "carboplatin")
        _drug(session, 2, "etoposide")
        _sig(session, sig_id=1, variant_cui=10, drug_cui=1, route="INTRAVENOUS", alldays="1")
        _sig(session, sig_id=2, variant_cui=10, drug_cui=2, route="ORAL", alldays="1,2,3")
        session.expire_all()
        return variant

    def test_one_row_per_drug_per_day(self, session):
        frame = administration_frame(self._nsclc_ish(session), decay_days=0)
        assert list(frame.columns) == [
            "variant_cui", "variant", "route_group", "drug_cui", "drug",
            "day", "intensity", "optional", "indefinite",
        ]
        assert len(frame) == 4  # carboplatin d1, etoposide d1-3
        assert set(frame["route_group"]) == {"IV", "PO"}
        assert (frame["intensity"] == 1.0).all()

    def test_a_single_variant_is_not_iterated_into_its_columns(self, session):
        """Entities inherit __iter__ from orm-loader's serialisation
        interface, so a naive Iterable check treats one variant as a
        collection of its own column values."""
        frame = administration_frame(self._nsclc_ish(session))
        assert set(frame["variant_cui"]) == {10}

    def test_decay_tapers_after_each_dosing_day(self, session):
        frame = administration_frame(self._nsclc_ish(session), decay_days=2, decay_factor=0.5)
        carbo = frame[frame["drug"] == "carboplatin"].set_index("day")["intensity"]
        assert carbo.loc[1] == 1.0
        assert carbo.loc[2] == 0.5
        assert carbo.loc[3] == 0.25

    def test_carries_both_drug_identifier_and_name(self, session):
        """The original keyed its grid by display name, so two distinct drugs
        sharing one name merged into a single row."""
        frame = administration_frame(self._nsclc_ish(session))
        assert set(zip(frame["drug_cui"], frame["drug"])) == {
            (1, "carboplatin"), (2, "etoposide"),
        }

    def test_unclassified_route_is_excluded(self, session):
        variant = _variant(session, 20)
        _drug(session, 1, "something")
        _sig(session, sig_id=1, variant_cui=20, drug_cui=1, route="NS", alldays="1")
        session.expire_all()
        assert administration_frame(variant).empty

    def test_a_variant_with_no_resolvable_days_gives_an_empty_frame(self, session):
        """An `EOC` range has no known length, so it yields no explicit days --
        an empty frame, not an error."""
        variant = _variant(session, 30)
        _drug(session, 1, "something")
        _sig(session, sig_id=1, variant_cui=30, drug_cui=1, route="INTRAVENOUS", alldays="[1,EOC,7]")
        session.expire_all()

        frame = administration_frame(variant)
        assert frame.empty
        assert list(frame.columns)[:3] == ["variant_cui", "variant", "route_group"]

    def test_overlapping_sigs_for_one_drug_keep_the_strongest_day(self, session):
        """Two sigs can dose the same drug in one variant and their decay
        tails land on the same day."""
        variant = _variant(session, 40)
        _drug(session, 1, "fluorouracil")
        _sig(session, sig_id=1, variant_cui=40, drug_cui=1, route="INTRAVENOUS", alldays="1")
        _sig(session, sig_id=2, variant_cui=40, drug_cui=1, route="INTRAVENOUS", alldays="2")
        session.expire_all()

        frame = administration_frame(variant)
        day_2 = frame[frame["day"] == 2]
        assert len(day_2) == 1                 # not one row per sig
        assert day_2["intensity"].iloc[0] == 1.0   # dosing day beats the other's tail

    def test_many_variants_come_back_in_one_frame(self, session):
        _drug(session, 1, "cisplatin")
        for cui in (51, 52):
            _variant(session, cui)
            _sig(session, sig_id=cui, variant_cui=cui, drug_cui=1,
                 route="INTRAVENOUS", alldays="1")
        session.expire_all()

        variants = session.execute(sa.select(Variants)).scalars().all()
        frame = administration_frame(variants)
        assert set(frame["variant_cui"]) == {51, 52}
        assert len(frame.groupby("variant_cui")) == 2

    def test_the_functions_issue_no_queries_of_their_own(self, session):
        """Sigs and drugs are batch-loaded with the variants, so summarising
        them costs nothing further -- looping is no worse than batching."""
        _drug(session, 1, "cisplatin")
        for cui in (61, 62, 63):
            _variant(session, cui)
            _sig(session, sig_id=cui, variant_cui=cui, drug_cui=1,
                 route="INTRAVENOUS", alldays="1,8")
        session.commit()
        session.expire_all()

        seen: list[str] = []
        engine = session.get_bind()

        def record(conn, cursor, statement, parameters, context, executemany):
            seen.append(statement)

        sa.event.listen(engine, "before_cursor_execute", record)
        try:
            variants = session.execute(sa.select(Variants)).scalars().all()
            after_load = len(seen)
            administration_frame(variants)
            assert len(seen) == after_load
        finally:
            sa.event.remove(engine, "before_cursor_execute", record)


class TestAdministrationMatrix:
    def test_pivots_to_the_drug_by_day_grid(self, session):
        variant = _variant(session, 70)
        _drug(session, 1, "carboplatin")
        _sig(session, sig_id=1, variant_cui=70, drug_cui=1, route="INTRAVENOUS", alldays="1,8")
        session.expire_all()

        grid = administration_matrix(administration_frame(variant, decay_days=0))
        assert list(grid.index) == ["carboplatin"]
        assert list(grid.columns) == [1, 8]
        assert grid.loc["carboplatin", 8] == 1.0

    def test_a_route_with_no_rows_gives_an_empty_grid(self, session):
        variant = _variant(session, 80)
        _drug(session, 1, "capecitabine")
        _sig(session, sig_id=1, variant_cui=80, drug_cui=1, route="ORAL", alldays="1")
        session.expire_all()

        frame = administration_frame(variant)
        assert administration_matrix(frame, route="IV").empty
        assert not administration_matrix(frame, route="PO").empty


class TestRouteGroupedHelpers:
    def test_splits_drugs_by_where_they_are_given(self, session):
        variant = _variant(session, 90)
        _drug(session, 1, "carboplatin")
        _drug(session, 2, "etoposide")
        _sig(session, sig_id=1, variant_cui=90, drug_cui=1, route="INTRAVENOUS", alldays="1")
        _sig(session, sig_id=2, variant_cui=90, drug_cui=2, route="ORAL", alldays="1,2,3")
        session.expire_all()

        assert [d.drug for d in cancer_services_drugs(variant)] == ["carboplatin"]
        assert [d.drug for d in home_administered_drugs(variant)] == ["etoposide"]

    def test_sigs_grouped_by_drug(self, session):
        variant = _variant(session, 100)
        drug = _drug(session, 1, "cisplatin")
        _sig(session, sig_id=1, variant_cui=100, drug_cui=1, route="INTRAVENOUS", alldays="1")
        _sig(session, sig_id=2, variant_cui=100, drug_cui=1, route="INTRAVENOUS", alldays="8")
        session.expire_all()

        by_drug = cancer_services_sigs_by_drug(variant)
        assert list(by_drug) == [drug]
        assert len(by_drug[drug]) == 2


if __name__ == "__main__":
    pytest.main([__file__])
