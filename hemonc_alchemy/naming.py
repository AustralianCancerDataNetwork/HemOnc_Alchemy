"""Identifier normalisation and source-file resolution shared across tiers.

Both the compiler (matching a table to its dictionary-declared CSV at
generation time) and the runtime loader (matching a generated entity to its
real CSV at load time) need the exact same answer to "which file on disk is
this table's data" -- HemOnc's own filenames don't always match a table's
name (punctuation gets added or dropped: `canonical.triples.csv` for
`canonicaltriples`). Two independent implementations of that matching
already drifted apart once before this rewrite (see compiler/infer.py's own
history) -- this module exists so there's exactly one, usable by both
`compiler/` and `toolbox/` without either needing to import the other
(`.importlinter`'s layers contract forbids `toolbox` from importing
`compiler`).

Deliberately dependency-free (no pandas, no project-internal imports) so it
sits below every layer in the `.importlinter` contract without needing to be
named in it at all -- the same role `config.py`/`errors.py` already play.
"""

from __future__ import annotations

import keyword
import re
from pathlib import Path

PY_KEYWORDS = set(keyword.kwlist)


def safe_identifier(name: str) -> str:
    """Return a normalised lowercase identifier safe for code and model fields."""
    if name == "":
        return "_"

    ident = re.sub(r"[^0-9a-zA-Z_]", "", str(name))

    if ident and ident[0].isdigit():
        ident = "_" + ident

    if not ident:
        ident = "_"

    if ident in PY_KEYWORDS:
        ident = ident + "_field"

    return ident.lower()


def resolve_source_csv(data_dir: Path, table_name: str) -> tuple[Path | None, list[str]]:
    """
    Find the real CSV backing `table_name` in `data_dir`.
    This tries progressively looser matches until exactly one file wins,
    excluding filenames containing "beta".

    Returns (path, ambiguous_matches). `path` is None if nothing resolved;
    `ambiguous_matches` is non-empty only when multiple candidates tied and
    the caller should treat that as an error rather than guess.
    """
    csvs = [p for p in sorted(data_dir.glob("*.csv")) if "beta" not in p.stem.lower()]

    exact = [p for p in csvs if p.stem == table_name]
    if len(exact) == 1:
        return exact[0], []
    if len(exact) > 1:
        return None, [p.name for p in exact]

    normalised = [p for p in csvs if safe_identifier(p.stem) == table_name]
    if len(normalised) == 1:
        return normalised[0], []
    if len(normalised) > 1:
        return None, [p.name for p in normalised]

    prefixed = [p for p in csvs if p.stem.lower().startswith(table_name.lower())]
    if len(prefixed) == 1:
        return prefixed[0], []
    if len(prefixed) > 1:
        return None, [p.name for p in prefixed]

    return None, []
