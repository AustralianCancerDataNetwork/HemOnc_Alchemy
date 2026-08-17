from ..registry_model import ColumnSpec, EnumInfo, TableMeta
from ..heuristics import safe_enum_key
from .normalisation import generate_normalisation_blocks

SQLA_TYPE_MAP = {
    "Integer": "Integer",
    "Float": "Float",
    "Boolean": "Boolean",
    "DateTime": "DateTime",
    "String": "String",
    "Text": "Text",
    "Enum": "Enum",
}

def sqlalchemy_column(spec: ColumnSpec) -> str:
    sa_type = SQLA_TYPE_MAP[spec.dtype]

    args = [sa_type]

    if spec.primary_key:
        args.append("primary_key=True")

    if not spec.nullable:
        args.append("nullable=False")

    return f"mapped_column({', '.join(args)})"


def generate_enum_class(
    class_name: str,
    column: str,
    enum: EnumInfo,
) -> list[str]:
    enum_class = f"{class_name}_{column.capitalize()}Enum"

    lines = [f"class {enum_class}(enum.Enum):"]
    for value in enum.values:
        key = safe_enum_key(value)
        lines.append(f"    {key} = {value!r}")

    lines.append("")
    return lines


def _python_type(spec: ColumnSpec, enum_class: str | None) -> str:
    if spec.dtype == "Enum":
        t = enum_class
    else:
        t = {
            "Integer": "int",
            "Float": "float",
            "Boolean": "bool",
            "DateTime": "datetime",
            "String": "str",
            "Text": "str",
        }[spec.dtype]

    return f"Optional[{t}]" if spec.nullable else f'{t}'


def generate_column_line(
    spec: ColumnSpec,
    *,
    enum_class: str | None = None,
) -> str:
    sa_type = SQLA_TYPE_MAP[spec.dtype]

    if spec.dtype == "Enum":
        sa_type = f"Enum({enum_class})"

    args = [sa_type]

    if spec.primary_key:
        args.append("primary_key=True")

    if not spec.nullable:
        args.append("nullable=False")

    return f"    {spec.name}: Mapped[{_python_type(spec, enum_class)}] = mapped_column({', '.join(args)})"



def generate_entity(meta: TableMeta) -> tuple[list[str], list[str]]:

    class_lines: list[str] = []
    enum_lines: list[str] = []

    class_lines.append(f"class {meta.classname}(Base):")
    class_lines.append(f"    __tablename__ = {meta.name!r}")
    class_lines.append(f"    filename = {meta.filename!r}")
    class_lines.append("")

    for col, spec in sorted(meta.columns.items()): # type: ignore[attr-defined]
        # Derived columns: decide policy here
        if spec.derived:
            continue  # recommended default

        enum_class = None
        if spec.dtype == "Enum":
            enum_class = f"{meta.classname}_{col.capitalize()}Enum"
            enum_lines.extend(
                generate_enum_class(meta.classname, col, spec.enum) # type: ignore[arg-type]
            )

        class_lines.append(
            generate_column_line(spec, enum_class=enum_class)
        )

    class_lines.append("")
    return enum_lines, class_lines


def generate_models(registry: dict[str, TableMeta]) -> str:
    enum_blocks: list[str] = []
    entity_blocks: list[str] = []
    normalisation_blocks: list[str] = []
    for meta in sorted(registry.values(), key=lambda m: m.name):
        enums, entity = generate_entity(meta)
        enum_blocks.extend(enums)
        entity_blocks.extend(entity)

        normalisation_blocks.extend(generate_normalisation_blocks(meta))

    return "\n".join(
        [
            "from .entity_base import *",
            "",
            *enum_blocks,
            "",
            *entity_blocks,
            "",
            *normalisation_blocks,
        ]
    )
