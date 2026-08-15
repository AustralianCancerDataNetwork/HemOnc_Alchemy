# schema/

Holds `hemonc.linkml.yaml` — the single canonical schema for hemonc-alchemy, replacing `hemonc_import`'s `registry.json` (US-14).

**Not yet authored.** Before writing it, prototype the per-table slot-scoping approach (`slot_usage` vs. fully class-local attributes) against 2-3 real tables that share column names — `date_added`, `type`, and `unit` all appear on multiple HemOnc tables. This is not optional groundwork: `docker/work/notebooks/generated_schema_hemonc.yaml` in the sibling `hemonc_import` checkout already demonstrates the failure mode live — its `Studies` class absorbed slots from unrelated tables because LinkML's `SchemaBuilder.schema.slots` is a global namespace keyed only by slot name, not scoped per class. See `_design/hemonc-alchemy-spec.md` US-14 and the "Open questions" section for the full writeup.

Once the scoping pattern is settled, this file is produced by `compiler/infer.py` reading the real HemOnc data dictionary (`hemonc_import/hemonc_import/data/data.dictionary.xlsx` in the sibling checkout) — not hand-authored from scratch, and not generated via LinkML's `gen-sqla` (tested and rejected — see the LinkML feasibility writeup in `_design/refactor-followups.md` from the migration source repo).
