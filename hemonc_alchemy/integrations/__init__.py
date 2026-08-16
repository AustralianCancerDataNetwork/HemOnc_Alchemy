"""Optional bridges to other libraries — the only place hemonc-alchemy is
allowed to depend on them. Not part of the base install.

Reserved for the HemOnc<->OMOP concept-resolution bridge discussed for
omop-alchemy specifically (not yet implemented): the rest of hemonc-alchemy
deliberately does not import omop_alchemy (see TS-5 in
_design/hemonc-alchemy-spec.md and the `.importlinter` contract that
enforces it) — the mapping from a HemOnc concept to an OMOP concept is
consumer-specific, not a fact this library should assert once for everyone.
A future `hemonc_alchemy.integrations.omop` module would live here, wiring
omop-alchemy's `toolkit.core.concepts` (`LookupIndex`, `ConceptResolver`)
against hemonc-alchemy's own entities, as an opt-in extra
(`hemonc-alchemy[omop]`) rather than a hard dependency.
"""
