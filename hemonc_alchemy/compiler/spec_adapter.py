"""HemOnc TableSpec/FieldSpec adapter over orm_loader.registry.validation (US-21).

New in this rewrite — not a port of anything in hemonc_import. orm_loader's
`registry.ModelRegistry`/`ModelDescriptor.from_model` and its four
always-on validators (`ColumnPresenceValidator`, `ColumnNullabilityValidator`,
`PrimaryKeyValidator`, `ForeignKeyShapeValidator`) already implement "does
the generated ORM model match its declared spec" — today coupled to
OMOP-style CSV specs (`load_table_specs`/`load_field_specs` read
`cdmTableName`/`cdmFieldName`/`isRequired` columns from a CSV). The
`Validator` protocol itself is spec-format-agnostic, and orm_loader's own
docstring flags exactly this gap: "TODO: support generalised specification
formats via LinkML or similar."

hemonc-alchemy's "spec" is not a CSV -- it's the `Registry` built by
compiler/schema_model.py, itself derived from the real HemOnc data
dictionary. This module builds TableSpec/FieldSpec directly from that
Registry and hands them to orm_loader's existing validators, rather than
reimplementing validator plumbing.

Lives in compiler/, not loaders/: this is fundamentally "does the compiled
schema match the generated model" (an author-facing, US-8 validation
concern), not a runtime loading concern. The `.importlinter` layers
contract (cli > compiler > toolbox > model) would forbid a `loaders`-tier
module from importing `compiler.schema_model` anyway, and there was never
any real content that needed to live in loaders/ once vocab_load.py was
dropped (its only other candidate, EntityBase's orm-loader composition,
already lives in model/base.py) -- so that empty package was removed
rather than kept around for one module that belongs elsewhere.
"""

from __future__ import annotations

from orm_loader.registry import (
    FieldSpec,
    ModelRegistry,
    TableSpec,
    ValidationRunner,
    always_on_validators,
)
from orm_loader.registry.validation_report import ValidationReport

from .schema_model import Registry as SchemaRegistry


def hemonc_table_specs(registry: SchemaRegistry) -> dict[str, TableSpec]:
    """Build orm_loader TableSpec objects directly from a hemonc-alchemy
    schema Registry -- the "generalised specification format" orm_loader's
    own ModelRegistry docstring flags as unsupported (CSV-only today).

    Only tables that actually produced an entity class (`meta.columns`
    non-empty) get a spec; the rest have no generated model to validate.
    `is_required` mirrors HemOnc's own `maturity` field (prod == required),
    the closest real analogue to OMOP's isRequired convention.
    """
    return {
        name: TableSpec(
            table_name=name,
            schema="hemonc",
            is_required=meta.maturity == "prod",
            description=meta.description,
        )
        for name, meta in registry.tables.items()
        if meta.columns
    }


def hemonc_field_specs(registry: SchemaRegistry) -> dict[str, dict[str, FieldSpec]]:
    """Build orm_loader FieldSpec objects from a hemonc-alchemy schema Registry.

    Mirrors compiler/schema_model.py's own table_class() rendering rules so
    the spec actually matches what gets generated, not a naive reading of
    TableMeta:
    - denormalised/derived columns are excluded (table_class() skips them
      too -- they aren't rendered as scalar columns at all, see
      schema_model.py:695-696).
    - for surrogate-PK ("content") tables, the real primary key is the
      generated `id` column, not the natural key in `pk_columns` (that's
      only a UniqueConstraint) -- marking pk_columns as is_primary_key here
      would make every natural-key column show up as
      PRIMARY_KEY_MISSING_FROM_MODEL against the real generated PK.
    - HemOnc's soft relationships are viewonly, primaryjoin-based, and
      never declared as a real SQLAlchemy ForeignKey (see
      model/relationships.py) -- is_foreign_key is always False here.
    """
    out: dict[str, dict[str, FieldSpec]] = {}

    for table_name, meta in registry.tables.items():
        if not meta.columns:
            continue

        uses_surrogate = meta.use_surrogate_pk and meta.kind == "content"
        effective_pk = {"id"} if uses_surrogate else set(meta.pk_columns)

        fields: dict[str, FieldSpec] = {}
        for col_name, col in meta.columns.items():
            if col_name in meta.denormalised_columns or col_name in meta.derived_columns:
                continue
            fields[col_name] = FieldSpec(
                table_name=table_name,
                field_name=col_name,
                data_type=col.type,
                is_required=not col.nullable,
                is_primary_key=col_name in effective_pk,
                is_foreign_key=False,
                fk_table=None,
                fk_field=None,
            )

        if uses_surrogate:
            fields["id"] = FieldSpec(
                table_name=table_name,
                field_name="id",
                data_type="BigInteger",
                is_required=True,
                is_primary_key=True,
                is_foreign_key=False,
                fk_table=None,
                fk_field=None,
            )

        out[table_name] = fields

    return out


def build_model_registry(
    schema_registry: SchemaRegistry,
    models: list[type],
    *,
    model_version: str,
) -> ModelRegistry:
    """Construct an orm_loader ModelRegistry from a hemonc-alchemy schema
    Registry and a list of live, mapped ORM classes.

    `models` is passed in rather than imported here so this module stays
    decoupled from `model/entities.py` -- the caller (compiler/validate.py)
    already has to import it to get real classes for `ModelDescriptor.from_model`
    (which requires an actually-mapped class, not just parsed AST), so there's
    no reason for this adapter to import it too.
    """
    registry = ModelRegistry(model_version=model_version, model_name="HemOnc")

    # orm_loader's public API (`load_table_specs`) only reads CSV files.
    # Setting these "private" attributes directly is filling the documented
    # gap in ModelRegistry's own docstring ("TODO: support generalised
    # specification formats via LinkML or similar"), not working around a
    # considered design decision.
    registry._table_specs = hemonc_table_specs(schema_registry)
    registry._field_specs = hemonc_field_specs(schema_registry)

    registry.register_models(models)
    return registry


def validate_with_orm_loader(
    schema_registry: SchemaRegistry,
    models: list[type],
    *,
    model_version: str = "unversioned",
) -> ValidationReport:
    """Run orm_loader's always-on validators against the generated model.

    A stronger, more structural check than compiler/validate.py's own
    ast/dataclass-level checks: this one requires the generated model to
    actually import and map correctly first, and validates PK/FK/nullability
    shape via the same battle-tested validators omop-alchemy uses.

    `model_version` has no real value to pass yet -- HemOnc's data
    dictionary isn't itself versioned in a way this project tracks (see
    _design/hemonc-alchemy-spec.md's open questions); "unversioned" is a
    placeholder pending that decision, not a considered value.
    """
    registry = build_model_registry(schema_registry, models, model_version=model_version)
    runner = ValidationRunner(validators=always_on_validators())
    return runner.run(registry)
