
from dataclasses import dataclass
from typing import Literal, Any

ColumnChange = Literal[
    "added",
    "removed",
    "type_changed",
    "enum_changed",
    "nullability_changed",
    "pk_changed",
    "derived_changed",
]

@dataclass
class ColumnDiff:
    table: str
    column: str
    change: ColumnChange
    before: Any | None
    after: Any | None


@dataclass
class TableDiff:
    table: str
    column_diffs: list[ColumnDiff]
    pk_changed: bool = False
    identity_keys_changed: bool = False


@dataclass
class RegistryDiff:
    added_tables: list[str]
    removed_tables: list[str]
    table_diffs: list[TableDiff]

    def is_empty(self) -> bool:
        return (
            not self.added_tables
            and not self.removed_tables
            and not self.table_diffs
        )

    def to_text(self) -> str:
        lines: list[str] = []

        for t in self.added_tables:
            lines.append(f"+ TABLE {t}")

        for t in self.removed_tables:
            lines.append(f"- TABLE {t}")

        for td in self.table_diffs:
            lines.append(f"\nTABLE {td.table}")

            if td.pk_changed:
                lines.append("  * primary key changed")

            if td.identity_keys_changed:
                lines.append("  * identity keys changed")

            for cd in td.column_diffs:
                lines.append(
                    f"  - column {cd.column}: {cd.change}"
                )
                if cd.before is not None or cd.after is not None:
                    lines.append(f"      before: {cd.before}")
                    lines.append(f"      after : {cd.after}")

        return "\n".join(lines)
