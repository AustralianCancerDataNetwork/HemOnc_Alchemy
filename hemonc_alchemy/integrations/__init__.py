"""Optional bridges to other libraries — the only place hemonc-alchemy is
allowed to depend on them. Not part of the base install.

Reserved for the HemOnc<->OMOP concept-resolution bridge - the rest of 
hemonc-alchemy deliberately does not import omop_alchemy 

the mapping from a HemOnc concept to an OMOP concept is consumer-specific, 
not a fact this library should assert once for everyone.
"""
