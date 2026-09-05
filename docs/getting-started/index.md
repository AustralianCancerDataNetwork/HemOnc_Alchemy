# Getting started

This section gets you from an installed package to a session that can answer
questions about imported HemOnc data.

HemOnc Alchemy does not provision a database for production use. It works with
any reachable PostgreSQL database that contains the generated HemOnc schema.
The repository also includes an optional two-container development stack for
local exploration.

## Orientation

- [Installation](installation.md) — install the query or development extras.
- [Configuration](configuration.md) — register a database with the shared stack configuration.
- [Quickstart](quickstart.md) — create an engine, session, and first query.
- [Local development](local-development.md) — use the PostgreSQL, pgvector, pgAdmin, and Python containers.
