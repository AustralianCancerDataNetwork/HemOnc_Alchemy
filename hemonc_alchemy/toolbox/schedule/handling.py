"""
Dosing-schedule string parsing and resolution.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from .tokens import TOKEN_RE, Choice, Day, Indefinite, Range

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResolvedSchedule:
    """Result of resolving an `alldays` string: explicit days, plus whether
    the schedule continues indefinitely beyond them.
    """

    days: tuple[Day, ...] = ()
    indefinite: Indefinite | None = None

    def __iter__(self):
        return iter(self.days)

    def __len__(self) -> int:
        return len(self.days)

    def __bool__(self) -> bool:
        return bool(self.days) or self.indefinite is not None


def apply_sig_to_series(
    series: dict[int, float],
    days: list[Day],
    decay_days: int = 2,
    decay_factor: float = 0.5,
):
    """
    Mutates series in place.
    """
    for day in days:
        base = 0.5 if day.optional else 1.0
        d0 = day.value

        for offset in range(decay_days + 1):
            value = base * (decay_factor ** offset)
            series[d0 + offset] = max(series[d0 + offset], value)


def tokenize_all_days(value: str | None) -> list[str]:
    if not value:
        return []
    return [match.group(0).strip() for match in TOKEN_RE.finditer(value) if match.group(0).strip()]


def parse_choice(token: str) -> Choice:
    return Choice([int(part) for part in token.split("|") if part.strip()])


def parse_scalar_list(token: str):
    out = []
    for part in token.split(","):
        part = part.strip()
        if not part:
            continue
        if part.startswith("(") and part.endswith(")"):
            out.extend(parse_optional(part))
        elif "|" in part:
            out.append(parse_choice(part))
        else:
            out.append(Day(int(part)))
    return out


def parse_range(token: str):
    body = token[1:-1]
    parts = [part.strip() for part in body.split(",")]
    if len(parts) != 3:
        logger.warning("Unparseable range token %r (expected 3 comma-separated parts)", token)
        return []

    start, end, step = parts
    start = int(start) if start.lstrip("-").isdigit() else start
    end = int(end) if end.lstrip("-").isdigit() else end
    return [Range(start, end, int(step))]


def parse_optional(token: str):
    inner = token[1:-1]

    if inner.startswith("+"):
        match = re.fullmatch(r"\+([a-zA-Z])(\d+)?", inner)
        if not match:
            logger.warning("Unparseable indefinite-dosing token %r", token)
            return []
        kind = f"+{match.group(1).lower()}"
        max_days = int(match.group(2)) if match.group(2) else None
        return [Indefinite(kind, max_days)]

    return [Day(int(inner), optional=True)]


def parse_token(token: str):
    token = token.replace("^", "").strip()
    if not token or token == "<NA>":
        return []
    if token.startswith("U"):
        logger.warning("Unspecified-dosing token %r dropped", token)
        return []
    if token.startswith("[") and token.endswith("]"):
        return parse_range(token)
    if token.startswith("(") and token.endswith(")"):
        return parse_optional(token)
    return parse_scalar_list(token)


def expand(parsed) -> ResolvedSchedule:
    days: list[Day] = []
    indefinite: Indefinite | None = None

    for item in parsed:
        if isinstance(item, Day):
            days.append(item)
        elif isinstance(item, Choice):
            days.extend(Day(day) for day in item.options)
        elif isinstance(item, Range):
            if isinstance(item.start, int) and isinstance(item.end, int):
                for day in range(item.start, item.end + 1, item.step):
                    days.append(Day(day, optional=item.optional))
        elif isinstance(item, Indefinite):
            if indefinite is not None:
                logger.warning(
                    "Multiple indefinite-dosing markers in one schedule; keeping the first (%r), dropping %r",
                    indefinite, item,
                )
            else:
                indefinite = item
                logger.warning(
                    "Indefinite-dosing marker %r found (continue until progression/indefinitely); "
                    "explicit days list is not the complete schedule",
                    item,
                )

    return ResolvedSchedule(days=tuple(days), indefinite=indefinite)


def resolve_all_days(all_days: str | None) -> ResolvedSchedule:
    parsed = []
    for token in tokenize_all_days(all_days):
        parsed.extend(parse_token(token))
    return expand(parsed)
