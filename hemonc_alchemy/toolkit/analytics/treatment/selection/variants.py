"""Inspectable and executable variant selection APIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sqlalchemy as sa
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from .....model import Variants
from .components import build_component_statement, component_search_predicate
from .specs import CategoryMapping, TreatmentSelectionSpec


@dataclass(frozen=True)
class VariantQueryArtifacts:
    """The stages of a treatment query, retained for inspection and testing."""

    components: Select
    categorized_components: Any
    variant_ids: Any
    variants: Select


def _categorized_components(
    components: Select,
    category_mapping: CategoryMapping | None,
) -> Any:
    from .components import _category_expression

    source = components.subquery("treatment_components")
    return select(
        source,
        _category_expression(source, category_mapping),
    ).subquery("categorized_components")


def build_variant_query_artifacts(
    spec: TreatmentSelectionSpec,
    *,
    category_mapping: CategoryMapping | None = None,
) -> VariantQueryArtifacts:
    """Build inspectable component, grouping, and final variant statements."""
    components = build_component_statement(spec, category_mapping=category_mapping)
    categorized = _categorized_components(components, category_mapping)

    predicates = []
    for requirement in spec.component_requirements:
        predicates.append(
            sa.func.count(sa.distinct(categorized.c.sig_id)).filter(
                component_search_predicate(categorized, requirement)
            )
            >= 1
        )
    for requirement in spec.category_requirements:
        count = sa.func.count(sa.distinct(categorized.c.sig_id)).filter(
            categorized.c.broad_category == requirement.category
        )
        predicates.append(
            count == requirement.amount
            if requirement.match == "exact"
            else count >= requirement.amount
        )

    variant_ids = (
        select(categorized.c.variant_id)
        .group_by(categorized.c.variant_id)
        .having(sa.and_(*predicates) if predicates else sa.true())
        .subquery("matching_variant_ids")
    )
    variants = select(Variants).join(
        variant_ids,
        variant_ids.c.variant_id == Variants.id,
    )
    return VariantQueryArtifacts(
        components=components,
        categorized_components=categorized,
        variant_ids=variant_ids,
        variants=variants,
    )


def build_variant_statement(
    spec: TreatmentSelectionSpec,
    *,
    category_mapping: CategoryMapping | None = None,
) -> Select:
    """Build a statement returning selected ``Variants`` ORM rows."""
    return build_variant_query_artifacts(
        spec,
        category_mapping=category_mapping,
    ).variants


def select_variants(
    session: Session,
    spec: TreatmentSelectionSpec,
    *,
    category_mapping: CategoryMapping | None = None,
) -> list[Variants]:
    """Execute :func:`build_variant_statement` and return selected variants."""
    return session.execute(
        build_variant_statement(spec, category_mapping=category_mapping)
    ).unique().scalars().all()
