"""Schema diff — new in this rewrite, no equivalent in hemonc_import (US-8).

hemonc_import's registry_main.py writes entities.py/enums.py/registry.json
unconditionally on every regeneration; nothing compares the new output
against what was previously committed. This is the confirmed root cause of
the git-divergence problems found in the audit: a real fix present for one
sibling field (`biomarker4`) went silently missing for another
(`canmed_minor_class`) after a regeneration, and a `studies` entity's
description/maturity metadata was found to have silently absorbed values
from a deleted `study_demographics` entity in the same pass. Neither would
have survived a diff step that required acknowledging what changed.

Responsibility: compare schema/hemonc.linkml.yaml[n-1] (the last committed
version, e.g. via git show HEAD:schema/hemonc.linkml.yaml) against
schema/hemonc.linkml.yaml[n] (freshly generated), and refuse to let
`hemonc-alchemy regen` succeed silently if:
- a table or column present before is now absent (or vice versa) without
  explicit acknowledgement
- a column's type or nullability changed
- natural/business key composition changed for any table

`hemonc-alchemy diff` should be runnable standalone (for a Schema Author to
review before committing) and also invoked by `regen` as a gate.
"""

from __future__ import annotations
