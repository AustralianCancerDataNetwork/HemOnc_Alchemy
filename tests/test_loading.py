"""Proves the runtime primary-CSV loader (toolbox/loading.py) actually loads
real HemOnc data, including tables whose real filename doesn't match their
table name -- `load_csv()` (from orm-loader's `CSVLoadableTableInterface`,
already composed onto every entity) requires `path.stem == cls.__tablename__`
as a safety check, but HemOnc's own filenames don't always agree
(`canonical.triples.csv` for `canonicaltriples`). `toolbox.loading.load_entity`
resolves the real file via the same `naming.resolve_source_csv` the compiler
already uses, and satisfies the check with a throwaway symlink rather than
weakening it.

Run against the real data directory (skipped if it isn't present -- this
suite intentionally isn't fixture-driven, since the whole point is proving
the filename-mismatch fix against HemOnc's actual, irregular filenames, not
a synthetic stand-in for them).

Deliberately queries only non-enum columns: `canonicaltriples.class_1` is a
required Enum column, and orm_loader's `perform_cast` has no CastRule for
`sa.Enum` at all (confirmed in tests/test_casting.py) -- reading a loaded
row back through the ORM fails on enum hydration today. That's the
enum-from-CSV casting gap (US-22), tracked separately; this suite only
proves the primary-load/filename-resolution path, which is fully
independent of it (confirmed directly: the row lands in the table with the
right values -- the failure is read-side ORM hydration, not the load).
"""

from __future__ import annotations

from pathlib import Path

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so

from hemonc_alchemy.model.base import Base
from hemonc_alchemy.model.entities import Canonicaltriples, Units, Variants
from hemonc_alchemy.toolbox.loading import load_all, load_denormalised, load_entity

_REAL_DATA_DIR = Path("/Users/georgie/Documents/unsw/sidequest/hemonc_import/hemonc_import/data")

pytestmark = [
    pytest.mark.skipif(
        len(Base.metadata.tables) == 0,
        reason="model/entities.py has no generated classes yet -- run `hemonc-alchemy regen` first",
    ),
    pytest.mark.skipif(
        not _REAL_DATA_DIR.is_dir(),
        reason=f"real HemOnc data directory not found at {_REAL_DATA_DIR}",
    ),
]


@pytest.fixture
def session():
    engine = sa.create_engine("sqlite:///:memory:")
    with so.Session(engine) as s:
        yield s


class TestFilenameResolution:
    def test_loads_table_whose_real_filename_does_not_match_tablename(self, session):
        # canonicaltriples' real file is canonical.triples.csv -- confirms
        # this table has 0 entity classes silently missing data, which is
        # exactly the class of bug the compiler-side resolver was built for
        # (US-13); this proves the same fix applies at load time.
        Base.metadata.create_all(session.get_bind(), tables=[Canonicaltriples.__table__])

        total = load_entity(session, Canonicaltriples, _REAL_DATA_DIR)
        assert total > 0

        count = session.execute(sa.text("SELECT COUNT(*) FROM canonicaltriples")).scalar()
        assert count == total

        sample = session.execute(
            sa.text("SELECT class_1, relationship, class_2 FROM canonicaltriples LIMIT 1")
        ).first()
        assert sample is not None
        assert all(v for v in sample)

    def test_loads_table_whose_filename_already_matches(self, session):
        Base.metadata.create_all(session.get_bind(), tables=[Units.__table__])

        total = load_entity(session, Units, _REAL_DATA_DIR)
        assert total > 0

        count = session.execute(sa.text("SELECT COUNT(*) FROM units")).scalar()
        assert count == total


class TestDenormalisedLoadingNaturalKey:
    """`Canonicaltriples` is a lookup (no surrogate id) table -- its
    denormalised map tables key directly off its own natural key, no
    parent-id lookup needed, so this works on SQLite same as Postgres.
    """

    def test_explodes_pipe_delimited_provenance_columns(self, session):
        Base.metadata.create_all(
            session.get_bind(),
            tables=[Canonicaltriples.__table__]
            + [rel.mapper.class_.__table__ for rel in sa.inspect(Canonicaltriples).relationships],
        )

        load_entity(session, Canonicaltriples, _REAL_DATA_DIR)
        session.flush()

        results = load_denormalised(session, Canonicaltriples, _REAL_DATA_DIR)

        assert set(results) == {"class_1_provenance", "class_2_provenance"}
        assert all(count > 0 for count in results.values())

        count = session.execute(sa.text("SELECT COUNT(*) FROM canonicaltriples_class_1_provenance")).scalar()
        assert count == results["class_1_provenance"]


class TestLoadAll:
    """`load_all` composes `load_entity` + `load_denormalised` -- the two
    prior test classes already prove each half works on real data; this
    just proves the composition itself against a real table with both an
    irregular filename and real denormalised columns.
    """

    def test_loads_primary_and_denormalised_in_one_call(self, session):
        Base.metadata.create_all(
            session.get_bind(),
            tables=[Canonicaltriples.__table__]
            + [rel.mapper.class_.__table__ for rel in sa.inspect(Canonicaltriples).relationships],
        )

        results = load_all(session, Canonicaltriples, _REAL_DATA_DIR)

        assert results["canonicaltriples"] > 0
        assert results["class_1_provenance"] > 0
        assert results["class_2_provenance"] > 0

        count = session.execute(sa.text("SELECT COUNT(*) FROM canonicaltriples")).scalar()
        assert count == results["canonicaltriples"]


@pytest.mark.postgres
class TestSurrogatePkEndToEnd:
    """`Variants` is a surrogate-PK ("content") table with real
    denormalised columns and, deliberately, zero enum columns -- so this
    exercises the natural-key-to-id parent lookup on real data without
    also hitting the separate, tracked enum-casting gap (US-22).

    Requires real Postgres: SQLite's rowid-aliasing autoincrement doesn't
    apply here (a real `INSERT ... SELECT id FROM staging` carries the
    staging table's all-NULL `id` column straight through, since `id` is
    never in the source CSV) -- a known, pre-existing, separate limitation
    (see migration-status.md), not something this test works around.
    """

    def test_primary_and_denorm_load_with_correct_linkage(self, pg_session):
        map_tables = [rel.mapper.class_.__table__ for rel in sa.inspect(Variants).relationships]
        with pg_session.get_bind().begin() as conn:
            for table in [*map_tables, Variants.__table__]:
                conn.execute(sa.text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
        Base.metadata.create_all(pg_session.get_bind(), tables=[Variants.__table__, *map_tables])

        results = load_all(pg_session, Variants, _REAL_DATA_DIR)
        pg_session.commit()

        assert results["variants"] > 0
        assert set(results) >= {"variants", "blob", "study", "tracer"}
        assert all(count > 0 for count in results.values())

        # Every row in variants_study must resolve to a real parent --
        # proves the natural-key-to-id lookup actually matched real rows,
        # not just that inserts happened to succeed.
        orphaned = pg_session.execute(
            sa.text(
                "SELECT COUNT(*) FROM variants_study m "
                "LEFT JOIN variants v ON v.id = m.parent_id WHERE v.id IS NULL"
            )
        ).scalar()
        assert orphaned == 0


if __name__ == "__main__":
    pytest.main([__file__])
