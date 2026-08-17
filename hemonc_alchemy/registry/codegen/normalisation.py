from ..registry_model import TableMeta

def lookup_class_name(meta: TableMeta, col: str) -> str:
    return f"{meta.classname}_{col.capitalize()}"

def lookup_table_name(meta: TableMeta, col: str) -> str:
    return f"{meta.name}_{col}"

def map_class_name(meta: TableMeta, col: str) -> str:
    return f"{meta.classname}_{col.capitalize()}Map"

def map_table_name(meta: TableMeta, col: str) -> str:
    return f"{meta.name}_{col}_map"


def generate_lookup_and_map(
    meta: TableMeta,
    col: str,
) -> list[str]:

    pk_col = meta.pk_columns[0]  # matches your historical pattern
    lookup_cls = lookup_class_name(meta, col)
    map_cls = map_class_name(meta, col)

    lookup_tbl = lookup_table_name(meta, col)
    map_tbl = map_table_name(meta, col)

    lines: list[str] = []

    # Lookup table
    lines.extend([
        f"class {lookup_cls}(Base):",
        f"    __tablename__ = {lookup_tbl!r}",
        f"    {col}: Mapped[str] = mapped_column(String, primary_key=True)",
        "",
    ])

    # Mapping table
    lines.extend([
        f"class {map_cls}(Base):",
        f"    __tablename__ = {map_tbl!r}",
        f"    {pk_col}: Mapped[int] = mapped_column(",
        f"        ForeignKey('{meta.name}.{pk_col}'), primary_key=True)",
        f"    {col}: Mapped[str] = mapped_column(",
        f"        ForeignKey('{lookup_tbl}.{col}'), primary_key=True)",
        "",
    ])

    return lines

def generate_normalisation_blocks(meta: TableMeta) -> list[str]:
    blocks: list[str] = []

    for group in meta.normalisation_groups or []:
        if group.kind != "lookup":
            continue

        for col in group.columns:
            blocks.extend(generate_lookup_and_map(meta, col))

    return blocks
