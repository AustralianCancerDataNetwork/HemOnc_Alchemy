"""
Build a Registry from the HemOnc data dictionary and render the model.

This is the path from data dictionary to generated code.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .infer import (
    CONTENT_COL,
    DICTIONARY_FILENAME,
    LOOKUP_COL,
    MATURITY_COL,
    UNIQUE_COL,
    parse_unique_key,
    safe_identifier,
)
from .schema_model import Registry, TableMeta, save_registry_json


def build_registry(dictionary_path: Path) -> Registry:
    """Build a `Registry` from the workbook's `Content` and `Lookup` sheets."""
    content_df = pd.read_excel(dictionary_path, sheet_name="Content")
    lookup_df = pd.read_excel(dictionary_path, sheet_name="Lookup")

    tables = []
    for content_col, df in {CONTENT_COL: content_df, LOOKUP_COL: lookup_df}.items():
        name_map = {
            content_col: "name",
            MATURITY_COL: "maturity",
            "Description": "description",
            UNIQUE_COL: "unique_key",
        }
        if "Identity Key" in df.columns:
            name_map["Identity Key"] = "identity_key"

        columns = df.rename(columns=name_map)[list(name_map.values())].to_dict(orient="records")
        for col in columns:
            c = {k: v.strip() if isinstance(v, str) else v for k, v in col.items()}
            c["name"] = safe_identifier(c["name"])
            c["pk_columns"] = parse_unique_key("" if pd.isna(c.get("unique_key")) else str(c["unique_key"]))
            c["identity_keys"] = parse_unique_key("" if pd.isna(c.get("identity_key")) else str(c["identity_key"]))
            c["kind"] = "content" if content_col == CONTENT_COL else "lookup"
            tables.append(TableMeta(**{k: v for k, v in c.items() if k in TableMeta.__annotations__}))

    return Registry(tables={t.name: t for t in tables})


def regenerate(
    data_dir: Path,
    output_dir: Path,
) -> Registry:
    """
    Regenerate model/entities.py, model/enums.py, and the interim JSON
    registry snapshot. Does NOT validate or diff.
    """
    dictionary_path = data_dir / DICTIONARY_FILENAME
    registry = build_registry(dictionary_path)
    registry.enrich_table_metadata(dictionary_path)
    registry.finalise_table_metadata_from_data(data_dir)

    entities_code, enums_code = registry.render_sa_models()

    (output_dir / "entities.py").write_text(entities_code, encoding="utf-8")
    (output_dir / "enums.py").write_text(enums_code, encoding="utf-8")
    save_registry_json(registry, output_dir.parent / "schema" / "registry.json")

    return registry
