# Configuration

HemOnc Alchemy uses `oa-configurator` so several Australian Cancer Data Network packages can refer to the same named databases without putting credentials in Python or source control.

The configuration has three levels:

- A **connection** contains driver, host, credentials, and database name.
- A **database** gives that connection a logical name and schema.
- A **tool target** tells HemOnc Alchemy which logical database to use as `hemonc_db`.

That indirection is useful when the same application moves between a local database, a shared server, and a test database. It also makes it possible for a HemOnc target and an OMOP target to share a PostgreSQL server while remaining different schemas or databases.

## Configure a database

Run the interactive configurator:

```bash
omop-config configure hemonc_alchemy
```

A minimal configuration has this shape:

```toml
[connections.hemonc]
dialect       = "postgresql+psycopg"
host          = "localhost"
port          = 5432
user          = "hemonc"
password      = "change-me"
database_name = "hemonc_alchemy"

[databases.hemonc_db]
kind        = "generic"
connection  = "hemonc"
schema_name = "public"

[tools.hemonc_alchemy]
hemonc_db = "hemonc_db"
```

Let the configurator create the real file so its current conventions are preserved. Never commit passwords. If you need separate test or OMOP targets, configure them as additional named databases rather than changing application code.

## Open a session

Resolve the logical target once, keep the engine for the lifetime of the application, and create sessions for units of work:

```python
from sqlalchemy.orm import Session

from hemonc_alchemy import create_hemonc_engine, get_hemonc_context

_, database = get_hemonc_context()
engine = create_hemonc_engine(database)

with Session(engine) as session:
    ...
```

Toolkit functions do not own your session or transaction. This keeps connection lifetime, transaction boundaries, and error handling under application control.

## The devcontainer configuration

When the repository devcontainer is created, `.devcontainer/config.toml` is copied to `~/.config/omop/config.toml` with mode 600. Its `hemonc_db` target points at the Compose PostgreSQL service; its test target points at a separate `hemonc_alchemy_test` database. The same server exposes `cdm_db` and `test_cdm_db` in the `omop` schema.

The checked-in file is a seed, not the active configuration. Delete the copied configuration before rebuilding if you want to start again from the seed. To keep configuration elsewhere, set `OA_CONFIG_PATH`.

## Check the connection

```bash
python - <<'PY'
from sqlalchemy import text
from sqlalchemy.orm import Session

from hemonc_alchemy import create_hemonc_engine, get_hemonc_context

_, database = get_hemonc_context()
engine = create_hemonc_engine(database)
with Session(engine) as session:
    print(session.execute(text("SELECT 1")).scalar_one())
PY
```

If the target is missing, configure it with `omop-config configure hemonc_alchemy` rather than embedding a connection string in analysis code.
