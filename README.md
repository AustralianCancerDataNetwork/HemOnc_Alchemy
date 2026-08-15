# hemonc-alchemy

SQLAlchemy-based models, regeneration tooling, and utilities for the HemOnc.org oncology terminology.

Sibling to [omop-alchemy](https://github.com/AustralianCancerDataNetwork/OMOP_Alchemy) — shares its infrastructure (`oa-configurator`, `orm-loader`) and packaging conventions, but not its ORM models. Unlike OMOP CDM, HemOnc's schema is dictionary-driven and evolves release to release, so this repo also ships an author-facing compiler that regenerates the model from HemOnc's data dictionary — see `_design/hemonc-alchemy-spec.md` for the full rationale.

**Status: ground-up rewrite in progress, on the `refactor` branch.** This replaces the previous `HemOnc_Alchemy` codebase (hand-typed model, notebook-driven ETL, no tests) rather than extending it. See `_design/migration-status.md` for exactly what's ported, what's a placeholder, and what's next.

## Layout

```
hemonc_alchemy/
├── model/       # runtime: entities (generated), relationships, schedule handling
├── toolbox/     # cross-entity enrichment: fuzzy linking, clinical classification
├── schema/      # the canonical LinkML schema (not yet authored)
├── compiler/    # author-facing only — regenerates model/ and schema/ from the
│                # HemOnc data dictionary. Not installed by default.
├── loaders/     # CSV/vocabulary loading, built on orm-loader
└── cli.py       # `hemonc-alchemy regen|validate|diff|audit`
```

## Installing

```bash
uv sync                 # runtime only
uv sync --extra dev     # runtime + compiler (author) + test/lint/docs tooling
```

## Reference material

`reference/` holds material salvaged from the pre-rewrite codebase that didn't make sense to delete outright: the spaCy sig-parsing patterns (`reference/nlp/`), the old example/demo notebooks (`reference/notebooks/`), and hard-won domain notes extracted from the old model's code comments (`reference/domain-notes.md`). None of it is wired into the current package.

## Configuration

hemonc-alchemy uses [oa-configurator](https://pypi.org/project/oa-configurator/) the same way omop-alchemy does. Once you have a stack config set up:

```bash
omop-config configure hemonc_alchemy
```
