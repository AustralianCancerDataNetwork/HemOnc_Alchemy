# Relationships and cross-references

HemOnc contains both ordinary generated relationships and cross-references
that require explicit model knowledge. The toolkit keeps those operations
visible and read-only.

## Multi-valued fields are child tables

A source field such as a variant's studies may contain several values. The
loader stores these in a child map table:

```text
Variants                 variants_study
---------                --------------
id  ───────────────────  parent_id
                         study
```

Use `variant.study_items` or `variant.study_objects` rather than parsing a
source pipe-delimited value. The same pattern applies to `Sigs.study_items` and
`Sigs.study_objects`.

## Core link helpers

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

These helpers may issue SQL when relationships are lazy or when a latest
variant context must be resolved. Keep the entity attached to its session.

## Ambiguity is part of the data model

`Studies.study` is not globally unique, and `Variants.variant_cui` can have
multiple versions. Helpers therefore need an explicit policy:

- variant traversal prefers the highest `(version, id)` for a shared CUI;
- treatment selection defaults to the latest variant row;
- study-ID queries return distinct `Studies.id` values, not a claim that source
  study names are unique;
- sig-to-variant links cannot prove version-specific membership because `Sigs`
  currently has no `version` column.

That last limitation is especially important when using `VariantBundle`,
classification, or schedule helpers on a selected variant.
