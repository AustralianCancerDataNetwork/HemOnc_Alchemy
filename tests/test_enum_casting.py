"""Proves US-22 (enum-from-CSV casting) is closed via composition, using
`orm-loader`'s new per-column cast-rule hook rather than reimplementing
casting logic here.

`orm_loader.loaders.data.converters.perform_cast` has no `CastRule` for
`sa.Enum` at all -- confirmed in `test_casting.py` -- because `sa.Enum` is
itself a subclass of `sa.String`, so an unrecognised value used to pass
straight through as a plain string instead of being caught (silently wrong
on SQLite; an immediate `InvalidTextRepresentation` on Postgres, whose
native enum type rejects it). `register_enum_casts` (`model/base.py`)
closes this by registering a validating rule for every generated `sa.Enum`
column via `orm_loader.loaders.data.converters.register_column_cast_rule`
(https://github.com/AustralianCancerDataNetwork/orm-loader/issues/36).

The one non-obvious piece this suite exists to prove: `compiler/schema_model.py`'s
`EnumSpec.enum_class` builds every member's `.value` from `v.strip().lower()`
(the same mechanism behind enum-collision warnings during `regen`, collapsing
case-only near-duplicates), but real CSV data keeps its original casing.
A first attempt at `register_enum_casts` used `register_column_cast_rule`'s
`enum_type=` shortcut directly (an exact-match lookup) and failed on *every*
real row of `canonicaltriples.class_1` -- not an edge case, 199/199 -- because
none of the real "Procedure"/"Regimen"-cased values matched the generated
lowercase members at all. `register_enum_casts` instead applies the identical
`.strip().lower()` before matching, so casting agrees with what the compiler
actually generated.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so

from hemonc_alchemy.model.base import Base, register_enum_casts
from hemonc_alchemy.model.entities import Canonicaltriples, Drugs
from hemonc_alchemy.model.enums import (
    Canonicaltriples_Class_1Enum,
    Drugs_Class_typeEnum,
)
from hemonc_alchemy.toolbox.loading import load_entity

_REAL_DATA_DIR = Path("/Users/georgie/Documents/unsw/sidequest/hemonc_import/hemonc_import/data")

pytestmark = pytest.mark.skipif(
    len(Base.metadata.tables) == 0,
    reason="model/entities.py has no generated classes yet -- run `hemonc-alchemy regen` first",
)


class TestRegisterEnumCasts:
    def test_discovers_real_enum_columns_across_the_whole_model(self):
        from orm_loader.loaders.data.converters import _COLUMN_CAST_RULES

        register_enum_casts()

        assert ("canonicaltriples", "class_1") in _COLUMN_CAST_RULES
        assert ("drugs", "class_type") in _COLUMN_CAST_RULES
        # A generated map/denormalised table with its own sa.Enum value column
        assert ("indications_biomarker2", "biomarker2") in _COLUMN_CAST_RULES

    def test_matches_case_insensitively_like_the_compiler_does(self):
        from orm_loader.loaders.data.converters import _COLUMN_CAST_RULES

        register_enum_casts()
        rule = _COLUMN_CAST_RULES[("canonicaltriples", "class_1")]

        # Real source casing ("Procedure"), not the generated lowercase member value
        assert rule("Procedure") == "PROCEDURE"
        assert rule("  Regimen  ") == "REGIMEN"

    def test_unmatched_value_raises_for_the_caller_to_handle(self):
        from orm_loader.loaders.data.converters import _COLUMN_CAST_RULES

        register_enum_casts()
        rule = _COLUMN_CAST_RULES[("canonicaltriples", "class_1")]

        with pytest.raises(ValueError):
            rule("not a real class")


@pytest.fixture
def sqlite_session():
    engine = sa.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine, tables=[Canonicaltriples.__table__])
    with so.Session(engine) as s:
        yield s


class TestLoadEntityEndToEnd:
    def test_real_lookup_table_enum_column_casts_correctly(self, sqlite_session):
        # Canonicaltriples has no surrogate id, so this runs cleanly on
        # SQLite (the surrogate-PK autoincrement limitation doesn't apply).
        total = load_entity(sqlite_session, Canonicaltriples, _REAL_DATA_DIR)
        sqlite_session.commit()

        assert total == 199
        rows = sqlite_session.execute(sa.select(Canonicaltriples.class_1)).scalars().all()
        assert len(rows) == 199
        assert all(isinstance(v, Canonicaltriples_Class_1Enum) for v in rows)
        # Confirms real, differently-cased source values ("Procedure") did
        # resolve, not just that nothing crashed.
        assert Canonicaltriples_Class_1Enum.PROCEDURE in rows
        assert Canonicaltriples_Class_1Enum.REGIMEN in rows

    def test_unknown_value_is_dropped_not_crashed(self, sqlite_session, tmp_path):
        csv_path = tmp_path / "canonicaltriples.csv"
        csv_path.write_text(
            "class_1,relationship,class_2,date_added,index,internal,used_in\n"
            "Procedure,is_a,thing,2020-01-01,1,0,x\n"
            "BOGUS_CLASS,is_a,other,2020-01-01,2,0,y\n"
            "Regimen,is_a,third,2020-01-01,3,0,z\n"
        )

        register_enum_casts()
        total = Canonicaltriples.load_csv(sqlite_session, csv_path)
        sqlite_session.commit()

        assert total == 2
        rows = sqlite_session.execute(sa.select(Canonicaltriples.class_1)).scalars().all()
        assert set(rows) == {Canonicaltriples_Class_1Enum.PROCEDURE, Canonicaltriples_Class_1Enum.REGIMEN}


@pytest.mark.postgres
class TestSurrogatePkEnumColumn:
    """`Drugs` is a surrogate-PK ("content") table with a nullable sa.Enum
    column (`class_type`) -- needs real Postgres, same as the rest of the
    surrogate-PK loading story (see test_loading.py).
    """

    def test_nullable_enum_column_casts_correctly_on_real_postgres(self, pg_session):
        with pg_session.get_bind().begin() as conn:
            conn.execute(sa.text('DROP TABLE IF EXISTS "drugs" CASCADE'))
        Base.metadata.create_all(pg_session.get_bind(), tables=[Drugs.__table__])

        total = load_entity(pg_session, Drugs, _REAL_DATA_DIR)
        pg_session.commit()

        assert total > 0
        rows = pg_session.execute(sa.select(Drugs.class_type)).scalars().all()
        assert all(v is None or isinstance(v, Drugs_Class_typeEnum) for v in rows)
        assert any(v == Drugs_Class_typeEnum.MECHANISTIC for v in rows)
        assert any(v is None for v in rows)  # real source data has some blank class_type rows


if __name__ == "__main__":
    pytest.main([__file__])
