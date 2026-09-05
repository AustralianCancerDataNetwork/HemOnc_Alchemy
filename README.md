# hemonc-alchemy

Query the [HemOnc.org](https://hemonc.org) oncology terminology as Python objects.

HemOnc describes cancer treatment regimens: which drugs make up a regimen, at what dose, on which days of a cycle, for which conditions, and which published studies support them. This package gives you that content as SQLAlchemy models, so you can query it alongside your own data instead of parsing spreadsheets.

Sibling to [omop-alchemy](https://github.com/AustralianCancerDataNetwork/OMOP_Alchemy), with which it shares configuration and loading infrastructure.

## Installing

```bash
uv sync                 # to query HemOnc
uv sync --extra dev     # also the regeneration tooling, tests and linting
```

## Documentation

The end-user documentation lives in `docs/` and is configured by `mkdocs.yml`.
With the development extras installed, preview it locally with:

```bash
mkdocs serve
```

Build the static site with `mkdocs build --strict`.

## Configuring a connection

Connections are managed by [oa-configurator](https://pypi.org/project/oa-configurator/), shared across the stack, so you set a database up once and every package can reach it:

```bash
omop-config configure hemonc_alchemy
```

Then:

```python
import sqlalchemy.orm as so
from hemonc_alchemy import create_hemonc_engine, get_hemonc_context

_, database = get_hemonc_context()
engine = create_hemonc_engine(database)
session = so.Session(engine)
```

## Selected entities

| Entity | One row per |
|---|---|
| `Regimens` | named regimen (e.g. FOLFOX) |
| `Variants` | specific version of a regimen — a concrete dosing variant |
| `Sigs` | dosing instruction: one drug, one dose, one schedule, within a variant |
| `Drugs` | drug or other treatment component |
| `Conditions` | cancer condition |
| `Indications` | condition/regimen pairing, with its evidence and approval status |
| `Studies` | published study |
| `StudyResults` | reported outcome from a study |
| `VariantEligibility` | eligibility criteria attached to a variant |

Fields ending `_cui` are HemOnc concept identifiers.

### Selected useful relationships

A variant has sigs; each sig names a drug. So the drugs in a regimen variant, with their doses and schedules:

```python
from hemonc_alchemy import Variants

variant = session.query(Variants).filter_by(variant_cui=12460).one()
for sig in variant.component_sigs:
    print(sig.drug_object.drug, sig.doseminnum, sig.doseunit, sig.alldays)
```

| From | Attribute | To |
|---|---|---|
| `Variants` | `component_sigs` | its `Sigs` |
| `Variants` | `regimen_cui_obj` | its `Regimens` row |
| `Sigs` | `drug_object` | the `Drugs` row it doses |
| `Sigs` | `variant_object` | the `Variants` row it belongs to |
| `Drugs` | `sigs` | every `Sigs` dosing this drug |
| `Studies` | `variants` | the variants it studied |
| `Studies` | `condition_cui_obj` / `condition_obj` | its `Conditions` row |
| `Conditions` | `studies` | studies in this condition |
| `Indications` | `regimen_cui_objects` | the regimens it cites |


### Normalisation of multi-valued fields

Some HemOnc fields hold several values in one pipe-delimited cell (`"12460|1354"`). These are split into child tables, reachable through an `_items` relationship rather than read as a string — for example `indications.regimen_cui_items`, since one indication can cite more than one regimen.

## Reading dosing schedules

A sig's `alldays` field is a compact expression of which days of a cycle a drug is given on. `resolve_all_days` turns it into explicit day numbers:

```python
from hemonc_alchemy import resolve_all_days

schedule = resolve_all_days("1,8,15")
schedule.days          # (Day(1), Day(8), Day(15))
schedule.indefinite    # None
```

Some schedules continue indefinitely (until progression, say) rather than ending on a known day. Those set `indefinite`, and the `days` list is then only the part that is explicitly specified — not the whole schedule. Check `indefinite` before treating `days` as complete.

### Comparing regimens by when they are given

`administration_frame` turns a variant's sigs into a per-drug, per-day view of a cycle — one row per drug per day, which pivots, groups and joins like any other tidy frame:

```python
from hemonc_alchemy.toolkit.analytics.treatment.scheduling import administration_frame, administration_matrix

frame = administration_frame(variant)
frame[frame.route_group == "IV"]                    # what needs a clinic visit
administration_matrix(frame)                        # the drug-by-day grid
```

```
day       1    2     3    8    9     10   15   16    17
drug
cisplatin  1.0  0.5  0.25  1.0  0.5  0.25  1.0  0.5  0.25
```

`intensity` is 1.0 on a dosing day and tapers over the two days after, so a treatment day and the days it encroaches on both register; pass `decay_days=0` for dosing days alone. Pass a list of variants to get them all in one frame and compare with `groupby("variant_cui")`.

Two things to know when reading it. Sigs whose route isn't specified are excluded, so the frame covers less than the regimen if `route_group` is unknown. And where `indefinite` is set the days shown are only the part that was written down — the schedule continues past them.

`hemonc_alchemy.toolkit` also holds helpers for classifying treatment, such as distinguishing radiotherapy-only variants from concurrent chemoradiotherapy, and for splitting a variant's drugs into clinic- versus home-administered (`cancer_services_drugs`, `home_administered_drugs`).

## Pulling in model updates as required

HemOnc's schema is defined by a data dictionary that may change with each release, so the model is generated from that dictionary rather than hand-written. Regenerating it is a maintainer task and needs the `dev` extra:

```bash
hemonc-alchemy regen --data-dir path/to/extract   # rebuild the model
hemonc-alchemy diff                               # what changed since last commit
hemonc-alchemy validate                           # check the current model
hemonc-alchemy audit                              # key duplication and enum risks
```

`regen` refuses to write a model that has quietly lost a table, and reports any schema change for review before it is accepted.

## Layout

```
hemonc_alchemy/
├── model/       entity classes (generated) and their relationships
├── toolkit/     classification, cross-entity lookup, dosing schedules, loading
├── schema/      registry.json — the schema the model was generated from
├── compiler/    regenerates model/ from the data dictionary; maintainers only
├── config.py    database configuration
└── cli.py       the hemonc-alchemy command
```
