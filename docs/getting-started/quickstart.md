# Quickstart

This example assumes PostgreSQL is configured and the HemOnc tables have
already been imported.

## Query a condition and its variants

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from hemonc_alchemy import Conditions, create_hemonc_engine, get_hemonc_context
from hemonc_alchemy.toolkit.core.conditions import condition_cuis_by_names
from hemonc_alchemy.toolkit.analytics.treatment.selection import (
    TreatmentSelectionSpec,
    select_variants,
)

_, database = get_hemonc_context()
engine = create_hemonc_engine(database)

with Session(engine) as session:
    condition_cuis = condition_cuis_by_names(session, "Acute myeloid leukemia")
    if not condition_cuis:
        raise LookupError("Condition was not found")

    spec = TreatmentSelectionSpec.for_conditions(condition_cuis)
    variants = select_variants(session, spec)

    for variant in variants[:5]:
        print(variant.variant_cui, variant.version, variant.regimen)
```

The default selection policy is `version_policy="latest"`: one generated
`Variants` row per `variant_cui`. Pass `version_policy="all"` when comparing
all imported versions deliberately.

## Inspect a variant's components

```python
from hemonc_alchemy.toolkit.analytics.treatment.bundles import VariantBundle

bundle = VariantBundle.from_variant(variants[0])
for sig in bundle.sigs:
    print(sig.component, sig.doseminnum, sig.doseunit, sig.alldays)
```

The bundle keeps the ORM rows attached to the session. The `Sigs` model does not
carry a version column, so the sigs should be read as linked by shared
`variant_cui`, not as version-provenance evidence.

## Build SQL without executing it

Toolkit queries return SQLAlchemy statements when you need to inspect or extend
the query before execution:

```python
from hemonc_alchemy.toolkit.core.components import component_search_statement

statement = component_search_statement("cisplatin")
statement = statement.limit(20)
rows = session.execute(statement).mappings().all()
```

This keeps SQL visible. The toolkit does not hide joins or turn every query
into a pandas DataFrame.
