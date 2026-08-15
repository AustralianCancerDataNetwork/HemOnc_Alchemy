"""Schema diff — new in this rewrite, no equivalent in hemonc_import (US-8).

hemonc_import's registry_main.py wrote entities.py/enums.py/registry.json
unconditionally on every regeneration; nothing compared the new output
against what was previously committed. This is the confirmed root cause of
the git-divergence problems found in the audit: a real fix present for one
sibling field (`biomarker4`) went silently missing for another
(`canmed_minor_class`) after a regeneration, and a `studies` entity's
description/maturity metadata was found to have silently absorbed values
from a deleted `study_demographics` entity in the same pass. Neither would
have survived a diff step that required acknowledging what changed.

Operates on the interim JSON registry snapshot (schema/registry.json) --
once schema/hemonc.linkml.yaml exists (US-14, pending the slot-scoping
prototype), this should diff that file instead; the comparison logic below
doesn't care which serialisation it's reading.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .schema_model import Registry


def load_previous_registry_from_git(path: Path, ref: str = "HEAD") -> Registry | None:
    """Load the last-committed registry.json via `git show`, or None if it
    doesn't exist yet at that ref (e.g. the very first regeneration)."""
    repo_root = path.parent
    while repo_root != repo_root.parent and not (repo_root / ".git").exists():
        repo_root = repo_root.parent

    rel_path = path.relative_to(repo_root)
    result = subprocess.run(
        ["git", "show", f"{ref}:{rel_path.as_posix()}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None

    import json

    return Registry.from_dict(json.loads(result.stdout))


def diff_registries(old: Registry, new: Registry) -> list[str]:
    """Human-readable list of schema changes between two registries.

    Every entry here is exactly the kind of change that should require a
    human to look at it before it's silently regenerated over -- table
    presence, column presence, column type, nullability, and primary-key
    composition.
    """
    changes: list[str] = []

    old_tables = set(old.tables)
    new_tables = set(new.tables)

    for removed in sorted(old_tables - new_tables):
        changes.append(f"TABLE REMOVED: '{removed}'")
    for added in sorted(new_tables - old_tables):
        changes.append(f"TABLE ADDED: '{added}'")

    for name in sorted(old_tables & new_tables):
        old_meta = old.tables[name]
        new_meta = new.tables[name]

        # Table-level metadata: catches exactly the confirmed real bug that
        # motivated this module -- `studies` silently absorbing
        # `study_demographics`'s description/maturity during a regeneration
        # pass (hemonc-import-audit.md). A pk_columns/column-only diff
        # would have missed it, since neither actually changed.
        if old_meta.description != new_meta.description:
            changes.append(
                f"{name}: description changed {old_meta.description!r} -> {new_meta.description!r}"
            )
        if old_meta.maturity != new_meta.maturity:
            changes.append(f"{name}: maturity changed {old_meta.maturity!r} -> {new_meta.maturity!r}")

        if old_meta.pk_columns != new_meta.pk_columns:
            changes.append(f"{name}: primary key changed {old_meta.pk_columns!r} -> {new_meta.pk_columns!r}")

        old_cols = set(old_meta.columns)
        new_cols = set(new_meta.columns)
        for removed in sorted(old_cols - new_cols):
            changes.append(f"{name}.{removed}: column removed")
        for added in sorted(new_cols - old_cols):
            changes.append(f"{name}.{added}: column added")

        for col_name in sorted(old_cols & new_cols):
            old_col = old_meta.columns[col_name]
            new_col = new_meta.columns[col_name]
            if old_col.type != new_col.type:
                changes.append(f"{name}.{col_name}: type changed {old_col.type!r} -> {new_col.type!r}")
            if old_col.nullable != new_col.nullable:
                changes.append(
                    f"{name}.{col_name}: nullable changed {old_col.nullable!r} -> {new_col.nullable!r}"
                )

    return changes


def diff_or_raise(registry_json_path: Path, new_registry: Registry, ref: str = "HEAD") -> list[str]:
    """Compare `new_registry` against what's committed at `ref`.

    Returns the list of changes (empty if none / first generation) rather
    than raising -- the CLI decides whether an unacknowledged diff should
    block `regen`, since "acknowledging" a diff is a human review step, not
    something this function can determine on its own.
    """
    previous = load_previous_registry_from_git(registry_json_path, ref)
    if previous is None:
        return []
    return diff_registries(previous, new_registry)
