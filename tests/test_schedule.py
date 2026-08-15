"""Regression tests for model/schedule/ — the one module ported end-to-end
so far. Covers the two behavioural fixes applied during porting: route
classification (US-6) and indefinite-dosing handling (US-5).
"""

from __future__ import annotations

from hemonc_alchemy.model.schedule import Day, Indefinite, resolve_all_days, route_group


class TestRouteGroup:
    """Cases confirmed against the real `route` column in
    hemonc_import/data/sigs.csv (~23,500 rows) — see routes.py's module
    docstring for the exact counts. Each of these previously fell through to
    None under the old hemonc_import CANCER_SERVICES_ADMINISTERED /
    HOME_ADMINISTRATION_ROUTES sets.
    """

    def test_common_abbreviations_still_classify(self):
        assert route_group("IV") == "IV"
        assert route_group("PO") == "PO"
        assert route_group("SC") == "IV"

    def test_intravesicularly_now_classifies_as_iv(self):
        # 23 real rows in sigs.csv used this exact wording; the old
        # "Intravesical" entry never matched it (different word, not just
        # different case).
        assert route_group("intravesicularly") == "IV"

    def test_inhaled_and_nebulized_case_insensitive(self):
        # 3 and 4 real rows respectively used lowercase; the old sets had
        # "Inhaled"/"Nebulized" and never matched.
        assert route_group("inhaled") == "PO"
        assert route_group("nebulized") == "PO"

    def test_not_specified_and_none_are_unclassified(self):
        assert route_group("Not specified") is None
        assert route_group(None) is None

    def test_unknown_route_is_unclassified(self):
        assert route_group("some future route nobody has seen yet") is None


class TestResolveAllDays:
    def test_simple_day_list(self):
        resolved = resolve_all_days("1,8,15")
        assert resolved.days == (Day(1), Day(8), Day(15))
        assert resolved.indefinite is None

    def test_range_expansion(self):
        resolved = resolve_all_days("[1,21,7]")
        assert resolved.days == (Day(1), Day(8), Day(15))

    def test_indefinite_marker_is_preserved_not_dropped(self, caplog):
        # Previously: expand() silently `continue`d past Indefinite tokens,
        # so a caller had no way to tell a maintenance/continuation regimen
        # was truncated. Now the marker survives and a warning is logged.
        resolved = resolve_all_days("1,8,15,(+n)")
        assert resolved.days == (Day(1), Day(8), Day(15))
        assert resolved.indefinite == Indefinite(kind="+n", max_days=None)
        assert bool(resolved) is True
        assert any("indefinite" in message.lower() for message in caplog.messages)

    def test_indefinite_only_schedule_is_still_truthy(self):
        resolved = resolve_all_days("(+c5)")
        assert resolved.days == ()
        assert resolved.indefinite == Indefinite(kind="+c", max_days=5)
        assert bool(resolved) is True

    def test_empty_input(self):
        resolved = resolve_all_days(None)
        assert resolved.days == ()
        assert resolved.indefinite is None
        assert bool(resolved) is False
