# Loading data

Loading is an environment or maintainer operation. Analysis code should normally connect to an already imported database and use the model or toolkit.

## Load one entity

```python
from pathlib import Path

from hemonc_alchemy.model import Variants
from hemonc_alchemy.toolkit.loading import load_all

counts = load_all(session, Variants, Path("data/Tables"))
session.commit()
print(counts)
```

`load_all()` loads primary rows and their denormalized child tables. It resolves source filenames and headers, applies registered enum casts, and maps child rows back to generated parent IDs.

## Bootstrap the development database

```bash
uv run python .devcontainer/bootstrap.py
```

The repository bootstrap loops over generated entities for which a source file exists. It drops and recreates the target schema before loading, which makes retries deterministic but destroys existing data in that schema. Use it only with the disposable database described in [Local development](../getting-started/local-development.md).

## Preserve source-shaped values

The loader does not force uncertain source values into invented types. A field may remain nullable, string-valued, or contain a source marker such as `Uncertain date`. Convert it only at the analysis boundary where your application can state what happens to values that do not parse.
