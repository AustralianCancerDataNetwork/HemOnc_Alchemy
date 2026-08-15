"""Post-generation structural validation — new in this rewrite (US-8).

hemonc_import had no validation step after writing generated files: nothing
checked the output was syntactically valid Python, or that every declared
primary-key column actually existed on its table. Two checks, run
independently so a failure is attributable to the right stage:

1. `validate_registry` — structural checks against the Registry object
   itself, before rendering (catches a bad pk_columns/enum declaration
   regardless of what the generator would have done with it).
2. `validate_generated_file` — `ast.parse` on the actual written Python, so
   a bug in the *generator* (producing invalid syntax from valid metadata)
   is caught too, not just bad input metadata.

Deferred: reusing orm_loader.registry.validation's `Validator` protocol
(US-21) via a HemOnc TableSpec/FieldSpec adapter (loaders/spec_adapter.py)
is the more complete long-term answer and would subsume some of this — not
done yet, this module is the minimum bar in the meantime.
"""

from __future__ import annotations

import ast
from pathlib import Path

from ..errors import HemOncValidationError
from .schema_model import Registry


def validate_registry(registry: Registry) -> list[str]:
    """Structural checks against the Registry, before any code is rendered."""
    errors: list[str] = []

    for name, meta in registry.tables.items():
        if len(meta.columns) == 0:
            # No entity class is generated for this table (e.g. no backing
            # CSV was found) -- nothing to check.
            continue

        uses_surrogate = meta.use_surrogate_pk and meta.kind == "content"
        effective_pk = ["id"] if uses_surrogate else meta.pk_columns

        for pk in effective_pk:
            if pk == "id" and uses_surrogate:
                continue
            if pk not in meta.columns:
                errors.append(f"{name}: declared pk_column '{pk}' does not exist among its generated columns")

        for col_name in meta.enums:
            if col_name not in meta.columns:
                errors.append(f"{name}: enum declared for column '{col_name}' but no such column exists")

        for rel in meta.soft_relationships:
            if rel.target_table not in registry.tables:
                errors.append(f"{name}: soft relationship targets unknown table '{rel.target_table}'")

        for rel in meta.soft_m2m_relationships:
            if rel.target_table not in registry.tables:
                errors.append(f"{name}: soft m2m relationship targets unknown table '{rel.target_table}'")

    return errors


def validate_generated_file(path: Path) -> list[str]:
    """Confirm a generated Python file is at least syntactically valid."""
    source = path.read_text(encoding="utf-8")
    try:
        ast.parse(source)
    except SyntaxError as exc:
        return [f"{path}: syntax error at line {exc.lineno}: {exc.msg}"]
    return []


def validate_all(registry: Registry, entities_path: Path, enums_path: Path) -> list[str]:
    """Run every check; return all failures (does not raise)."""
    errors = validate_registry(registry)
    errors += validate_generated_file(entities_path)
    errors += validate_generated_file(enums_path)
    return errors


def validate_or_raise(registry: Registry, entities_path: Path, enums_path: Path) -> None:
    """Raise HemOncValidationError with every failure listed, if any."""
    errors = validate_all(registry, entities_path, enums_path)
    if errors:
        joined = "\n".join(f"  - {e}" for e in errors)
        raise HemOncValidationError(f"Generated model failed validation:\n{joined}")
