"""
Data-dictionary-facing helpers: column normalisation and declared-type mapping.
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
