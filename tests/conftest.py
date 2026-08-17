"""Shared pytest fixtures.

Marker convention mirrors omop-alchemy (US-27): unmarked tests run on
sqlite with no external dependencies; `@pytest.mark.postgres` tests require
a docker-compose Postgres instance and are skipped by default.

`tests/docker-compose.yaml` brings up that instance (`docker compose -p
hemonc_alchemy_tests up -d` from this directory, port 55433 -- distinct
from orm-loader's own equivalent test stack on 55432, since both compose
files live in a directory literally named `tests` and share a container
name unless given explicit, distinct `-p` project names). Configure the
`test_hemonc_db` field `HemOncAlchemyConfig` already declares against it
once, via `omop-config connections add`/`omop-config databases add`
(see migration-status.md for the exact commands used to set this up).
"""

import time

import pytest
import sqlalchemy as sa


@pytest.fixture(scope="session")
def pg_engine():
    from oa_configurator.pytest_plugin import (
        ensure_test_db_exists,
        resolve_test_database,
    )

    from hemonc_alchemy.config import HemOncAlchemyConfig

    url = resolve_test_database(HemOncAlchemyConfig, "test_hemonc_db")

    try:
        ensure_test_db_exists(url)
    except Exception as exc:  # noqa: BLE001 -- best-effort setup, real connection attempt follows
        print(f"Could not ensure test DB exists, will try anyway: {exc}")

    last_err = None
    for i in range(20):
        engine: sa.Engine | None = None
        try:
            engine = sa.create_engine(url, future=True)
            with engine.connect() as conn:
                conn.execute(sa.text("SELECT 1"))
            yield engine
            engine.dispose()
            return
        except Exception as exc:  # noqa: BLE001 -- retry loop, any connection failure should retry
            if engine is not None:
                engine.dispose()
            last_err = exc
            print(f"[{i}] Postgres not ready:", repr(exc))
            time.sleep(1)

    pytest.skip(f"PostgreSQL never became available: {last_err}")


@pytest.fixture
def pg_session(pg_engine):
    import sqlalchemy.orm as so

    Session = so.sessionmaker(pg_engine, future=True)
    with Session() as session:
        yield session
        session.rollback()
