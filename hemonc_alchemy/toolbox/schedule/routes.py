"""Route classification for schedule/administration grouping.

This replaces hemonc_import's final_model/definitions.py
CANCER_SERVICES_ADMINISTERED / HOME_ADMINISTRATION_ROUTES sets, which had
drifted from the real data (US-6 in _design/hemonc-alchemy-spec.md).

Empirical check against the real `route` column (hemonc_import/data/sigs.csv,
~23,500 rows) turned up more than the audit's original framing captured: the
mismatch is not only a *future* risk once Sigs.route gets properly
enum-cast — it is already live today on raw string values, for three real,
counted cases:

- ``"intravesicularly"`` (23 rows) — the old set had ``"Intravesical"``, a
  different word (not just different case), so this never matched.
- ``"inhaled"`` (3 rows) — the old set had ``"Inhaled"``; case-only mismatch.
- ``"nebulized"`` (4 rows) — the old set had ``"Nebulized"``; case-only
  mismatch.

Everything else in the real data (IV, PO, SC, Intravenous, IT, IM, Oral,
Subcutaneous, IA, IP, Intracavitary, Intrathecal, Intramuscular,
Intra-arterial, by scarification, "Not specified") already matched the old
sets exactly and is unaffected.

The fix here is deliberately narrow: case-insensitive matching plus the one
empirically-confirmed missing value. It does NOT attempt to be the long-term
source of truth — once compiler/generate.py produces the real
`Sigs_RouteEnum` (11 canonical members, confirmed via
hemonc_import/final_model/enums.py:332-343), route grouping should key off
that enum directly rather than a hand-maintained parallel vocabulary. This
module's constants should be re-derived from the enum at that point, not
maintained in parallel indefinitely — see US-6 acceptance criteria.
"""

from __future__ import annotations

# Lowercased, since matching is case-insensitive (see module docstring).
_CLINIC_ADMINISTERED_ROUTES = frozenset(
    {
        "iv", "intravenous",
        "ia", "intra-arterial",
        "im", "intramuscular",
        "sc", "subcutaneous",
        "ip", "intraperitoneal",
        "it", "intrathecal",
        "intracavitary",
        "intravesical", "intravesicularly",
    }
)

_HOME_ADMINISTRATION_ROUTES = frozenset(
    {
        "po", "oral",
        "topical",
        "inhaled",
        "nebulized",
        "by scarification",
    }
)


def route_group(route: str | None) -> str | None:
    """Classify a raw `route` string as "IV" (clinic-administered), "PO"
    (home-administered), or None (unclassified/not specified).
    """
    if route is None:
        return None
    normalised = route.strip().lower()
    if normalised in _CLINIC_ADMINISTERED_ROUTES:
        return "IV"
    if normalised in _HOME_ADMINISTRATION_ROUTES:
        return "PO"
    return None
