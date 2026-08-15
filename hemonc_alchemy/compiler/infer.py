"""Type/enum/natural-key/denormalisation inference from the HemOnc data dictionary.

Ported from hemonc_import/src/hemonc_import/registry_version/infer.py (326
lines), with three confirmed bugs fixed during the port (empirically
validated against the real data dictionary — see hemonc_import's
_design/refactor-followups.md §4):

- `parse_unique_key`: previously claimed (in its own docstring) to strip
  parenthetical explanatory text but didn't. Two real cases were affected:
  `sequencetable`'s `"(complex)"` produced a fabricated `'complex'`
  pseudo-column, and `changelog`'s
  `"Date + Type + Affected Table + (Addition|Change|Deletion)"` fused the
  parenthetical alternatives into one garbage token
  `'additionchangedeletion'`. Fixed by stripping `(...)` before tokenizing,
  applying the fix a commented-out line in the original had already drafted
  but never wired in.
- `infer_pipe_groups`: wrapped an already-distinct 2-element list in
  `set()`, making output order depend on Python's string hash
  randomization. CONFIRMED via repeated runs under different
  `PYTHONHASHSEED` values to be the actual mechanism behind a real
  git-merge inconsistency in hemonc_import (a column-ordering fix present
  on one branch, silently absent on another after a regeneration run).
  Fixed with `sorted(...)`.
- Filename resolution: `TableMeta.filename` (see schema_model.py) used a
  naive `f"{name}.csv"` convention that missed real, available data for 4
  tables whose actual filenames don't match: `canonicaltriples` (real file
  `canonical.triples.csv`), `contexttable` (`context.table.csv`),
  `variantblob` (`variant.blob.csv`), and `study_eligibility`
  (`study_eligibility beta.csv` — a literal space plus a "beta" suffix).
  `resolve_source_csv` below replaces the naive check. Note: the OLD
  natural_key_audit.py already had its own, separate `resolve_csv_path`
  with a normalized-match fallback that happened to handle 3 of these 4
  cases correctly (punctuation-insensitive matching) — but the actual
  generation step never used it, so the audit and the generator silently
  disagreed about which source files exist. There is now exactly one
  implementation, used by both compiler/generate.py and compiler/audit.py.
"""

from __future__ import annotations

import keyword
import re
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)

PY_KEYWORDS = set(keyword.kwlist)
MAX_ENUM_UNIQUE = 20
MAX_STRING_INLINE = 100
BOOLEAN_LIKE = {"true", "false", "t", "f", "yes", "no", "y", "n", "0", "1"}


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
    Robust detection of boolean / logical data, including:
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
    Detect datetime columns robustly:
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

    # sample a bit more than 5 to reduce false positives
    sample = s.head(20)

    parsed = pd.to_datetime(sample, errors="coerce", format="ISO8601")
    ratio = parsed.notna().mean()

    if ratio < 0.8:
        return False

    looks_like_date = sample.str.contains(r"[-/:T]").mean()
    return looks_like_date >= 0.5


def detect_numeric(series: pd.Series) -> str | None:
    """
    Return 'Integer', 'Float', or None.
    Works with numpy, pandas nullable, and pyarrow dtypes.
    """
    dt = str(series.dtype).lower()

    if is_integer_dtype(series.dtype) or re.match(r"^int\d+\[", dt):
        return "Integer"

    if is_float_dtype(series.dtype) or re.match(r"^float\d+\[", dt):
        return "Float"

    return None


def table_to_class(table: str) -> str:
    """Convert a normalised table name into a PascalCase class name."""
    table = table.replace(".", "_")
    return "".join(part.capitalize() for part in table.split("_"))


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
    """Find the real CSV backing `table_name` in `data_dir`, tolerating the
    filename irregularities confirmed in the real HemOnc data export
    (dots/spaces stripped when normalised, or an extra descriptive suffix).

    Returns (path, ambiguous_matches). `path` is None if nothing resolved;
    `ambiguous_matches` is non-empty only when multiple candidates tied and
    the caller should treat this as an error rather than guess.

    Resolution order (first tier that produces exactly one match wins):
    1. Exact stem match (`table_name.csv`).
    2. Normalised-stem match (`safe_identifier(stem) == table_name`) — this
       alone recovers 3 of the 4 confirmed-missing tables:
       `canonicaltriples`/`canonical.triples.csv`,
       `contexttable`/`context.table.csv`,
       `variantblob`/`variant.blob.csv`.
    3. Case-insensitive prefix match on the raw stem — recovers the 4th:
       `study_eligibility`/`study_eligibility beta.csv`. Only used when it
       yields exactly one candidate; a tie is reported as ambiguous rather
       than guessed.
    """
    csvs = sorted(data_dir.glob("*.csv"))

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

    The parser is intentionally permissive so workbook expressions such as
    `a + b + c` or `name or person_cui` can still be reduced to the column
    tokens used by the registry. Parenthetical explanatory text (e.g.
    `"study_id (see note)"`, or an inline set of alternatives like
    `"(Addition|Change|Deletion)"`) is stripped before tokenizing — this is
    the fix for the two real, confirmed corrupted-key cases described in
    this module's docstring.
    """
    text = value.strip()

    # Strip parenthetical text before anything else (US-9 fix).
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
    Group denormalised columns that appear to explode together row-by-row.

    Column pairs within a group are returned `sorted(...)`, not wrapped in
    `set(...)` — the original's `set()` usage produced non-deterministic
    output ordering across process runs (Python's string hash
    randomization), confirmed to be the mechanism behind a real git-merge
    inconsistency (US-10 fix).
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
