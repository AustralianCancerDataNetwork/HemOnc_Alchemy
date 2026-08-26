"""Loading a HemOnc CSV extract into the database.

`load_all` is usually what you want: it loads an entity's own rows and then
its child tables, in that order.

Two things about the extract need handling before the rows go in. Filenames
don't always match the table they hold (`canonical_triples.csv` for the
`canonicaltriples` table), and neither do column headers (`parameter-based`
for `parameterbased`, `class` for `class_field`). Both are reconciled here so
the source files can stay exactly as HemOnc ships them.

Columns holding several pipe-delimited values in one cell live in their own
child tables rather than as a single string, and `load_denormalised` fills
those. It has to run after the parent rows exist, because a child row is
matched back to its parent by the parent's natural key.
"""

from __future__ import annotations

import csv
import logging
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import sqlalchemy as sa
import sqlalchemy.orm as so

from ..model.base import register_enum_casts
from ..naming import resolve_source_csv, safe_identifier

logger = logging.getLogger(__name__)


def _header_renames(path: Path) -> dict[str, str]:
    """Source headers that don't already match their generated column name.

    Six extracts need this, `sigs` and `indications` among them: a header may
    contain dots or hyphens (`seq.rel.when`, `parameter-based`) or be a Python
    keyword (`class`, `with`), none of which survive into a column name.

    Case-only differences are excluded, since those already match.
    """
    with path.open(newline="", encoding="utf-8-sig") as handle:
        header = next(csv.reader(handle), [])

    renames: dict[str, str] = {}
    for raw in header:
        normalised = safe_identifier(raw).lower()
        if raw.strip().lower() != normalised:
            renames[raw] = normalised
    return renames


@contextmanager
def _resolved_csv_path(data_dir: Path, table_name: str) -> Generator[Path, None, None]:
    """Yield a CSV whose filename and headers both match the model.

    The real file is used untouched when it already matches. Otherwise it is
    presented through a temporary directory for the duration of the `with`
    block, as a symlink if only the name differs or a rewritten copy if the
    headers do too. The original is never modified, and rewriting streams row
    by row so extract size doesn't matter.
    """
    real_path, ambiguous = resolve_source_csv(data_dir, table_name)
    if ambiguous:
        raise ValueError(f"Ambiguous CSV matches for table '{table_name}': {', '.join(ambiguous)}")
    if real_path is None:
        raise FileNotFoundError(f"No CSV found for table '{table_name}' in {data_dir}")

    renames = _header_renames(real_path)

    if real_path.stem == table_name and not renames:
        yield real_path
        return

    with tempfile.TemporaryDirectory(prefix="hemonc_alchemy_load_") as tmp_dir:
        staged = Path(tmp_dir) / f"{table_name}.csv"

        if not renames:
            staged.symlink_to(real_path.resolve())
            yield staged
            return

        logger.debug(
            "%s: normalising %d source header(s) for load: %s",
            table_name, len(renames), ", ".join(f"{k!r}->{v!r}" for k, v in renames.items()),
        )
        with (
            real_path.open(newline="", encoding="utf-8-sig") as source,
            staged.open("w", newline="", encoding="utf-8") as target,
        ):
            reader = csv.reader(source)
            writer = csv.writer(target)
            header = next(reader, [])
            writer.writerow([renames.get(col, col.strip()) for col in header])
            writer.writerows(reader)

        yield staged


def load_entity(
    session: so.Session,
    entity_cls: type,
    data_dir: Path,
    **load_csv_kwargs,
) -> int:
    """Load one entity's own rows, without its child tables.

    Extra keyword arguments (`merge_strategy`, `chunksize`, `dedupe`, ...) are
    passed through to the underlying loader.
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
    """Load one entity completely: its own rows, then its child tables.

    Returns a count per table loaded. Use `load_entity` and
    `load_denormalised` separately if you need every entity's own rows in
    place before any child tables are filled.
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
    """Fill the child tables holding an entity's pipe-delimited columns.

    Must run after `load_entity` for the same entity. Returns a count per
    column loaded.

    Values are cast the same way `load_csv` casts them, so a bad value is
    dropped with a warning rather than replaced by a sentinel, and an enum
    column in a map table is validated like any other.
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
