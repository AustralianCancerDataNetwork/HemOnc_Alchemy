
from typing import Type, Any
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import Integer, Float, Boolean, DateTime, String, Text, Enum
import pandas as pd
import enum

def _to_enum_literal(enum_type: Type[enum.Enum], column_name: str, value: str) -> Any:
    """
    Reconstructs the enum literal string used by SQLAlchemy Enum fields.
    Example: "Person_GenderEnum.MALE"
    """
    
    key = "".join(ch if ch.isalnum() else "_" for ch in str(value)).upper()
    try:
        return enum_type[key]
    except KeyError:
        return None
    

def _to_bool(value: Any) -> bool | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if s in {"true", "t", "yes", "y", "1"}:
        return True
    if s in {"false", "f", "no", "n", "0"}:
        return False
    return None


def cast_value(model: Type[DeclarativeMeta], col_name: str, value: Any) -> Any:
    """
    Cast a raw CSV cell to the appropriate Python type based on the SQLAlchemy
    column type on the given model.

    - Integers -> int or None
    - Floats   -> float or None
    - Bool     -> True/False/None
    - DateTime -> pandas.Timestamp/datetime; parses strings via pandas.to_datetime
    - Enum     -> assumes value is already a valid enum string or underlying value
    - String/Text -> str or None
    """
    # Treat NA / pandas NA as None
    if value is None or pd.isna(value):
        return None

    column = model.__table__.columns[col_name] # type: ignore
    col_type = column.type
    return perform_cast(value, col_type)


def perform_cast(value: Any, col_type: Any) -> Any:

    # Integer
    if isinstance(col_type, Integer):
        try:
            return int(value)
        except (ValueError, TypeError):
            return -1

    # Float
    if isinstance(col_type, Float):
        try:
            return float(value)
        except (ValueError, TypeError):
            return -1.0

    # Boolean
    if isinstance(col_type, Boolean):
        return _to_bool(value)

    # DateTime
    if isinstance(col_type, DateTime):
        # if already datetime-like, accept
        if hasattr(value, "to_pydatetime"):
            return value.to_pydatetime()
        from datetime import datetime
        if isinstance(value, datetime):
            return value
        try:
            return pd.to_datetime(value).to_pydatetime()
        except Exception:
            return None

    if isinstance(col_type, Enum):
        # pass through because we handle this separately
        return value

    # String / Text
    if isinstance(col_type, (String, Text)):
        # Canonicalise numeric-looking identifiers
        try:
            # floats like 46096.0 → "46096"
            if isinstance(value, float) and value.is_integer():
                return str(int(value))

            # strings like "46096" or "46096.0"
            if isinstance(value, str):
                v = value.strip()
                if v.isdigit():
                    return str(int(v))
                try:
                    f = float(v)
                    if f.is_integer():
                        return str(int(f))
                except ValueError:
                    pass

            return str(value)

        except Exception:
            return str(value)
    # Fallback: leave as is
    return value
