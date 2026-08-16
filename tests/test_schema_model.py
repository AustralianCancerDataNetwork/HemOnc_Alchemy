"""Regression tests for compiler/schema_model.py's review-follow-up fixes:
denormalised-column dedup ordering, registry.json round-tripping of soft
relationships, and enum-collision detection.
"""

from __future__ import annotations

import pandas as pd
import pytest

from hemonc_alchemy.compiler.audit import enum_collision_warnings
from hemonc_alchemy.compiler.schema_model import (
    EnumSpec,
    ForeignLikeRef,
    Registry,
    SoftManyToManyRef,
    TableMeta,
    load_registry_json,
    save_registry_json,
)


class TestDenormalisedColumnDedup:
    """`finalise_from_data` must dedupe `denormalised_columns` before calling
    `infer_pipe_groups`, not after -- CONFIRMED in the real generated
    entities.py: `Drugs.normalisation_groups` contained a malformed
    `['atc', 'atc']` self-pair even though `Drugs.denormalised_columns`
    itself came out clean (deduped too late to matter for inference).
    """

    def test_pre_existing_duplicate_does_not_produce_self_pair_group(self):
        meta = TableMeta(
            name="drugs",
            description="",
            kind="content",
            maturity="prod",
            pk_columns=["drug_cui"],
        )
        # Simulate the dictionary-driven pass (enrich_field_metadata) having
        # already appended 'atc' once before the data-driven pass runs.
        meta.denormalised_columns = ["atc"]

        df = pd.DataFrame(
            {
                "drug_cui": [1, 2, 3],
                "atc": ["A01|A02", "B01", "C01|C02|C03"],
            }
        )
        meta.finalise_from_data(df)

        assert meta.denormalised_columns == ["atc"]
        for group in meta.normalisation_groups:
            assert len(group.columns) == len(set(group.columns)), f"malformed self-pair: {group.columns}"


class TestTableMetaRoundTrip:
    """TableMeta.from_dict must round-trip everything save_registry_json
    writes -- CONFIRMED the checked-in registry.json has 18 soft
    relationships that silently became 0 after a load_registry_json
    round-trip, which is what compiler/diff.py and compiler/audit.py both
    operate on.
    """

    def test_soft_relationships_and_use_surrogate_pk_survive_round_trip(self, tmp_path):
        table = TableMeta(
            name="sigs",
            description="d",
            kind="content",
            maturity="prod",
            pk_columns=["sig_cui"],
            use_surrogate_pk=False,
        )
        table.soft_relationships = [ForeignLikeRef(local_column="drug_cui", target_table="drugs", target_column="drug_cui")]
        table.soft_m2m_relationships = [
            SoftManyToManyRef(
                local_table="sigs", map_table="sigs_route", map_column="route_cui",
                target_table="routes", target_column="route_cui",
            )
        ]
        registry = Registry(tables={"sigs": table})

        path = tmp_path / "registry.json"
        save_registry_json(registry, path)
        loaded = load_registry_json(path)

        loaded_table = loaded.tables["sigs"]
        assert loaded_table.use_surrogate_pk is False
        assert len(loaded_table.soft_relationships) == 1
        assert loaded_table.soft_relationships[0].target_table == "drugs"
        assert len(loaded_table.soft_m2m_relationships) == 1
        assert loaded_table.soft_m2m_relationships[0].map_table == "sigs_route"

    def test_defaults_when_fields_absent_from_older_snapshot(self):
        # A registry.json written before these fields existed shouldn't fail
        # to load.
        raw = {
            "name": "drugs", "description": "d", "kind": "content", "maturity": "prod",
            "pk_columns": ["drug_cui"], "columns": {},
        }
        table = TableMeta.from_dict(raw)
        assert table.soft_relationships == []
        assert table.soft_m2m_relationships == []
        assert table.use_surrogate_pk is True


class TestEnumCollisionWarnings:
    """CONFIRMED against real data: sigs/indications' `targetleveltype`-style
    columns have both 'CPS at least 10%' and 'CPS at least 10', which both
    normalise to the same `safe_enum_key`. Should warn, not fail (the two
    values are the same real-world category here) -- and stay silent when
    there's no collision.
    """

    def test_warns_on_colliding_enum_values(self):
        table = TableMeta(
            name="indications", description="", kind="content", maturity="prod", pk_columns=[],
        )
        table.enums = {
            "biomarker4_finding": EnumSpec(
                name="biomarker4_finding", tablename="indications",
                values=["CPS at least 10%", "CPS at least 10"],
            )
        }
        registry = Registry(tables={"indications": table})
        warnings = enum_collision_warnings(registry)
        assert len(warnings) == 1
        assert "indications.biomarker4_finding" in warnings[0]

    def test_no_warning_without_collision(self):
        table = TableMeta(
            name="indications", description="", kind="content", maturity="prod", pk_columns=[],
        )
        table.enums = {
            "biomarker4_finding": EnumSpec(
                name="biomarker4_finding", tablename="indications",
                values=["Positive", "Negative"],
            )
        }
        registry = Registry(tables={"indications": table})
        assert enum_collision_warnings(registry) == []


if __name__ == "__main__":
    pytest.main([__file__])
