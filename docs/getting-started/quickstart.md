# Quickstart

The normal analysis flow is: resolve a human-readable condition name once, keep the resulting CUI, build an explicit selection specification, and execute it with your session. Names are convenient input; CUIs are the stable scope passed into model queries.

This example assumes PostgreSQL is configured and the HemOnc tables are loaded:

```python
from sqlalchemy.orm import Session

from hemonc_alchemy import create_hemonc_engine, get_hemonc_context
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

    spec = TreatmentSelectionSpec.for_conditions(
        condition_cuis,
        version_policy="latest",
    )
    variants = select_variants(session, spec)

    for variant in variants[:5]:
        print(variant.variant_cui, variant.version, variant.regimen)
```

`version_policy="latest"` returns one generated `Variants` row per `variant_cui`, using the highest imported `(version, id)`. Use `version_policy="all"` when the purpose is to compare or audit imported versions. Do not infer version policy from the CUI alone.

## Inspect a selected variant

```python
from hemonc_alchemy.toolkit.analytics.treatment.bundles import VariantBundle

bundle = VariantBundle.from_variant(variants[0])
for sig in bundle.sigs:
    print(sig.component, sig.doseminnum, sig.doseunit, sig.alldays)
```

The bundle is a read model over ORM rows; it is not a second persistence schema. `Sigs` has no version column, so its relationship to a selected variant is by shared `variant_cui`, not proof of version-specific provenance.

## Inspect or extend the SQL

The toolkit keeps query construction separate from execution. Use a statement when you need to inspect SQL, add a predicate, apply a limit, or return mappings instead of ORM objects:

```python
from hemonc_alchemy.toolkit.core.components import component_search_statement

statement = component_search_statement("cisplatin").limit(20)
rows = session.execute(statement).mappings().all()
```

For treatment selection, `build_variant_query_artifacts()` exposes the intermediate projections as well as the final statement. This is useful when a selection returns an unexpected number of variants.
