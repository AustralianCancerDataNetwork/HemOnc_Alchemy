# Regenerating the model

The generated model is derived from the HemOnc data dictionary. Regeneration is
therefore a reviewable schema operation, not an ordinary application edit.

## Workflow

Install the development tools, then run:

```bash
uv sync --extra dev
hemonc-alchemy validate
hemonc-alchemy diff
hemonc-alchemy regen --data-dir path/to/extract
```

If the schema change is intentional, review the generated diff and rerun with
the required acceptance flags. Run the complete test and import-linter suites
before committing:

```bash
pytest
ruff check hemonc_alchemy tests
lint-imports
```

## Do not hand-edit generated files

`model/entities.py`, `model/enums.py`, and `schema/registry.json` are generated
artifacts. Change the source data dictionary or compiler behavior, regenerate,
and review the resulting output. Hand-written relationships belong in
`model/relationships.py`; reusable query and interpretation code belongs in
the toolkit.
