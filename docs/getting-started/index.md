# Getting started

There are two separate jobs: install the Python package, then point it at a database that already contains HemOnc data. The package does not download or provision a production extract.

The shortest useful route is:

1. [Install](installation.md) the base package and the PostgreSQL driver.
2. [Configure](configuration.md) a named database with `omop-config`.
3. Follow the [quickstart](quickstart.md) to resolve a condition and select variants.

Use the [local development](local-development.md) guide when you want the disposable Compose stack, pgAdmin, or the repository's notebooks.

The first conceptual guide to read is [Understanding the HemOnc model](../model/index.md). It explains row grain, source identifiers, versioning, and multi-valued fields—the details that determine whether a query is counting what you think it is counting.
