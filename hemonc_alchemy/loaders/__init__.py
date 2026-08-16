"""Loading built on orm_loader's interfaces — part of the runtime (not the
author extra). See ../model/base.py for the EntityBase composition and
_design/hemonc-alchemy-spec.md US-19/US-20/US-21.

Deliberately does NOT include a HemOnc-to-OMOP vocabulary bulk loader
(hemonc_import's old `omop_load.py`, ~752 lines). That module bundled two
different problems, and only one of them is still hemonc-alchemy's to
solve:

1. Generic Athena-CSV-to-CDM bulk loading (staging tables, merge
   strategies, chunked reads, retries) -- superseded by omop-alchemy 1.0's
   own `maintenance/cli_vocab.py` (`load_vocab_source`), a more mature,
   actively-maintained implementation of exactly this. Re-porting it here
   would be maintaining a second, weaker copy of code that already exists
   and is better exercised elsewhere.
2. HemOnc-specific vocabulary *subset* scoping (only load the vocabularies
   relevant to HemOnc mapping work, trace concept_relationship/
   concept_ancestor outward from a HemOnc anchor concept) -- genuinely had
   no omop-alchemy equivalent, but is an optimisation against loading the
   full multi-GB Athena export, not a hard requirement. The assumption
   going forward is that a CDM backend resource already exists and is
   already populated (via `omop-alchemy vocab load`, run once as
   environment setup, independent of hemonc-alchemy) -- hemonc-alchemy
   consumes concepts by reference against that shared database rather than
   loading them itself.

Concept resolution/lookup (mapping a HemOnc code or name to an OMOP
concept) also now belongs to omop-alchemy's `toolkit.core.concepts`
(`LookupIndex`, `ConceptResolver`) -- a consumer needing that reaches for
omop-alchemy directly, the same way SCOOP already depends on both
libraries side by side (TS-5). hemonc-alchemy has zero omop-alchemy
touchpoints anywhere in its own runtime as a result -- not even indirectly
through a vocab loader.
"""
