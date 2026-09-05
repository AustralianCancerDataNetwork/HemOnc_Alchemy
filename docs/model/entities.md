# Entities and generated models

The classes in `hemonc_alchemy.model` are generated from the HemOnc data
dictionary. They are not the place to add application-specific properties or
workflow state.

```python
from hemonc_alchemy import Sigs, Variants

variant = session.get(Variants, variant_id)
if variant is not None:
    for sig in variant.component_sigs:
        print(sig.component, sig.alldays)
```

## Surrogate IDs and natural keys

Some entity tables use a generated integer `id` as their primary key while the
source identity remains a separate natural key. For `Variants`:

```text
primary key:  id
natural key: (variant_cui, version)
identity:    variant_cui, when a latest-version policy is explicit
```

Do not join a child map's `parent_id` to a CUI. `variants_study.parent_id`
points to `Variants.id`, not `Variants.variant_cui`.

## Generated enums

Enum columns are exposed as generated Python enum members after loading:

```python
from hemonc_alchemy.model.enums import Sigs_RouteEnum

if sig.route == Sigs_RouteEnum.INTRAVENOUS:
    ...
```

Toolkit APIs that accept source-facing strings document whether they normalize
the value. When writing lower-level SQLAlchemy expressions, prefer the generated
enum member for enum columns.

## Selected entities

The [model API reference](../reference/entities.md) documents selected entity
classes and their generated columns. The complete generated surface can be
larger than the small set most analyses need, because it follows the current
data dictionary.
