"""HemOnc-specific OMOP-vocabulary loading helpers.

Ports hemonc_import/src/hemonc_import/utils/omop_load.py (752 lines).
Already imports orm_loader directly today in hemonc_import (`bulk_load_context`,
`LoaderContext`, `PandasLoader`, `infer_encoding`) but as an undeclared
transitive dependency reached only via omop-alchemy's own pin — orm-loader
is now a direct, explicit dependency of hemonc-alchemy itself (see
pyproject.toml), so this module can depend on it plainly.

Fixes to apply during the port:

- Parameterize hardcoded HemOnc defaults (omop_load.py:544,672):
  `vocabulary_id: str = "HemOnc"` and `anchor_vocabulary_id: str = "HemOnc"`
  are baked into functions that otherwise read as generic OMOP-vocabulary
  loaders. Keep "HemOnc" as the default value if useful, but make it clear
  in the function's purpose/naming that this is HemOnc-specific, not a
  generic utility incidentally defaulting to one vocabulary.
- Don't mask the original exception in the cleanup path (omop_load.py:344-348):
  `finally: try: model.drop_staging_table(session) finally: ...` — if the
  main load body raised because the session's transaction is now invalid,
  the cleanup call is likely to raise too, silently replacing the original
  error. Catch and log the cleanup failure without letting it hide what
  actually failed.
- Rename or merge `drop_existing_rows()` (omop_load.py:246-282, a DataFrame-
  level PK dedup) so it's not confusable with the unrelated `drop_existing:
  bool` parameter threaded through the loader (which actually toggles
  merge strategy, not a truncate) — same phrase, two unrelated meanings in
  one file today.
- Chunk the `IN`-clause in `drop_existing_rows` rather than building one
  query over an entire incoming CSV's primary keys.

Prefer orm_loader's own chunked bulk-load/merge-strategy machinery
(loadable_table.py) over hand-rolling equivalents here where the two
overlap — this module should own only the HemOnc/OMOP-vocabulary-specific
parts orm_loader has no opinion about.
"""

from __future__ import annotations
