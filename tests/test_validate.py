"""Regression test for compiler/validate.py's normalisation-group invariant
(review follow-up): a repeated column within a group, or a column spread
across more than one group, means table_class() would render malformed or
ambiguous exploded map tables -- CONFIRMED in the real generated
entities.py as `['atc', 'atc']` before schema_model.py's dedup-ordering fix.
"""

from __future__ import annotations

import pytest

from hemonc_alchemy.compiler.schema_model import NormalisationGroup, Registry, TableMeta
from hemonc_alchemy.compiler.validate import validate_registry


def _table(**overrides) -> TableMeta:
    base = {
        "name": "drugs", "description": "d", "kind": "content", "maturity": "prod",
        "pk_columns": [], "columns": {"atc": object()},
    }
    base.update(overrides)
    return TableMeta(**base)


class TestNormalisationGroupInvariant:
    def test_self_pair_group_is_rejected(self):
        table = _table()
        table.normalisation_groups = [NormalisationGroup(columns=["atc", "atc"])]
        errors = validate_registry(Registry(tables={"drugs": table}))
        assert any("repeats a column" in e for e in errors)

    def test_column_in_two_groups_is_rejected(self):
        table = _table()
        table.normalisation_groups = [
            NormalisationGroup(columns=["atc", "atc_class"]),
            NormalisationGroup(columns=["atc", "atc_code"]),
        ]
        errors = validate_registry(Registry(tables={"drugs": table}))
        assert any("appears in 2 normalisation groups" in e for e in errors)

    def test_clean_groups_pass(self):
        table = _table()
        table.normalisation_groups = [NormalisationGroup(columns=["atc_class", "atc_code"])]
        assert validate_registry(Registry(tables={"drugs": table})) == []


if __name__ == "__main__":
    pytest.main([__file__])
