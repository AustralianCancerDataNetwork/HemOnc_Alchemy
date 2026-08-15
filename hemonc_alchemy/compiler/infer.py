"""Type/enum/natural-key/denormalisation inference from the HemOnc data dictionary.

Ports hemonc_import/src/hemonc_import/registry_version/infer.py (326 lines).
This is HemOnc-workbook-specific business logic (parsing "Unique Key" cells,
detecting pipe-delimited denormalised column groups, classifying enums from
an observed-value snapshot) that stays bespoke regardless of the schema
format — neither LinkML nor generic CSV-induction tooling (schema-automator)
understands these conventions. Confirmed in
_design/refactor-followups.md §2.

Confirmed bugs to fix during the port (empirically validated against the
real data dictionary in _design/refactor-followups.md §4 — not theoretical):

- `parse_unique_key` (source infer.py:268-294): claims to strip parenthetical
  explanatory text but doesn't. Two real, confirmed cases:
  `sequencetable`'s `"(complex)"` -> must become `[]` contribution, not a
  fabricated `'complex'` pseudo-column; `changelog`'s
  `"Date + Type + Affected Table + (Addition|Change|Deletion)"` -> must
  parse to `['date', 'type', 'affected', 'table']`, not fuse the
  parenthetical alternatives into `'additionchangedeletion'`. A commented-out
  attempt at the real fix already exists in the source
  (`re.sub(r"\\(.*?\\)", "", p)`) — apply it, don't reinvent it.
- `infer_pipe_groups` (source infer.py:307-324): wraps an already-distinct
  2-element list in `set()`, so output order depends on Python's string hash
  randomization. CONFIRMED via 3 subprocess runs plus explicit
  `PYTHONHASHSEED=0`/`=1` testing to be the actual mechanism behind a real
  git-merge inconsistency in hemonc_import (the `canmed_minor_class` fix
  present on one branch, silently absent on another after a regeneration).
  Fix: `sorted([c1, c2])`, not `set(...)`.
- Enum threshold (`MAX_ENUM_UNIQUE=20`, source infer.py:22): QUANTIFIED as
  low but non-zero risk — of 58 real columns currently classified Enum, 3
  sit within 3 of the cliff (`conditions.condition_type`=19,
  `units.unit_type`=19, `studies.registry`=17). Not urgent, but
  compiler/audit.py should surface these proactively (US-15) rather than
  silently reclassifying a column to String on the next HemOnc release.
- Filename resolution (`filename_to_table_name`, TableMeta.filename
  convention): CONFIRMED to be why 4 of 17 "missing" tables in hemonc_import
  actually have real, available data that's silently never found —
  `canonicaltriples`/`canonical.triples.csv`,
  `contexttable`/`context.table.csv`, `variantblob`/`variant.blob.csv`, and
  `study_eligibility`/`study_eligibility beta.csv` (space + "beta" suffix).
  Fix the filename-matching convention to handle dotted/spaced real
  filenames, not just the naive `f"{table_name}.csv"` case.
- `safe_identifier` column-name normalisation: REFUTED as a real collision
  risk (0 collisions found across 340 real identifiers) — port as-is,
  no fix needed here.
- Derived-column substring heuristic (`"count_"`, `"total"`, `"valid"`,
  `"num_"`): REFUTED as a real false-positive risk in the current dictionary
  (1 hit, `persons.total_pubs`, and it's a genuine derived column) — port
  as-is, but keep the heuristic narrow if new columns are added later.
"""

from __future__ import annotations
