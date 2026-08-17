"""
Route classification for schedule/administration grouping.
"""

from __future__ import annotations

from hemonc_alchemy.model.enums import Sigs_RouteEnum

_CLINIC_ADMINISTERED_ROUTES = frozenset(
    {
        Sigs_RouteEnum.IA,
        Sigs_RouteEnum.IM,
        Sigs_RouteEnum.INTRAVESICULARLY,
        Sigs_RouteEnum.IP,
        Sigs_RouteEnum.IT,
        Sigs_RouteEnum.IV,
        Sigs_RouteEnum.SC,
    }
)

_HOME_ADMINISTRATION_ROUTES = frozenset(
    {
        Sigs_RouteEnum.INHALED,
        Sigs_RouteEnum.NEBULIZED,
        Sigs_RouteEnum.PO,
    }
)


def route_group(route: Sigs_RouteEnum | str | None) -> str | None:
    """
    Classify a route enum or raw route string as "IV" (clinic-administered), "PO"
    (home-administered), or None (unclassified/not specified).
    """
    if route is None:
        return None

    if not isinstance(route, Sigs_RouteEnum):
        try:
            route = Sigs_RouteEnum(str(route).strip().lower())
        except ValueError:
            return None

    if route in _CLINIC_ADMINISTERED_ROUTES:
        return "IV"
    if route in _HOME_ADMINISTRATION_ROUTES:
        return "PO"
    return None
