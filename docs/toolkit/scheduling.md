# Schedules and administration

Scheduling helpers turn the source `alldays` notation into inspectable day
objects and project sigs into administration-oriented views.

## Resolve cycle days

```python
from hemonc_alchemy import resolve_all_days

resolved = resolve_all_days("1,8,15,(+n)")
resolved.days       # (Day(1), Day(8), Day(15))
resolved.indefinite # Indefinite(kind="+n", max_days=None)
```

An indefinite marker is preserved. Explicit days are only the part represented
in the source expression; do not treat them as the complete treatment course.

## Build an administration frame

```python
from hemonc_alchemy.toolkit.analytics.treatment.scheduling import (
    administration_frame,
    administration_matrix,
)

frame = administration_frame(variant, decay_days=0)
clinic = frame[frame.route_group == "IV"]
matrix = administration_matrix(frame)
```

The frame has one row per drug per cycle day. `route_group == "IV"` is a
historical shorthand for clinic-administered routes; it includes more than
intravenous administration. Unrecognized or unspecified routes are excluded
from the administration projections rather than guessed.

## Source-shaped dosing fields

`ScheduleEvent` preserves source-facing strings for fields such as dose and
cycle length bounds, and generated enum members for phase, frequency, and cycle
length units. Numeric interpretation belongs in a caller policy because source
values may be nullable or contain non-numeric text.
