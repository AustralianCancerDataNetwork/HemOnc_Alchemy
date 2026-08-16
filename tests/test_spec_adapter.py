"""Tests for compiler/spec_adapter.py (US-21).

Two levels: unit tests against synthetic TableMeta (no regen required), and
an end-to-end run of orm_loader's always-on validators against the real
generated model -- the same check `hemonc-alchemy validate` runs, kept as a
permanent regression test rather than only an ad hoc CLI check.

That end-to-end run is what caught a real bug while building this module:
every generated map/child table's value column was declared
`primary_key=True` but nullable (`Optional[...]`, no `nullable=False`) --
`ColumnSpec.sa_python_type`/`normalised_table_class` computed nullability
relative to the *parent* table's key, not the map table's own composite
key. Fixed in compiler/schema_model.py; this test would fail again if that
regressed.
"""

from __future__ import annotations

import pytest

from hemonc_alchemy.compiler.schema_model import ColumnSpec, Registry, TableMeta
from hemonc_alchemy.compiler.spec_adapter import (
    hemonc_field_specs,
    hemonc_table_specs,
    validate_with_orm_loader,
)


def _toy_registry() -> Registry:
    content = TableMeta(
        name="widgets",
        description="Test table",
        kind="content",
        maturity="prod",
        pk_columns=["widget_cui"],
        columns={
            "widget_cui": ColumnSpec(name="widget_cui", type="Integer", nullable=False),
            "name": ColumnSpec(name="name", type="String(255)", nullable=True),
        },
    )
    lookup = TableMeta(
        name="units",
        description="Lookup table",
        kind="lookup",
        maturity="prod",
        pk_columns=["unit"],
        columns={"unit": ColumnSpec(name="unit", type="String(50)", nullable=False)},
        use_surrogate_pk=False,
    )
    empty = TableMeta(
        name="no_data",
        description="No backing data -- should be excluded entirely",
        kind="lookup",
        maturity="dev",
        pk_columns=[],
        columns={},
    )
    return Registry(tables={"widgets": content, "units": lookup, "no_data": empty})


class TestHemoncTableSpecs:
    def test_only_tables_with_columns_get_a_spec(self):
        specs = hemonc_table_specs(_toy_registry())
        assert set(specs) == {"widgets", "units"}

    def test_is_required_mirrors_prod_maturity(self):
        specs = hemonc_table_specs(_toy_registry())
        assert specs["widgets"].is_required is True

    def test_dev_maturity_is_not_required(self):
        registry = _toy_registry()
        registry.tables["widgets"] = TableMeta(**{**vars(registry.tables["widgets"]), "maturity": "dev"})
        specs = hemonc_table_specs(registry)
        assert specs["widgets"].is_required is False


class TestHemoncFieldSpecs:
    def test_surrogate_pk_table_marks_id_not_natural_key(self):
        fields = hemonc_field_specs(_toy_registry())["widgets"]
        assert fields["id"].is_primary_key is True
        # widget_cui is the natural/business key, not the real generated PK
        # (that's a UniqueConstraint, not primary_key=True) -- marking it
        # as a spec PK would make PrimaryKeyValidator flag every content
        # table's natural key as PRIMARY_KEY_MISSING_FROM_MODEL.
        assert fields["widget_cui"].is_primary_key is False

    def test_non_surrogate_table_marks_natural_key_as_pk(self):
        fields = hemonc_field_specs(_toy_registry())["units"]
        assert fields["unit"].is_primary_key is True
        assert "id" not in fields

    def test_empty_table_excluded(self):
        fields = hemonc_field_specs(_toy_registry())
        assert "no_data" not in fields


class TestValidateWithOrmLoader:
    """End-to-end against the real generated model."""

    def test_generated_model_has_no_validation_errors(self):
        try:
            from hemonc_alchemy.model import entities
            from hemonc_alchemy.model.base import concrete_entities
        except ImportError:
            pytest.skip("model/entities.py has no generated classes yet")

        models = concrete_entities(entities)
        if not models:
            pytest.skip("model/entities.py has no generated classes yet -- run `hemonc-alchemy regen` first")

        from pathlib import Path

        from hemonc_alchemy.compiler.schema_model import load_registry_json

        registry_path = Path(__file__).parent.parent / "hemonc_alchemy" / "schema" / "registry.json"
        if not registry_path.exists():
            pytest.skip("no registry.json -- run `hemonc-alchemy regen` first")

        registry = load_registry_json(registry_path)
        report = validate_with_orm_loader(registry, models)

        assert report.exit_code() == 0, report.render_text_report()
