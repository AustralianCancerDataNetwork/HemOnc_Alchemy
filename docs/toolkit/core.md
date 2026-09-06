# Core queries and links

`toolkit.core` answers questions about the HemOnc model without deciding what the result means clinically. Its main jobs are to resolve condition names, search treatment components, select condition-scoped sigs, and traverse normalized links.

## Resolve names to CUIs

Use names at the edge of an application, then carry CUIs through the rest of the query:

```python
from hemonc_alchemy.toolkit.core.conditions import (
    condition_cuis_by_names,
    conditions_by_names,
)

conditions = conditions_by_names(session, "Acute myeloid leukemia")
condition_cuis = condition_cuis_by_names(session, "Acute myeloid leukemia")
```

Matching is exact. Missing names are omitted and logged rather than raised. If an absent condition would make the analysis invalid, check the returned list immediately and fail with an application-level message.

The returned CUI is a HemOnc identifier, not an OMOP `concept_id`. When an OMOP-shaped vocabulary contains HemOnc, the CUI can be looked up as `concept_code` with `vocabulary_id = 'HemOnc'`. That is different from following an external mapping to a target vocabulary.

## Search components

```python
from hemonc_alchemy.toolkit.core.components import search_components

hits = search_components(session, "cisplatin")
for hit in hits:
    print(hit.component_cui, hit.component, hit.drug_inn, hit.main_class)
```

The default search is case-insensitive substring matching over the sig component label, drug name and INN, main class, and normalized CanMED major/minor class rows. Pass explicit `columns` when the vocabulary scope matters; a class-label search and a drug-name search answer different questions.

Use `component_search_statement()` when you need SQLAlchemy composition, and `component_cui_subquery()` when the component match is only one predicate in a larger query. CanMED child rows join through generated `Drugs.id`, not through a drug CUI.

## Follow model links

```python
from hemonc_alchemy.toolkit.core.links import (
    condition_variant_objects,
    sig_condition_objects,
    sig_study_objects,
    study_variant_objects,
)

conditions = sig_condition_objects(sig)
studies = sig_study_objects(sig)
variants = study_variant_objects(study)
```

These helpers may query the database and may deduplicate by entity identity. They keep source ambiguity visible: a study name can resolve to several study rows, and variant traversal applies an explicit latest-version policy where needed. Keep the entity attached to its session.

## Select condition-scoped sigs

Use `SigSelectionSpec` for candidates that are not naturally retrieved through a regimen-variant selection, such as standalone radiotherapy or surgery:

```python
from hemonc_alchemy.toolkit.core import SigSelectionSpec, find_sigs

spec = SigSelectionSpec.for_conditions(
    [condition_cui],
    component_terms="External beam radiotherapy",
    variant_policy="none",
)
sigs = find_sigs(session, spec)
```

The condition restriction is resolved through normalized `sigs_study` links. The spec can also constrain regimen, phase, class field, study context, and the columns used for component matching. `sig_search_statement(spec)` returns the inspectable statement without executing it.

Sigs do not carry a version column. A sig selection therefore says which sig rows match; it does not establish version-specific provenance for a variant.
