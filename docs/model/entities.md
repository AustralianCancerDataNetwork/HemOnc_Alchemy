# Entities and generated models

The classes in `hemonc_alchemy.model` are generated from the HemOnc data dictionary. Treat them as a faithful structural surface: application-specific state, protocol rules, and derived classifications belong outside the generated model.

## Choosing a class

Use the entity that matches the question's grain:

- `Conditions` for condition identity and names.
- `Regimens` for named treatment concepts and regimen-level metadata.
- `Variants` for concrete regimen versions.
- `Sigs` for drug, dose, route, and cycle-day instructions.
- `Drugs` for component identity and classification.
- `Indications` for regulatory records.
- `Studies` and `StudyResults` for source studies and recorded outcomes.

For example:

```python
from hemonc_alchemy import Sigs, Variants

variant = session.get(Variants, variant_id)
if variant is not None:
    for sig in variant.component_sigs:
        print(sig.component, sig.alldays)
```

## Surrogate IDs and source keys

Generated primary keys make relationships efficient, but they are not usually the source identity. For `Variants`:

```text
database primary key: id
source/version key:   (variant_cui, version)
latest identity:      variant_cui, when a latest-version policy is explicit
```

Child map rows use generated foreign keys. For example, `variants_study.parent_id` points to `Variants.id`, not `Variants.variant_cui`.

## Generated enums

Enum columns are exposed as generated Python enum members:

```python
from hemonc_alchemy.model.enums import Sigs_RouteEnum

if sig.route == Sigs_RouteEnum.INTRAVENOUS:
    ...
```

Toolkit functions that accept source-facing strings document their normalization rules. In lower-level SQLAlchemy expressions, prefer the generated enum member for enum columns.

## HemOnc CUIs and OMOP concepts

A HemOnc CUI is a source identifier, not an OMOP `concept_id`. When the HemOnc vocabulary is loaded into OMOP, the CUI can be found as `concept_code` with `vocabulary_id = 'HemOnc'`; an external mapping then leads to a target vocabulary and target code. These are separate joins with separate semantics.
