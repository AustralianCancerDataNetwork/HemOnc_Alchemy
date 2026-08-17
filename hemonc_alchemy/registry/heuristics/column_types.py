import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_integer_dtype,
    is_float_dtype,
)
from typing import Optional
import re

BOOLEAN_LIKE = {"true","false","t","f","yes","no","y","n","0","1"}

def detect_boolean(series: pd.Series) -> bool:
    """
    Robust detection of boolean / logical data, including:
    - pandas nullable boolean dtype
    - strings 'yes/no', '0/1', 'true/false'
    - numerics 0/1
    """

    # Real boolean dtype (pandas or pyarrow)
    if is_bool_dtype(series.dtype):
        return True

    # Semantic boolean detection
    vals = series.dropna().astype(str).str.strip().str.lower().unique()
    if len(vals) == 0:
        return False

    # Check semantic boolean set
    return set(vals).issubset(BOOLEAN_LIKE)

def detect_datetime(series: pd.Series) -> bool:
    """
    Detect any kind of datetime-ish column:
    - pandas datetime dtype
    - pyarrow timestamp
    - strings that consistently parse as dates (optional)
    """
    if is_datetime64_any_dtype(series.dtype):
        return True

    # PyArrow timestamps appear as "timestamp[us]" etc.
    if "timestamp" in str(series.dtype).lower():
        return True

    # Optional: heuristic for strings
    # Try parse a small sample
    sample = series.dropna().astype(str).head(5)
    for v in sample:
        try:
            pd.to_datetime(v)
            return True
        except Exception:
            pass

    return False

def detect_numeric(series: pd.Series) -> Optional[str]:
    """
    Return 'Integer', 'Float', or None.
    Works with numpy, pandas nullable, and pyarrow dtypes.
    """

    dt = str(series.dtype).lower()

    # True integer types (arrow uses int64[pyarrow], int32, etc.)
    if is_integer_dtype(series.dtype) or re.match(r"^int\d+\[", dt):
        return "Integer"

    # True float types (including arrow)
    if is_float_dtype(series.dtype) or re.match(r"^float\d+\[", dt):
        return "Float"

    return None
