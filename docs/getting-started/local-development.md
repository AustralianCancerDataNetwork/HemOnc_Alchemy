# Local development stack

The repository's `.devcontainer` stack provides three services:

- a pure PostgreSQL 18 database with pgvector enabled;
- a pure Python development environment installed with `uv`;
- pgAdmin for browser-based database inspection.

The Python service mounts the checkout and installs the development extras,
including IPython and `ipykernel`, so VS Code notebooks can use the project
environment.

## Start the stack

From the repository root:

```bash
docker compose -f .devcontainer/compose.yaml up -d
```

Open the repository in the Dev Container when using VS Code. The Python
interpreter is `/opt/venv/bin/python` inside the container.

## pgAdmin

Open [http://localhost:5050](http://localhost:5050). The default development
login is defined by `.devcontainer/.env`; set your own values there rather than
sharing the defaults on a shared machine.

The `hemonc` PostgreSQL server is provisioned automatically from the checked-in
pgAdmin server definition. Inside pgAdmin use:

```text
Host:     postgres
Port:     5432
Database: hemonc_alchemy
User:     hemonc
```

The host name is `postgres` because pgAdmin connects over the Compose network,
not through `localhost`.

## Import data

Place the HemOnc extracts under `data/Tables`, then run the disposable
development bootstrap from the Python container:

```bash
docker compose -f .devcontainer/compose.yaml exec \
  python-hemonc-alchemy uv run python .devcontainer/bootstrap.py
```

Bootstrap recreates the schema before loading. It is intended for a disposable
development database and should not be pointed at a database containing work
you need to preserve.

For a controlled load in application code, see [Loading data](../model/loading.md).
