"""Lazy binding to ``omop-alchemy``'s public CDM models.

The optional dependency is imported only when a caller enters this bridge.
Normal HemOnc imports therefore remain valid in installations without the
``omop`` extra.  The returned binding carries a per-statement
``schema_translate_map`` so the public OMOP classes, whose tables are
intentionally schema-neutral, can be used against a configured schema while a
session remains bound to the HemOnc database.

The package's own queries are limited to HemOnc-specific joins that
``omop-alchemy`` cannot know about.  OMOP model classes and their public
validity/standardness expressions remain the source of truth for OMOP-side
semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sqlalchemy as sa


@dataclass(frozen=True)
class OmopBinding:
    """Public OMOP Alchemy models plus the schema routing for a session."""

    schema: str
    concept: Any
    concept_relationship: Any
    vocabulary: Any
    concept_ancestor: Any
    relationship: Any
    schema_translate_map: dict[str | None, str | None]

    def apply(self, statement: sa.Select) -> sa.Select:
        """Route this statement's schema-neutral OMOP tables to ``schema``."""

        return statement.execution_options(
            schema_translate_map=self.schema_translate_map
        )


def load_omop_binding(*, schema: str = "omop") -> OmopBinding | None:
    """Load public OMOP models lazily, returning ``None`` if extra is absent.

    ``omop-alchemy``'s own ``ResolvedCDMDatabase.schema_translate_map`` uses
    the same convention.  We reproduce only that small, public execution
    option here because the caller's session is usually already bound to the
    HemOnc database.
    """

    if not schema:
        return None
    try:
        from omop_alchemy.cdm.model import (
            Concept,
            Concept_Ancestor,
            Concept_Relationship,
            Relationship,
            Vocabulary,
        )
    except ImportError:
        return None
    return OmopBinding(
        schema=schema,
        concept=Concept,
        concept_relationship=Concept_Relationship,
        vocabulary=Vocabulary,
        concept_ancestor=Concept_Ancestor,
        relationship=Relationship,
        schema_translate_map={None: schema, "vocab": schema},
    )


def omop_available(
    session: Any,
    *,
    schema: str = "omop",
) -> bool:
    """Return whether the optional extra and ``schema.concept`` are usable.

    Missing extras, missing schemas, permissions, connection failures, and
    incompatible OMOP installations all return ``False``.  This deliberately
    performs a harmless model query rather than reflecting database metadata.
    """

    binding = load_omop_binding(schema=schema)
    if binding is None:
        return False
    try:
        statement = binding.apply(
            sa.select(binding.concept.concept_id).limit(1)
        )
        session.execute(statement).first()
        return True
    except Exception:  # noqa: BLE001 - availability must never break callers
        return False


__all__ = ["OmopBinding", "load_omop_binding", "omop_available"]
