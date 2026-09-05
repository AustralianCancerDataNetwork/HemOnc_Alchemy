# Configuration

Database settings use `oa-configurator`, the shared configuration layer used by
the Australian Cancer Data Network stack. This keeps connection details out of
source code and lets related packages refer to the same named database.

## Configure a HemOnc database

Run:

```bash
omop-config configure hemonc_alchemy
```

When prompted, configure the database referenced by `hemonc_db`. A minimal
configuration conceptually looks like this:

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

Use the interactive command to create the exact file and preserve the
configurator's current schema conventions. Never commit passwords.

## Create an engine

```python
import sqlalchemy.orm as so

from hemonc_alchemy import create_hemonc_engine, get_hemonc_context

_, database = get_hemonc_context()
engine = create_hemonc_engine(database)

with so.Session(engine) as session:
    ...
```

`get_hemonc_context()` resolves the named database once. Keep the engine for
the lifetime of the application and create sessions for individual units of
work.

## Check connectivity

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

If configuration is missing, the connection helper points you back to
`omop-config configure hemonc_alchemy`.
