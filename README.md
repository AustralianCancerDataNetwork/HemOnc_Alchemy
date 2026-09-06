# HemOnc Alchemy

HemOnc Alchemy turns an imported [HemOnc.org](https://hemonc.org) terminology database into typed SQLAlchemy models and composable Python queries.

The package sits between source data and an analysis or application:

```text
HemOnc extracts → generated model → toolkit queries and treatment policies → your application
```

The generated model describes the source. The toolkit helps navigate it and makes recurring treatment interpretations explicit. Your application remains responsible for cohort definitions, local protocol policy, OMOP mappings, and presentation.

## Start here

Read the [documentation](docs/index.md), beginning with the [quickstart](docs/getting-started/quickstart.md) if you already have a configured database, or [installation](docs/getting-started/installation.md) and [configuration](docs/getting-started/configuration.md) if you do not.

Before writing analytical joins, read [Understanding the HemOnc model](docs/model/index.md). The important questions are the row grain, the difference between a HemOnc CUI and an OMOP `concept_id`, and whether a latest-version policy is being applied.

## Install

```bash
uv add "hemonc-alchemy[postgres]"
```

For repository development:

```bash
uv sync --extra dev
```

For notebooks and exploratory plots:

```bash
uv sync --extra exploration
```

The optional `omop` extra adds the bridge for resolving HemOnc identifiers against an OMOP vocabulary. Docker, PostgreSQL, pgAdmin, source extracts, and clinical data are not installed by the package.

## Configure and query

```bash
omop-config configure hemonc_alchemy
```

```python
from sqlalchemy.orm import Session

from hemonc_alchemy import create_hemonc_engine, get_hemonc_context

_, database = get_hemonc_context()
engine = create_hemonc_engine(database)

with Session(engine) as session:
    ...
```

The [toolkit guide](docs/toolkit/index.md) explains when to use core model queries, treatment selection, classification, and scheduling. The [local development guide](docs/getting-started/local-development.md) describes the disposable Compose stack.

## Repository layout

```text
hemonc_alchemy/
├── model/       generated entities and hand-written relationships
├── toolkit/     model queries, treatment analytics, schedules, and loading
├── schema/      registry used to generate the model
├── compiler/    model-generation and validation code
└── config.py    database configuration
```

Model generation and source loading are maintainer operations. See [Regenerating the model](docs/maintainers/regeneration.md) before changing generated files.
