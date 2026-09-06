# Relationships and cross-references

HemOnc contains ordinary foreign-key relationships, normalized child tables for multi-valued fields, and source links that need explicit policy. The ORM exposes these as read-only navigation; it does not remove ambiguity from the data.

## Multi-valued source fields

Source spreadsheets often store several values in one cell, for example `"12460|1354"`. The loader splits those values into child map rows:

```text
Variants                 variants_study
---------                --------------
id  ───────────────────  parent_id
                         study
```

Use `variant.study_items` or `variant.study_objects` rather than parsing a pipe-delimited string. The same pattern applies to sigs, indications, and other generated map tables.

## Traversal helpers

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

Some helpers issue SQL when a relationship is lazy or when they must resolve a latest variant context. Keep the entity attached to its session for the duration of traversal.

## Ambiguity is part of the model

`Studies.study` is not globally unique. The same study name can be represented by several rows, often because it is associated with several conditions. Do not use `.scalar_one()` on a study-name lookup unless you have first established uniqueness for your extract.

`Variants` can contain several imported rows for one `variant_cui`. Traversal and treatment selection therefore need an explicit version policy; the toolkit's latest policy keeps the highest `(version, id)`.

`Sigs` currently store `variant_cui` but not variant version. A sig attached to a selected variant is therefore shared across imported versions with that CUI. It is not evidence of version-specific provenance.

The toolkit reports or preserves these ambiguities instead of picking an arbitrary row. If your application needs a single result, make the tie-breaking rule part of that application's query.
