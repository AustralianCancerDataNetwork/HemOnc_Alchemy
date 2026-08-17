from __future__ import annotations

from ..registry_model import TableMeta, ColumnSpec, EnumInfo
from .diff_model import ColumnDiff, TableDiff, RegistryDiff

def _enum_changed(old: EnumInfo | None, new: EnumInfo | None) -> bool:
    if old is None and new is None:
        return False
    if old is None or new is None:
        return True
    return old.values != new.values or old.kind != new.kind


def _enum_snapshot(enum: EnumInfo | None) -> dict | None:
    if enum is None:
        return None
    return {
        "kind": enum.kind,
        "values": list(enum.values),
    }


def _column_snapshot(spec: ColumnSpec | None) -> dict | None:
    if spec is None:
        return None
    return {
        "dtype": spec.dtype,
        "nullable": spec.nullable,
        "primary_key": spec.primary_key,
        "derived": spec.derived,
        "enum": _enum_snapshot(spec.enum),
    }


def diff_registries(
    old: dict[str, TableMeta],
    new: dict[str, TableMeta],
) -> RegistryDiff:
    old_tables = set(old)
    new_tables = set(new)

    added_tables = sorted(new_tables - old_tables)
    removed_tables = sorted(old_tables - new_tables)

    table_diffs: list[TableDiff] = []

    for table in sorted(old_tables & new_tables):
        old_meta = old[table]
        new_meta = new[table]

        column_diffs: list[ColumnDiff] = []

        old_cols = old_meta.columns or {}
        new_cols = new_meta.columns or {}

        all_columns = set(old_cols) | set(new_cols)

        for col in sorted(all_columns):
            old_spec = old_cols.get(col)
            new_spec = new_cols.get(col)

            # Column added
            if old_spec is None:
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="added",
                        before=None,
                        after=_column_snapshot(new_spec),
                    )
                )
                continue

            # Column removed
            if new_spec is None:
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="removed",
                        before=_column_snapshot(old_spec),
                        after=None,
                    )
                )
                continue

            # Type change
            if old_spec.dtype != new_spec.dtype:
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="type_changed",
                        before=old_spec.dtype,
                        after=new_spec.dtype,
                    )
                )

            # Enum change
            if _enum_changed(old_spec.enum, new_spec.enum):
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="enum_changed",
                        before=_enum_snapshot(old_spec.enum),
                        after=_enum_snapshot(new_spec.enum),
                    )
                )

            # Nullability change
            if old_spec.nullable != new_spec.nullable:
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="nullability_changed",
                        before=old_spec.nullable,
                        after=new_spec.nullable,
                    )
                )

            # Primary key change
            if old_spec.primary_key != new_spec.primary_key:
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="pk_changed",
                        before=old_spec.primary_key,
                        after=new_spec.primary_key,
                    )
                )

            # Derived flag change
            if old_spec.derived != new_spec.derived:
                column_diffs.append(
                    ColumnDiff(
                        table=table,
                        column=col,
                        change="derived_changed",
                        before=old_spec.derived,
                        after=new_spec.derived,
                    )
                )

        pk_changed = old_meta.pk_columns != new_meta.pk_columns
        identity_changed = old_meta.identity_keys != new_meta.identity_keys

        if column_diffs or pk_changed or identity_changed:
            table_diffs.append(
                TableDiff(
                    table=table,
                    column_diffs=column_diffs,
                    pk_changed=pk_changed,
                    identity_keys_changed=identity_changed,
                )
            )

    return RegistryDiff(
        added_tables=added_tables,
        removed_tables=removed_tables,
        table_diffs=table_diffs,
    )
