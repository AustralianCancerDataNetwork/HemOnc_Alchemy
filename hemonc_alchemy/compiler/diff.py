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
    doesn't exist yet at that ref (e.g. the very first regeneration).

    Validates `ref` itself first (review follow-up): a bad `ref` used to be
    indistinguishable from "no registry.json committed yet at a real ref" --
    CONFIRMED `diff --ref definitely-not-a-ref` exited 0 with "No schema
    changes", since any nonzero `git show` return code (including "unknown
    revision") was treated as first-generation. Now only a *valid* ref
    lacking the file at that point in history is treated that way; an
    invalid ref raises instead of silently reporting a clean diff.
    """
    repo_root = path.parent
    while repo_root != repo_root.parent and not (repo_root / ".git").exists():
        repo_root = repo_root.parent

    ref_check = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if ref_check.returncode != 0:
        raise ValueError(f"'{ref}' is not a valid git ref in {repo_root}")

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
        if old_meta.use_surrogate_pk != new_meta.use_surrogate_pk:
            changes.append(
                f"{name}: use_surrogate_pk changed {old_meta.use_surrogate_pk!r} -> {new_meta.use_surrogate_pk!r}"
            )

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

        # Beyond column presence/type/nullability: every one of these
        # directly shapes the generated code (enum members, exploded map
        # tables, viewonly relationships) without necessarily changing a
        # column's type or the table's own pk_columns/description -- a
        # synthetic enum-member change previously produced an empty diff
        # (review follow-up).
        old_enums = {col: tuple(sorted(v.strip().lower() for v in e.values)) for col, e in old_meta.enums.items()}
        new_enums = {col: tuple(sorted(v.strip().lower() for v in e.values)) for col, e in new_meta.enums.items()}
        for col in sorted(set(old_enums) - set(new_enums)):
            changes.append(f"{name}.{col}: enum removed")
        for col in sorted(set(new_enums) - set(old_enums)):
            changes.append(f"{name}.{col}: enum added")
        for col in sorted(set(old_enums) & set(new_enums)):
            if old_enums[col] != new_enums[col]:
                changes.append(
                    f"{name}.{col}: enum values changed {list(old_enums[col])!r} -> {list(new_enums[col])!r}"
                )

        if set(old_meta.denormalised_columns) != set(new_meta.denormalised_columns):
            changes.append(
                f"{name}: denormalised columns changed {sorted(old_meta.denormalised_columns)!r} "
                f"-> {sorted(new_meta.denormalised_columns)!r}"
            )
        if set(old_meta.derived_columns) != set(new_meta.derived_columns):
            changes.append(
                f"{name}: derived columns changed {sorted(old_meta.derived_columns)!r} "
                f"-> {sorted(new_meta.derived_columns)!r}"
            )

        old_groups = {tuple(sorted(g.columns)) for g in old_meta.normalisation_groups}
        new_groups = {tuple(sorted(g.columns)) for g in new_meta.normalisation_groups}
        if old_groups != new_groups:
            changes.append(f"{name}: normalisation groups changed {sorted(old_groups)!r} -> {sorted(new_groups)!r}")

        old_soft = {(r.local_column, r.target_table, r.target_column) for r in old_meta.soft_relationships}
        new_soft = {(r.local_column, r.target_table, r.target_column) for r in new_meta.soft_relationships}
        if old_soft != new_soft:
            changes.append(f"{name}: soft relationships changed {sorted(old_soft)!r} -> {sorted(new_soft)!r}")

        old_m2m = {
            (r.map_table, r.map_column, r.target_table, r.target_column) for r in old_meta.soft_m2m_relationships
        }
        new_m2m = {
            (r.map_table, r.map_column, r.target_table, r.target_column) for r in new_meta.soft_m2m_relationships
        }
        if old_m2m != new_m2m:
            changes.append(f"{name}: soft m2m relationships changed {sorted(old_m2m)!r} -> {sorted(new_m2m)!r}")

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
