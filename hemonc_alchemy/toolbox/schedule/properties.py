"""Cross-entity schedule/administration properties.

Ported from hemonc_import's final_model/schedule_properties.py. These are
attached to Sigs/Variants once model/entities.py exists (see the compiler
work in _design/hemonc-alchemy-spec.md TS-6 step 2-3) — until then this
module is correct, self-contained Python that operates on any object
duck-typing the expected attributes (sig.route, sig.resolved_days,
sig.drug_object, ...), same as the original.

Three changes from the original, all already applied here rather than left
as follow-up:
- `route_group` now comes from routes.py's case-corrected, empirically
  re-checked classification (US-6), not a hand-duplicated vocabulary.
- `ScheduleEvent` carries `indefinite` alongside `days`, and `resolved_days`
  exposes both explicitly, since `resolve_all_days` now returns a
  `ResolvedSchedule` rather than a bare list (US-5).
- `administration_matrices`'s per-drug grid used to be keyed by `drug.drug`
  (the display name string) while every other property in this file keys by
  `drug.drug_cui` — confirmed inconsistent in the audit (two distinct Drugs
  rows sharing a display name would silently merge). Now keyed by
  `drug_cui` throughout. The original also declared `decay_days`/
  `decay_factor` parameters on a `@cached_property`, which are unreachable
  through normal property access (`cached_property.__get__` only ever calls
  `fget(instance)`) — split into a zero-arg property for the common case
  plus `compute_administration_matrices(...)` for callers who need
  non-default decay parameters.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Any

import pandas as pd

from .handling import Day, Indefinite, apply_sig_to_series, resolve_all_days
from .routes import route_group


@dataclass(frozen=True)
class ScheduleEvent:
    sig: Any
    drug_object: Any | None
    route_group: str | None
    days: tuple[Day, ...]
    indefinite: Indefinite | None
    phase: str | None
    portion: str | None
    branch: str | None
    timing_sequence: str | None
    step_number: str | None
    dose_min: str | None
    dose_max: str | None
    dose_unit: str | None
    frequency: str | None
    cycle_length_lb: float | None
    cycle_length_ub: str | None
    cycle_length_unit: str | None
    raw_all_days: str | None


@cached_property
def schedule_events(self):
    events = []
    for sig in self.component_sigs:
        resolved = sig.resolved_days
        events.append(
            ScheduleEvent(
                sig=sig,
                drug_object=sig.drug_object,
                route_group=route_group(sig.route),
                days=resolved.days,
                indefinite=resolved.indefinite,
                phase=sig.phase,
                portion=sig.portion,
                branch=sig.branch,
                timing_sequence=sig.timing_sequence,
                step_number=sig.step_number,
                dose_min=sig.doseminnum,
                dose_max=sig.dosemaxnum,
                dose_unit=sig.doseunit,
                frequency=sig.frequency,
                cycle_length_lb=sig.cycle_length_lb,
                cycle_length_ub=sig.cycle_length_ub,
                cycle_length_unit=sig.cycle_length_unit,
                raw_all_days=sig.alldays,
            )
        )
    return events


@cached_property
def cancer_services_drugs(self):
    """
    Unique Drugs administered in a chemo suite (IV / parenteral).
    """
    drugs = {}
    for event in self.schedule_events:
        drug = event.drug_object
        if event.route_group == "IV" and drug is not None:
            drugs[drug.drug_cui] = drug
    return list(drugs.values())


@cached_property
def home_administered_drugs(self):
    """
    Unique Drugs administered at home (PO, topical, inhaled).
    """
    drugs = {}
    for event in self.schedule_events:
        drug = event.drug_object
        if event.route_group == "PO" and drug is not None:
            drugs[drug.drug_cui] = drug
    return list(drugs.values())


@cached_property
def cancer_services_sigs_by_drug(self):
    """
    { Drug -> [Sigs, ...] } for chemo-suite administration.
    """
    out = defaultdict(list)
    for event in self.schedule_events:
        drug = event.drug_object
        if event.route_group == "IV" and drug is not None:
            out[drug].append(event.sig)
    return dict(out)


@cached_property
def home_administered_sigs_by_drug(self):
    """
    { Drug -> [Sigs, ...] } for home administration.
    """
    out = defaultdict(list)
    for event in self.schedule_events:
        drug = event.drug_object
        if event.route_group == "PO" and drug is not None:
            out[drug].append(event.sig)
    return dict(out)


@cached_property
def administration_matrices(self) -> dict[str, pd.DataFrame]:
    """
    Per-route day-by-drug intensity grids for explicit dosing days.

    NOTE: does not currently represent indefinite/open-ended continuation.
    A schedule_event with `indefinite is not None` contributes only its 
    explicit `days`. 
    
    Extending the grid (or otherwise marking it) to reflect an
    open-ended tail is an open design question, not solved here.
    """
    return compute_administration_matrices(self, decay_days=2, decay_factor=0.5)


def compute_administration_matrices(
    self,
    decay_days: int = 2,
    decay_factor: float = 0.5,
) -> dict[str, pd.DataFrame]:
    matrices = {}
    route_groups = {
        "IV": [event for event in self.schedule_events if event.route_group == "IV"],
        "PO": [event for event in self.schedule_events if event.route_group == "PO"],
    }

    for route, events in route_groups.items():
        if not events:
            continue

        grid = defaultdict(lambda: defaultdict(float))
        all_days = set()

        for event in events:
            drug = event.drug_object
            if drug is None or not event.days:
                continue

            apply_sig_to_series(
                grid[drug.drug_cui],
                list(event.days),
                decay_days=decay_days,
                decay_factor=decay_factor,
            )
            all_days.update(day.value for day in event.days)

        if not all_days:
            continue

        day_range = range(min(all_days), max(all_days) + decay_days + 1)
        df = pd.DataFrame(
            0.0,
            index=sorted(grid.keys()),
            columns=list(day_range),
        )

        for drug_cui, series in grid.items():
            for day, value in series.items():
                if day in df.columns:
                    df.loc[drug_cui, day] = value

        matrices[route] = df

    return matrices


@cached_property
def resolved_days(self):
    return resolve_all_days(self.alldays)
