# Treatment analytics

Treatment analytics interpret HemOnc sigs and variants while keeping the
selection criteria explicit.

## Classify a variant

```python
from hemonc_alchemy.toolkit.analytics.treatment.classification import (
    is_concurrent_chemort,
    is_rt_only,
)

if is_concurrent_chemort(variant):
    print("radiation and systemic sigs are both classified")
elif is_rt_only(variant):
    print("all sigs are confidently classified as radiation")
```

A NULL or unknown `class_field` is unclassified. It does not count as systemic
treatment, and it prevents a variant from being called confidently RT-only.

## Filter standalone radiation sigs

```python
from hemonc_alchemy.toolkit.analytics.treatment.filters import (
    find_standalone_radiation_sigs,
)

sigs = find_standalone_radiation_sigs(session, [condition_cui])
```

“Standalone” here is a specific model query policy: a radiation-classified sig
with regimen `Radiation therapy`, no `variant_cui`, and a normalized study link
to one of the requested condition CUIs. It is not equivalent to proving that a
whole study contains no systemic treatment.

## Select variants by requirements

```python
from hemonc_alchemy.toolkit.analytics.treatment.selection import (
    ComponentRequirement,
    TreatmentSelectionSpec,
    select_variants,
)

spec = TreatmentSelectionSpec.for_conditions(
    [condition_cui],
    component_requirements=(ComponentRequirement.from_terms("cisplatin"),),
    version_policy="latest",
)
variants = select_variants(session, spec)
```

Category requirements require an explicit mapping from source fields to the
categories used by the requirement:

```python
from hemonc_alchemy.toolkit.analytics.treatment.selection import CategoryRequirement

spec = TreatmentSelectionSpec.for_conditions(
    [condition_cui],
    category_requirements=(CategoryRequirement("cytotoxic", 1),),
)
variants = select_variants(
    session,
    spec,
    category_mapping={"main_class": {"Platinum agent": "cytotoxic"}},
)
```

The query builder exposes intermediate SQL artifacts when a notebook or test
needs to inspect the component projection, category projection, matching
variant IDs, and final ORM statement.
