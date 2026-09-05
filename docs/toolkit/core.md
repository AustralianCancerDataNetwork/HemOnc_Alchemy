# Core queries and links

The core toolkit handles reusable operations that are directly about the
HemOnc model: condition lookup, component search, and traversal through
normalized cross-references.

## Resolve conditions

```python
from hemonc_alchemy.toolkit.core.conditions import (
    condition_cuis_by_names,
    conditions_by_names,
)

conditions = conditions_by_names(session, "Acute myeloid leukemia")
condition_cuis = condition_cuis_by_names(session, "Acute myeloid leukemia")
```

Name matching is exact. Missing names are omitted and logged; callers that
need to distinguish an absent condition should check the returned list.

## Search components

```python
from hemonc_alchemy.toolkit.core.components import search_components

hits = search_components(session, "cisplatin")
for hit in hits:
    print(hit.component_cui, hit.component, hit.drug_inn, hit.main_class)
```

Search covers the sig component label, drug name and INN, main class, and
normalized CanMED major/minor class rows. The default search is case-insensitive
substring matching. Pass explicit `columns` when the search scope must be
narrower.

## Compose SQL

Use `component_search_statement()` or `component_cui_subquery()` when composing
the search with your own condition or study predicates. The statements join
CanMED child rows through `Drugs.id`, because a child `parent_id` is a generated
surrogate foreign key rather than a drug CUI.

## Follow links

The [relationships guide](../model/relationships.md) shows the common traversal
helpers. They are deliberately separate from generated table declarations so
loading remains structural and predictable.
