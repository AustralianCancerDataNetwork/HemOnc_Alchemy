# Release and repository workflow

HemOnc Alchemy uses the shared [cava-devops](https://github.com/AustralianCancerDataNetwork/cava-devops) workflows. The package repository keeps the small amount of configuration that is inherently repository-specific; the CI, label gate, release drafting, documentation deployment, and distribution build logic remains reusable and centralised.

## Pull requests

The `CI` workflow runs on pull requests targeting `main`. It has two independent responsibilities:

- `label-gate / check` requires exactly one release label: `breaking`, `feature`, `fix`, `dependencies`, or `chore`.
- `build-test / test` runs the full test suite against a PostgreSQL service, including tests that need a real database connection.

The label controls release intent, not test selection. Use `chore` for documentation, refactoring, generated maintenance, and CI changes that should not create a release-note entry. Use the highest applicable bump label when a change affects the public package.

The PR title becomes the release-note entry. The description is reviewer context, so explain design decisions, data-model consequences, and how the change was verified there. Before merging, confirm that the title is suitable for someone reading the release history months later.

## Versioning and release drafting

The version is derived from Git tags by `hatch-vcs`. The repository does not maintain a manually edited version string or a generated `CHANGELOG.md`.

When a labelled PR is squash-merged, `merge.yml` updates the standing draft release. The draft's next version is resolved from the highest-priority label it contains:

| Label | Version impact |
|---|---|
| `breaking` | Major |
| `feature` | Minor |
| `fix` or `dependencies` | Patch |
| `chore` | No release-note entry and no version bump |

A maintainer reviews and publishes the draft from GitHub's Releases page. Publishing creates a `vX.Y.Z` tag on `main`; that tag is the only event that starts package publication.

## Package publication

`publish.yml` delegates building to CAVA, which verifies that the tag is reachable from `main` and produces the wheel and source distribution. The final PyPI upload stays in this repository because PyPI trusted publishing binds its OIDC identity to the calling repository's workflow file.

The repository needs a GitHub environment named `pypi` and a PyPI trusted publisher with these values:

| Field | Value |
|---|---|
| Owner | `AustralianCancerDataNetwork` |
| Repository | `hemonc-alchemy` |
| Workflow | `publish.yml` |
| Environment | `pypi` |

## Documentation deployment

`docs.yml` deploys the MkDocs site after changes land on `main` and can also be run manually. The documentation dependencies live in the `dev` extra so the reusable deployment workflow can recreate the same build environment.

## Repository settings

For the workflows to protect the intended path, configure `main` to require pull requests, at least one approval, and these status checks:

- `label-gate / check`
- `build-test / test`

Use squash merging as the normal merge strategy and prevent force pushes to `main`. The initial history migration or other exceptional administrative operation should be handled separately from ordinary package changes.
