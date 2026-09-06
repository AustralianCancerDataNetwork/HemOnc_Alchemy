# Contributing

## Development setup

```bash
uv sync --all-extras --dev
uv run pytest -q
uv run ruff check .
```

The repository devcontainer provides the same environment plus PostgreSQL, pgAdmin, the source extract, and the notebook dependencies. The devcontainer database is disposable; see [Local development](docs/getting-started/local-development.md).

## Pull requests

Use the PR template for reviewer context and apply exactly one release label before merging:

| Label | Use when |
|---|---|
| `breaking` | A public, backward-incompatible change |
| `feature` | New backward-compatible functionality |
| `fix` | A bug fix |
| `dependencies` | A dependency update |
| `chore` | Refactoring, tests, docs, generated maintenance, or CI work with no public API change |

The PR title is the release-note entry. Keep it concise and factual. The opening PR description is for reviewers; include design context, data-model implications, and validation there. Squash merge with the final title intact.

Changes to generated model files should include the source or generator change that produced them, plus the relevant regeneration and validation output. Do not hand-edit generated entities as a substitute for fixing the generator or registry.

## Releases

The repository uses the shared [CAVA devops workflows](docs/maintainers/release-process.md). Versions come from `vX.Y.Z` tags through `hatch-vcs`; no version file or changelog commit is written back to `main`.
