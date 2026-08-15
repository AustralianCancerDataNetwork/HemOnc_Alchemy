"""Dosing-schedule token grammar.

Ported verbatim from hemonc_import's final_model/definitions.py — pure
dataclasses and a regex, no entity dependency, so this is portable ahead of
the compiler/model-generation work. Route-classification vocabulary has been
split out to routes.py (see that module for why) rather than living here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Day:
    value: int
    optional: bool = False


@dataclass(frozen=True)
class Choice:
    options: list[int]


@dataclass(frozen=True)
class Range:
    start: int | str  # int or "EOC"
    end: int | str
    step: int
    optional: bool = False


@dataclass(frozen=True)
class Indefinite:
    kind: str  # "+n" or "+c"
    max_days: int | None = None


TOKEN_RE = re.compile(
    r"""
    (\[[^\]]*\])        |  # [ ... ] blocks
    ([^[]+)                # everything else (outside brackets)
    """,
    re.VERBOSE,
)
