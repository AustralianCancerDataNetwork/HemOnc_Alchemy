# Installation

## Querying an existing database

Install the package with `uv`:

```bash
uv add hemonc-alchemy
```

The base install provides the generated SQLAlchemy model, connection helpers,
and toolkit query APIs. PostgreSQL support is included in the recommended
`postgres` extra:

```bash
uv add "hemonc-alchemy[postgres]"
```

The equivalent `pip` form is:

```bash
pip install "hemonc-alchemy[postgres]"
```

## Working on HemOnc Alchemy

From a checkout, install the development environment:

```bash
uv sync --extra dev
```

This includes the model-generation tooling, tests, linting, IPython, and
Jupyter kernel support used by the repository's notebooks and development
containers.

## What is not installed by default

The package does not install Docker, PostgreSQL, pgAdmin, or HemOnc source
extracts. Those are environment concerns. For a disposable local database,
use the repository's [development stack](local-development.md).
