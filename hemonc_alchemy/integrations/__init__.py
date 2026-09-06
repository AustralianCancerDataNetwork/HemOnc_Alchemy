"""Optional bridges to external standards and libraries.

The integration boundary is deliberately separate from the generated model
and the HemOnc toolkit. HemOnc concepts use HemOnc CUIs as their source
identities; resolving those CUIs through relationship-stage external codes to
OMOP ``concept_id`` values depends on vocabulary versions, mapping policy, and
the database arrangement. It therefore does not belong in ``toolkit.core`` or
``toolkit.analytics``.

The OMOP integration is exposed in ``hemonc_alchemy.integrations.omop``. That
submodule loads the optional ``omop-alchemy`` package lazily, so importing the
core package does not require OMOP to be installed.
"""
