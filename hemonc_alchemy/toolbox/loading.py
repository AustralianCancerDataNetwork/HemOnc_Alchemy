"""
Load a generated entity's primary rows from a real HemOnc data directory.

`EntityBase.load_csv()` (via orm-loader's `CSVLoadableTableInterface`,
already composed onto every generated entity) does the actual staged
ingestion.

HemOnc's own filenames don't always agree with the table name they belong
to requiring `naming.resolve_source_csv` compile-time workaround.
This module reuses the same resolver at load time, and satisfies 
orm-loader's filename check with a throwaway symlink rather than 
weakening the check itself.

`load_denormalised` handles pipe-delimited HemOnc columns that the 
compiler explodes into their own generated map tables (e.g. `Sigs.timing` 
-> `sigs_timing`, one row per pipe-delimited value) rather than a plain 
scalar column. `load_csv()` only ever populates an entity's own scalar 
columns -- it has no idea these child tables exist, since they're a 
HemOnc-specific convention with no orm-loader equivalent. This
must run *after* `load_entity` for the same entity: surrogate-PK ("content")
tables have no `id` in the source CSV at all (it's assigned on insert), so
resolving which parent row a denormalised value belongs to means looking
its declared natural key back up against the now-loaded parent table.
"""

from __future__ import annotations

import logging
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import sqlalchemy as sa
import sqlalchemy.orm as so

from ..model.base import register_enum_casts
from ..naming import resolve_source_csv, safe_identifier

logger = logging.getLogger(__name__)


@contextmanager
def _resolved_csv_path(data_dir: Path, table_name: str) -> Iterator[Path]:
    """Yield a path whose stem is guaranteed to equal `table_name`.

    Returns the real file directly when its own stem already matches
    (the common case). Otherwise symlinks it under a throwaway temp
    directory for the duration of the `with` block only.
    """
    real_path, ambiguous = resolve_source_csv(data_dir, table_name)
    if ambiguous:
        raise ValueError(f"Ambiguous CSV matches for table '{table_name}': {', '.join(ambiguous)}")
    if real_path is None:
        raise FileNotFoundError(f"No CSV found for table '{table_name}' in {data_dir}")

    if real_path.stem == table_name:
        yield real_path
        return

    with tempfile.TemporaryDirectory(prefix="hemonc_alchemy_load_") as tmp_dir:
        aliased = Path(tmp_dir) / f"{table_name}.csv"
        aliased.symlink_to(real_path.resolve())
        yield aliased


def load_entity(
    session: so.Session,
    entity_cls: type,
    data_dir: Path,
    **load_csv_kwargs,
) -> int:
    """Load one generated entity's primary rows from `data_dir`.

    Resolves the real source CSV (tolerating HemOnc's filename
    irregularities), then delegates entirely to `entity_cls.load_csv()` --
    staging, casting, merge strategy, everything -- without reimplementing
    any of it. `load_csv_kwargs` passes through unchanged (`merge_strategy`,
    `chunksize`, `dedupe`, etc.).
    """
    register_enum_casts()
    with _resolved_csv_path(data_dir, entity_cls.__tablename__) as path:
        return entity_cls.load_csv(session, path, **load_csv_kwargs)


def load_all(
    session: so.Session,
    entity_cls: type,
    data_dir: Path,
    **load_csv_kwargs,
) -> dict[str, int]:
    """Load one entity fully: primary rows, then its denormalised children.

    `load_denormalised` must run after the primary rows exist (surrogate-PK
    tables resolve each denormalised row back to a generated `id`), so this
    is the one call most callers actually want -- `load_entity`/
    `load_denormalised` stay available separately for callers that need
    finer-grained control (e.g. loading primary rows for every table first,
    then denormalised children in a second pass, to avoid FK-ordering
    surprises across entities).

    Returns `{"<tablename>": primary_row_count, **denorm_column_counts}`.
    """
    primary_total = load_entity(session, entity_cls, data_dir, **load_csv_kwargs)
    session.flush()
    denorm_totals = load_denormalised(session, entity_cls, data_dir)
    return {entity_cls.__tablename__: primary_total, **denorm_totals}


def _natural_key_columns(entity_cls: type) -> list[str]:
    """The real declared business/natural key for an entity.

    Not the same thing as `entity_cls.natural_key_columns` for a
    surrogate-PK ("content") table -- there, that attribute is the literal
    generated PK, `['id']`, which the source CSV doesn't even contain. The
    real natural key for those tables lives in a generated
    `UniqueConstraint` named `uq_{tablename}_natural_key`. Lookup tables
    have no surrogate id at all, so `natural_key_columns` already *is*
    their real PK and needs no further resolution.
    """
    table = entity_cls.__table__
    preferred_name = f"uq_{table.name}_natural_key"
    uniques = [c for c in table.constraints if isinstance(c, sa.UniqueConstraint)]
    preferred = next((u for u in uniques if u.name == preferred_name), None)
    if preferred is not None:
        return [col.name for col in preferred.columns]
    return list(entity_cls.natural_key_columns)


def _map_class_for_column(entity_cls: type, column: str) -> type:
    """Find the generated map (child) table class for one denormalised
    column via the entity's own declared `{column}_items` relationship,
    rather than re-deriving the compiler's `{Parent}_{Column}Map` naming
    convention independently -- one source of truth for the mapping.
    """
    rel_name = f"{column}_items"
    relationship_prop = sa.inspect(entity_cls).relationships.get(rel_name)
    if relationship_prop is None:
        raise LookupError(
            f"{entity_cls.__name__} has no relationship '{rel_name}' for denormalised column '{column}'"
        )
    return relationship_prop.mapper.class_


def _read_source_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str)
    return df.rename(columns=lambda c: safe_identifier(c).lower())


def load_denormalised(
    session: so.Session,
    entity_cls: type,
    data_dir: Path,
) -> dict[str, int]:
    """Explode every denormalised column of `entity_cls` into its generated
    map tables, from the real HemOnc CSV -- must run after `load_entity`
    for the same entity and data_dir.

    Returns a dict of `{column_name: rows_loaded}`.

    Scalar casting reuses `perform_cast` (the same mechanism `load_csv`
    itself uses), so a bad value in a denormalised column is dropped with
    a warning rather than defaulted to a sentinel -- consistent with
    US-20. Enum-typed denormalised columns (several map tables have them,
    e.g. `indications_biomarker2.biomarker2`) get the same validated
    casting as any other enum column, via `register_enum_casts` (US-22).
    """
    from orm_loader.loaders.data.converters import perform_cast
    from orm_loader.loaders.data_classes import TableCastingStats

    register_enum_casts()

    if not entity_cls.denormalised_columns:
        return {}

    with _resolved_csv_path(data_dir, entity_cls.__tablename__) as path:
        df = _read_source_csv(path)

    key_cols = [c for c in _natural_key_columns(entity_cls) if c in df.columns]
    is_surrogate = hasattr(entity_cls, "id")

    parent_lookup: dict[tuple[str, ...], int] = {}
    if is_surrogate:
        if not key_cols:
            raise RuntimeError(
                f"{entity_cls.__name__} has a surrogate id but no usable natural key columns "
                "found in its source CSV -- cannot resolve denormalised rows to a parent id."
            )
        rows = session.execute(sa.select(entity_cls.id, *(getattr(entity_cls, c) for c in key_cols))).all()
        parent_lookup = {tuple(str(v) for v in row[1:]): row[0] for row in rows}

    results: dict[str, int] = {}
    for column in entity_cls.denormalised_columns:
        if column not in df.columns:
            continue

        map_cls = _map_class_for_column(entity_cls, column)
        value_type = map_cls.__table__.c[column].type
        stats = TableCastingStats(table_name=map_cls.__tablename__)

        seen: set[tuple] = set()
        records: list[dict] = []
        for _, row in df.iterrows():
            raw = row.get(column)
            if raw is None or (isinstance(raw, float) and pd.isna(raw)):
                continue

            if is_surrogate:
                key = tuple(str(row[c]) for c in key_cols)
                parent_id = parent_lookup.get(key)
                if parent_id is None:
                    continue
                fixed_fields = {"parent_id": parent_id}
            else:
                fixed_fields = {c: row[c] for c in key_cols}

            for token in str(raw).split("|"):
                token = token.strip()
                if not token:
                    continue

                value = perform_cast(
                    token,
                    value_type,
                    on_error=lambda v, _col=column, _stats=stats: _stats.record(column=_col, value=v),
                    table_name=map_cls.__tablename__,
                    column_name=column,
                )
                if value is None:
                    continue

                dedupe_key = (*fixed_fields.values(), value)
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)

                records.append({**fixed_fields, column: value})

        # A single bulk insert per column rather than one `session.merge()`
        # per exploded value -- `merge()` is a SELECT-then-insert/update
        # round trip *per row*, and denormalised columns routinely explode
        # into tens of thousands of values across a real HemOnc table.
        # Deduping into `records` above already makes a plain insert safe;
        # nothing here needs merge's update-if-exists behaviour.
        if records:
            session.execute(sa.insert(map_cls.__table__), records)

        if stats.has_failures():
            for col_name, col_stats in stats.columns.items():
                logger.warning(
                    "CAST %s.%s: %d row(s) failed. Examples: %s",
                    map_cls.__tablename__,
                    col_name,
                    col_stats.count,
                    col_stats.examples,
                )

        results[column] = len(records)

    session.flush()
    return results
