"""A bad value in the extract must become NULL or drop the row, never a
sentinel like -1 that would read as real data.

Casting is orm-loader's, not ours; these tests hold the guarantee at both
levels -- the cast function directly, and a real entity's load end to end.

Two levels of proof:
- `TestPerformCastDirectly` exercises `perform_cast`/`TableCastingStats`
  directly, matching exactly what `PandasLoader.cast_to_model` does
  internally -- the mechanism the AC describes ("cast failures are
  counted/logged per column; no magic sentinel defaults").
- `TestLoadCsvEndToEnd` proves it end-to-end through a real generated
  entity class's own `load_csv()`, against a real (if small) CSV, on a
  real SQLite database -- a bad value in a nullable column comes back as
  NULL, not a `-1`/`-1.0` sentinel, and the row still loads. The
  complementary case is covered too: in a non-nullable column the loader
  drops the row rather than inventing a value to satisfy the constraint.

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

`Units` covers the direct-cast and non-nullable cases: a simple lookup
table (no surrogate `id`, no FK, no denormalised columns). It was the whole
suite's subject until the 2026-08 drop made every one of its columns
non-nullable, at which point a bad `concept_code` stopped being a NULL and
became a dropped row. `Regimens.first_studied` (nullable Integer) carries
the null-not-sentinel case now. Enum casting is , covered separately in
`test_enum_casting.py`.
"""

from __future__ import annotations

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from orm_loader.loaders.data.converters import perform_cast
from orm_loader.loaders.data_classes import TableCastingStats

from hemonc_alchemy.model.base import Base
from hemonc_alchemy.model.entities import Regimens, Units

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
    Base.metadata.create_all(engine, tables=[Units.__table__, Regimens.__table__])
    with so.Session(engine) as s:
        yield s


class TestLoadCsvEndToEnd:
    """`Regimens.first_studied` (nullable Integer) is the end-to-end target.

    This used `Units.concept_code` until the 2026-08 drop made every Units
    column non-nullable -- a bad value there is now a rejected row rather
    than a NULL, which tests a different property. Both are checked below.
    """

    # `id` is the generated surrogate PK for a content table; BigInteger
    # doesn't autoincrement on SQLite, so the CSV supplies it.
    _REQUIRED = (
        "id,regimen_cui,regimen_name,regimen_type,highest_evidence,sact,contains_rt,"
        "studies,variantcount,variantcountdate,date_added"
    )
    # sa.Enum columns store the member *name*; this suite deliberately does
    # not register_enum_casts() -- value-to-member casting is , in
    # test_enum_casting.py. The target column here is a plain Integer.
    _FIXED = "NULL_REGIMEN,PHASE_3_RCT,FALSE,FALSE,0,0,2020-01-01,2020-01-01"

    def test_bad_nullable_number_becomes_null_not_sentinel(self, session, tmp_path):
        csv_path = tmp_path / "regimens.csv"
        csv_path.write_text(
            f"{self._REQUIRED},first_studied\n"
            f"1,1,good,{self._FIXED},1998\n"
            f"2,2,bad,{self._FIXED},not-a-number\n"
        )

        total = Regimens.load_csv(session, csv_path)
        assert total == 2

        rows = {
            row.regimen_name: row.first_studied
            for row in session.execute(sa.select(Regimens)).scalars()
        }
        assert rows["good"] == 1998
        assert rows["bad"] is None
        assert -1 not in rows.values()
        assert -1.0 not in rows.values()

    def test_bad_value_in_a_non_nullable_column_drops_the_row(self, session, tmp_path):
        """The complementary guarantee: where NULL isn't allowed, the loader
        refuses the row rather than inventing a sentinel to satisfy it.
        """
        csv_path = tmp_path / "units.csv"
        csv_path.write_text(
            "unit,unit_type,concept_code,date_added,fixed,parameterbased,timebased\n"
            "mg,UNITS_PER_VOLUME,134444,2020-01-01,TRUE,FALSE,FALSE\n"
            "bad_unit,UNITS_PER_VOLUME,not-a-number,2020-01-01,TRUE,FALSE,FALSE\n"
        )

        total = Units.load_csv(session, csv_path)
        assert total == 1

        rows = {row.unit: row.concept_code for row in session.execute(sa.select(Units)).scalars()}
        assert rows == {"mg": 134444}
        assert "bad_unit" not in rows


if __name__ == "__main__":
    pytest.main([__file__])
