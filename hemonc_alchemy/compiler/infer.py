"""
Turns a raw HemOnc data-dictionary column into the shape the generated
model needs: what SQL type it should be, whether it's really an enum,
whether it should be exploded into its own table, and what actually
identifies a row.

Most of this works from the real CSV data, in combination with the 
data dictionary declared types 

Handling notes:

- if a plain string column only holds a handful of distinct values it is treated as an enum candidate)
- a pipe-delimited free text field is denormalised into a child table 
- type detection reads the live data
- unique keys and identity keys are parsed from the data dictionary, which may have added annotations that need handling

"""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import pairwise

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)

from ..naming import PY_KEYWORDS, resolve_source_csv, safe_identifier  # noqa: F401

MAX_ENUM_UNIQUE = 20
MAX_STRING_INLINE = 100
BOOLEAN_LIKE = {"true", "false", "t", "f", "yes", "no", "y", "n", "0", "1"}

# Column headers from the data dictionary
CONTENT_COL = "Content Tables"
LOOKUP_COL = "Lookup and Metadata Tables"
MATURITY_COL = "Maturity"
UNIQUE_COL = "Unique Key"

# The dictionary workbook always has this exact filename inside a HemOnc
# data directory -- no need for callers to track a separate dictionary
# path alongside data_dir.
DICTIONARY_FILENAME = "data.dictionary.xlsx"


def looks_denormalised_text(series: pd.Series) -> bool:
    """Detect delimited text columns that likely need normalisation."""
    non_null = series.dropna().astype(str)
    if len(non_null) == 0:
        return False
    return any(("|" in v) or (";" in v) for v in non_null)


def max_string_length(series: pd.Series) -> int:
    """Return the maximum observed string length for a series."""
    non_null = series.dropna().astype(str)
    return int(non_null.str.len().max()) if len(non_null) else 0


def detect_boolean(series: pd.Series) -> bool:
    """
    Detection of boolean / logical data, including:
    - pandas nullable boolean dtype
    - strings 'yes/no', '0/1', 'true/false'
    - numerics 0/1
    """
    if is_bool_dtype(series.dtype):
        return True

    vals = series.dropna().astype(str).str.strip().str.lower().unique()
    if len(vals) == 0:
        return False

    return set(vals).issubset(BOOLEAN_LIKE)


def detect_datetime(series: pd.Series) -> bool:
    """
    Detect datetime columns:
    - native datetime dtype
    - pyarrow timestamp
    - string columns that mostly look like real dates (with separators)
    """
    if is_datetime64_any_dtype(series.dtype):
        return True

    if "timestamp" in str(series.dtype).lower():
        return True

    s = series.dropna().astype(str)
    if s.empty:
        return False

    sample = s.head(20)

    parsed = pd.to_datetime(sample, errors="coerce", format="ISO8601")
    ratio = parsed.notna().mean()

    if ratio < 0.8:
        return False

    looks_like_date = sample.str.contains(r"[-/:T]").mean()
    return looks_like_date >= 0.5


def detect_numeric(series: pd.Series) -> str | None:
    """
    Return 'Integer', 'Float', or None, based on the real values

    This doesn't handle placeholder text like "TBA" mixed into an
    otherwise-numeric column
    """
    dt = str(series.dtype).lower()

    if is_integer_dtype(series.dtype) or re.match(r"^int\d+\[", dt):
        return "Integer"

    if is_float_dtype(series.dtype) or re.match(r"^float\d+\[", dt):
        non_null = series.dropna()
        if len(non_null) > 0 and (non_null % 1 == 0).all():
            return "Integer"
        return "Float"

    return None


@dataclass
class EnumInfo:
    """Represents an enum candidate inferred from observed data values."""
    kind: str  # "normal" | "relationship"
    values: list[str]


def detect_enum(col_name: str, series: pd.Series) -> EnumInfo | None:
    """Infer a small inline enum from observed values, if one looks appropriate."""
    col_lower = col_name.lower()

    if any(n in col_lower for n in ["description", "date"]):
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
    """Convert an arbitrary display value into a safe enum member name."""
    s = raw.strip()

    s = s.replace("<", "LT_")
    s = s.replace(">", "GT_")
    s = s.replace("≤", "LE_")
    s = s.replace("≥", "GE_")

    s = s.replace(" to ", "_TO_")
    s = s.replace("-", "_TO_")
    s = s.replace("–", "_TO_")
    s = s.replace("/", "_")

    if re.match(r"^\d", s):
        s = "I_" + s

    s = re.sub(r"[^0-9a-zA-Z_]", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.upper()[:60]

    if s == "":
        s = "VALUE"

    return s.strip("_")


def parse_unique_key(value: str) -> list[str]:
    """
    Parse a workbook `Unique Key` or `Identity Key` cell into column names.

    These cells are written for a human reader, not a parser 
    
    things like `a + b + c`, `name or person_cui`, or `study_id (see note)` 
    show up in the real dictionary. 
    
    This is intentionally permissive about the `+`/`or` join syntax, and 
    strips parenthetical text before tokenizing so explanatory asides 
    or an inline list of alternatives like `"(Addition|Change|Deletion)"`
    don't get treated as column names.
    """
    text = value.strip()

    # Strip parenthetical text before anything else.
    text = re.sub(r"\(.*?\)", "", text)

    text = text.replace(" OR ", " or ")
    text = text.replace(" or ", " + ")

    parts = [p.strip() for p in text.split("+") if p.strip()]

    cols: list[str] = []
    for p in parts:
        for token in p.split():
            ident = re.sub(r"[^0-9a-zA-Z_]", "", str(token))
            if re.match(r"^[A-Za-z_]\w*$", ident):
                cols.append(ident)

    seen: set[str] = set()
    uniq: list[str] = []
    for c in cols:
        if c not in seen:
            seen.add(c)
            uniq.append(c)

    return [u.strip().lower() for u in uniq]


def infer_pipe_groups(
    df: pd.DataFrame,
    columns: list[str],
) -> list[list[str]]:
    """
    Group denormalised columns that appear to explode together row-by-row
    e.g. `biomarker2` and `biomarker2_finding`, where each pipe-delimited
    entry in one column lines up with the corresponding entry in the other.
    Paired columns like this share one exploded child table instead of two
    separate ones.
    """
    groups: list[list[str]] = []
    cols = sorted(columns)
    df = df.rename(columns=lambda c: safe_identifier(c).lower())
    for c1, c2 in pairwise(cols):
        if c1 in c2 or c2 in c1:
            s1: pd.Series = df[c1].fillna("").astype(str)
            s2: pd.Series = df[c2].fillna("").astype(str)

            if (s1.map(lambda x: len(x.split("|"))) == s2.map(lambda x: len(x.split("|")))).all():
                groups.append(sorted([str(c1), str(c2)]))
    return groups
