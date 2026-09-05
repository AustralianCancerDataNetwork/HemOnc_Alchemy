# Loading data

Loading is a maintainer or environment operation. Analysis code should normally
connect to an already imported database and use the model or toolkit.

## Load one entity

```python
from pathlib import Path

from hemonc_alchemy.model import Variants
from hemonc_alchemy.toolkit.loading import load_all

counts = load_all(
    session,
    Variants,
    Path("data/Tables"),
)
session.commit()
print(counts)
```

`load_all()` loads the entity's primary rows and then its denormalized child
tables. It resolves source filenames and headers, applies the registered enum
casts, and maps denormalized rows back to their generated parent IDs.

## Full development bootstrap

The repository bootstrap loops over every generated entity with a source file:

```bash
uv run python .devcontainer/bootstrap.py
```

It drops and recreates the schema first. This makes retries deterministic after
a partial import, but also makes it destructive to the target database. Use it
only with the disposable development database described in [Local development](../getting-started/local-development.md).

## Source-shaped values

The loader preserves the fact that some source values are not safely numeric or
date-like. For example, a value such as `Uncertain date` is not forced into an
invented timestamp. Scheduling and analysis code should handle nullable or
string-valued source fields at the boundary where a numeric interpretation is
actually needed.
