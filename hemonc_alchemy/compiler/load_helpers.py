"""Data-dictionary-facing helpers: column normalisation and declared-type mapping.

Ported from hemonc_import/src/hemonc_import/registry_version/load_helpers.py
(175 lines) -- but only the two functions the compiler itself needs.

Deliberately NOT ported here: `load_csv_best`, `perform_cast`, `cast_value`,
`_to_bool`, `_to_enum_literal`. Those were runtime CSV-loading/casting
helpers (imported by hemonc_import's final_model/entity_base.py, not by
anything in registry_version's own build path), and per US-19/US-20 they're
being replaced at runtime by orm_loader's `loading_helpers`/`data.converters`
-- not ported verbatim into the compiler. Enum casting
(`_to_enum_literal`'s job) has no orm_loader equivalent and still needs a
HemOnc-specific home in `model/base.py`, fixed per US-22 (surface unknown
values instead of silently returning None) -- tracked there, not here.
"""

from __future__ import annotations

import pandas as pd


def norm_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Trim column labels without otherwise changing the input frame."""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def get_data_type(raw_type: str) -> str:
    """
    Map raw type string from data dictionary to standard type.
    """
    rt = raw_type.strip().lower()
    if "int" in rt:
        return "Integer"
    if "float" in rt or "double" in rt or "decimal" in rt:
        return "Float"
    if "date" in rt or "time" in rt:
        return "DateTime"
    if "bool" in rt or "logical" in rt:
        return "Boolean"
    if "uuid" in rt or "guid" in rt:
        return "UUID"
    if "enum" in rt or "categorical" in rt or "value set" in rt:
        return "Enum"
    return "String"
