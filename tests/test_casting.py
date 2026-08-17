"""Proves US-20 (reuse orm-loader's type casting) is satisfied by composition
alone -- no casting code needed in model/base.py for non-enum types.

`EntityBase` already composes `orm_loader.tables.CSVLoadableTableInterface`,
whose `load_csv()` delegates scalar casting to `PandasLoader.cast_to_model()`,
which calls `orm_loader.loaders.data.converters.perform_cast()` per column
and records failures on a `TableCastingStats` object rather than silently
substituting a sentinel value.

Two levels of proof:
- `TestPerformCastDirectly` exercises `perform_cast`/`TableCastingStats`
  directly, matching exactly what `PandasLoader.cast_to_model` does
  internally -- the mechanism the AC describes ("cast failures are
  counted/logged per column; no magic sentinel defaults").
- `TestLoadCsvEndToEnd` proves it end-to-end through a real generated
  entity class's own `load_csv()`, against a real (if small) CSV, on a
  real SQLite database -- a bad value in a nullable column comes back as
  NULL, not a `-1`/`-1.0` sentinel, and the row still loads.

  This end-to-end path was blocked on its first run by an unrelated bug
  this test caught: every generated entity class used to render its own
  `pk_columns` class attribute (a plain list of natural-key column
  names), which shadowed `orm_loader.tables.ORMTableBase.pk_columns()`
  -- a same-named method `merge_from_staging()` calls internally.
  `cls.pk_columns()` tried to call a list. Confirmed independent of
  casting itself (the CAST warning log line fired correctly before the
  crash). Fixed by renaming the generated attribute to
  `natural_key_columns` (compiler/schema_model.py's `table_class()`);
  `TableMeta.pk_columns`, the compiler's own internal field, is
  unrelated and unchanged.

`Units` is the entity used throughout: a simple lookup table (no surrogate
`id`, no FK, no denormalised columns) with one nullable BigInteger column
(`concept_code`) that's a clean target for a bad-value test, independent
of `unit_type`'s Enum casting -- that's US-22, covered separately in
`test_enum_casting.py` now that it's built.
"""

from __future__ import annotations

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from orm_loader.loaders.data.converters import perform_cast
from orm_loader.loaders.data_classes import TableCastingStats

from hemonc_alchemy.model.base import Base
from hemonc_alchemy.model.entities import Units

pytestmark = pytest.mark.skipif(
    len(Base.metadata.tables) == 0,
    reason="model/entities.py has no generated classes yet -- run `hemonc-alchemy regen` first",
)


class TestPerformCastDirectly:
    def test_bad_value_is_recorded_not_defaulted(self):
        stats = TableCastingStats(table_name="units")
        col_type = Units.__table__.c.concept_code.type

        result = perform_cast(
            "not-a-number",
            col_type,
            on_error=lambda value: stats.record(column="concept_code", value=value),
        )

        assert result is None
        assert stats.has_failures()
        assert stats.total_failures == 1
        assert stats.columns["concept_code"].examples == ["not-a-number"]

    def test_good_value_casts_cleanly_with_no_failures(self):
        stats = TableCastingStats(table_name="units")
        col_type = Units.__table__.c.concept_code.type

        result = perform_cast(
            "134444",
            col_type,
            on_error=lambda value: stats.record(column="concept_code", value=value),
        )

        assert result == 134444
        assert not stats.has_failures()


@pytest.fixture
def session():
    engine = sa.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine, tables=[Units.__table__])
    with so.Session(engine) as s:
        yield s


class TestLoadCsvEndToEnd:
    def test_bad_concept_code_becomes_null_not_sentinel(self, session, tmp_path):
        csv_path = tmp_path / "units.csv"
        csv_path.write_text(
            "unit,unit_type,concept_code,date_added\n"
            "mg,UNITS_PER_VOLUME,134444,2020-01-01\n"
            "bad_unit,UNITS_PER_VOLUME,not-a-number,2020-01-01\n"
        )

        total = Units.load_csv(session, csv_path)
        assert total == 2

        rows = {row.unit: row.concept_code for row in session.execute(sa.select(Units)).scalars()}
        assert rows["mg"] == 134444
        assert rows["bad_unit"] is None
        assert -1 not in rows.values()


if __name__ == "__main__":
    pytest.main([__file__])
