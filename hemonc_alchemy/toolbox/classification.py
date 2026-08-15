"""Clinical/domain classification rules.

Tier 3 of the split from hemonc_import's final_model/relationships.py
(US-17) — not a relationship at all, but domain classification, comparable
to SCOOP's protocols/classification/. The original hardcoded the
classification literal inline (`_sig_class_value(sig) == "rad sig"`); this
module should expose that as a named constant so it's discoverable and
overridable rather than a magic string buried in a comparison.

Pending model/entities.py existing, these cannot be ported verbatim yet.
Source, from
hemonc_import/src/hemonc_import/final_model/relationships.py:33-35,157-180:

- `_sig_class_value` (a `Sigs.class_field` accessor) — becomes the basis for
  a named `RAD_SIG_CLASS_VALUE = "rad sig"` constant here, not an inline
  string literal.
- `has_radiation_sig` / `has_non_radiation_sig` (any/all over
  `variant.component_sigs`)
- `is_concurrent_chemort` (`has_radiation_sig and has_non_radiation_sig`)
- `is_rt_only` (`has_radiation_sig and not has_non_radiation_sig`)
"""

from __future__ import annotations

RAD_SIG_CLASS_VALUE = "rad sig"
