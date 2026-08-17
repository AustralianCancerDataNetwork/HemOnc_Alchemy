
import re
import pandas as pd
from typing import Optional
from .column_types import detect_boolean
from ..registry_model import EnumInfo


MAX_ENUM_UNIQUE = 20
MAX_STRING_INLINE = 100

def max_string_length(series: pd.Series) -> int:
    non_null = series.dropna().astype(str)
    return int(non_null.str.len().max()) if len(non_null) else 0

def detect_enum(col_name: str, series: pd.Series) -> Optional[EnumInfo]:

    col_lower = col_name.lower()

    if any([n in col_lower for n in ["description", "date"]]):
        return None

    non_null = series.dropna()
    uniques_raw = non_null.unique()
    uniques = [str(v).strip() for v in uniques_raw]

    if len(uniques) <= 1 or len(uniques) > MAX_ENUM_UNIQUE:
        return None
    
    max_len = max_string_length(series)
    if max_len > MAX_STRING_INLINE:
        return None

    if detect_boolean(series):
        return None

    if any(re.match(r"^\d", u) for u in uniques):
        return None

    if any(("|" in u) or (";" in u) for u in uniques):
        return None

    if all(u.startswith("Has") for u in uniques):
        return EnumInfo(kind="relationship", values=uniques)

    return EnumInfo(kind="normal", values=uniques)



def safe_enum_key(raw: str) -> str:
    """
    Convert an arbitrary string ('<200', '75 to 200', '200', '3-12', '10/14')
    into a valid, unique Python enum member name.
    """

    # normalise whitespace & punctuation
    s = raw.strip()

    # special tokens
    s = s.replace("<", "LT_")
    s = s.replace(">", "GT_")
    s = s.replace("≤", "LE_")
    s = s.replace("≥", "GE_")

    # replace range indicators
    s = s.replace(" to ", "_TO_")
    s = s.replace("-", "_TO_")
    s = s.replace("–", "_TO_")
    s = s.replace("/", "_")

    # remove remaining illegal characters
    s = re.sub(r"[^0-9a-zA-Z_]", "_", s)

    # no leading digit
    if re.match(r"^\d", s):
        s = "_" + s

    # collapse duplicate underscores
    s = re.sub(r"_+", "_", s)

    # uppercase
    s = s.upper()

    # fallback if empty
    if s == "":
        s = "VALUE"

    return s
