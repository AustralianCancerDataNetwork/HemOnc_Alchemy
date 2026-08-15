"""Shared pytest fixtures.

Marker convention mirrors omop-alchemy (US-27): unmarked tests run on
sqlite with no external dependencies; `@pytest.mark.postgres` tests require
a docker-compose Postgres instance and are skipped by default.
"""
