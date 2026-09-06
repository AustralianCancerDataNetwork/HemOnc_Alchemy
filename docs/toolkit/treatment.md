# Treatment analytics

Treatment analytics are where HemOnc rows acquire reusable treatment meaning. The key discipline is to keep the policy explicit: HemOnc supplies source labels and relationships, while the selection spec or classification function states how your application interprets them.

## Classify a variant

```python
from hemonc_alchemy.toolkit.analytics.treatment.classification import (
    is_concurrent_chemort,
    is_rt_only,
)

if is_concurrent_chemort(variant):
    print("radiation and systemic sigs are both confidently classified")
elif is_rt_only(variant):
    print("all sigs are confidently classified as radiation")
```

An unknown or NULL `class_field` is unknown. It does not count as systemic treatment and prevents a confident radiation-only or concurrent-chemoradiotherapy classification. Treating “unclassified” as “not present” would turn missing source information into a clinical conclusion.

## Query standalone radiation

```python
from hemonc_alchemy.toolkit.analytics.treatment.filters import (
    find_standalone_radiation_sigs,
)

sigs = find_standalone_radiation_sigs(session, [condition_cui])
```

“Standalone” is a precise query policy: a radiation-classified sig with regimen `Radiation therapy`, no `variant_cui`, and a normalized study link to one of the requested condition CUIs. It does not prove that the entire study contains no systemic treatment.

## Select variants

Describe the selection as a plain spec, then execute it:

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

Component terms within one requirement are alternatives; separate requirements are combined. Category requirements work the same way, but require an application-supplied mapping from a source field to the category names used by the spec:

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

The mapping is policy, not a hidden property of the model. Read source values before building a production mapping and decide how unmapped classes should be handled.

`build_variant_query_artifacts()` exposes the component projection, category projection, matching variant identities, and final statement. Use it when a selection needs auditability or returns an unexpected volume.
