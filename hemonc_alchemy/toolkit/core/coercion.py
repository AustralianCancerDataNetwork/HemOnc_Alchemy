"""Value coercion shared by model-facing toolkit queries."""

from __future__ import annotations

from enum import Enum

from ...naming import safe_enum_key


def coerce_enum_value[EnumValue: Enum](
    enum_type: type[EnumValue],
    value: object,
    label: str,
) -> EnumValue:
    """Convert a source-facing enum value to a generated enum member.

    Generated enum values use source values while their Python member names
    use :func:`safe_enum_key`. Accepting either spelling keeps query APIs
    convenient without weakening the generated model's enum typing.
    """
    if isinstance(value, enum_type):
        return value
    text = str(value).strip().lower()
    try:
        return enum_type(text)
    except ValueError:
        try:
            return enum_type[safe_enum_key(text)]
        except (KeyError, ValueError) as exc:
            raise ValueError(f"Unknown {label}: {value!r}") from exc
