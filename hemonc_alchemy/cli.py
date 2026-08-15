"""hemonc-alchemy CLI — one entry point (US-7, US-24), mirroring
omop-alchemy's maintenance/cli.py assembly pattern.

Replaces hemonc_import's three inconsistent invocation styles
(registry_main.py: no CLI args, env-vars only; natural_key_audit.py: its own
argparse CLI; sa_create.py: no CLI at all, driven ad hoc from a notebook).
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .compiler import audit as audit_module
from .compiler import diff as diff_module
from .compiler import generate as generate_module
from .compiler import validate as validate_module
from .compiler.schema_model import load_registry_json
from .errors import HemOncValidationError

app = typer.Typer(
    help="hemonc-alchemy schema compiler and maintenance utilities.",
    rich_markup_mode="rich",
)

_PACKAGE_ROOT = Path(__file__).parent
_MODEL_DIR = _PACKAGE_ROOT / "model"
_SCHEMA_DIR = _PACKAGE_ROOT / "schema"
_REGISTRY_JSON = _SCHEMA_DIR / "registry.json"

DictionaryPathOption = Annotated[
    Path,
    typer.Option(envvar="HEMONC_DICTIONARY_PATH", help="Path to the HemOnc data dictionary workbook (.xlsx)."),
]
DataDirOption = Annotated[
    Path,
    typer.Option(envvar="HEMONC_DATA_DIR", help="Directory containing the current HemOnc CSV extracts."),
]


@app.command()
def regen(
    dictionary_path: DictionaryPathOption,
    data_dir: DataDirOption,
    force: Annotated[bool, typer.Option(help="Proceed even if the schema diff shows unacknowledged changes.")] = False,
) -> None:
    """Regenerate model/entities.py, model/enums.py, and schema/registry.json
    from the HemOnc data dictionary.

    Runs generate -> validate -> diff as one gated pipeline (US-8): a
    validation failure or an un-acknowledged schema diff stops the command
    before anything is left in a half-updated state relative to what's
    committed. Pass --force to accept the diff (e.g. after reviewing it
    with `hemonc-alchemy diff`).
    """
    registry = generate_module.regenerate(dictionary_path, data_dir, _MODEL_DIR)

    errors = validate_module.validate_all(registry, _MODEL_DIR / "entities.py", _MODEL_DIR / "enums.py")
    if errors:
        typer.secho("Validation failed:", fg=typer.colors.RED, bold=True)
        for error in errors:
            typer.echo(f"  - {error}")
        raise typer.Exit(code=1)

    changes = diff_module.diff_or_raise(_REGISTRY_JSON, registry)
    if changes and not force:
        typer.secho(
            f"Schema changed in {len(changes)} way(s) since the last committed version. "
            "Review with `hemonc-alchemy diff`, then re-run with --force to accept.",
            fg=typer.colors.YELLOW,
        )
        for change in changes:
            typer.echo(f"  - {change}")
        raise typer.Exit(code=1)

    warnings = audit_module.enum_threshold_warnings(registry)
    for warning in warnings:
        typer.secho(f"Warning: {warning}", fg=typer.colors.YELLOW)

    typer.secho(
        f"Regenerated {len(registry.tables)} tables "
        f"({sum(1 for t in registry.tables.values() if t.columns)} produced an entity class).",
        fg=typer.colors.GREEN,
    )


@app.command()
def validate() -> None:
    """Check the currently generated model for structural correctness."""
    if not _REGISTRY_JSON.exists():
        typer.secho(f"No registry found at {_REGISTRY_JSON} — run `regen` first.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    registry = load_registry_json(_REGISTRY_JSON)
    try:
        validate_module.validate_or_raise(registry, _MODEL_DIR / "entities.py", _MODEL_DIR / "enums.py")
    except HemOncValidationError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc

    typer.secho("Model is structurally valid.", fg=typer.colors.GREEN)


@app.command()
def diff(
    ref: Annotated[str, typer.Option(help="Git ref to diff against.")] = "HEAD",
) -> None:
    """Diff the currently generated schema against the last committed one."""
    if not _REGISTRY_JSON.exists():
        typer.secho(f"No registry found at {_REGISTRY_JSON} — run `regen` first.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    registry = load_registry_json(_REGISTRY_JSON)
    changes = diff_module.diff_or_raise(_REGISTRY_JSON, registry, ref=ref)

    if not changes:
        typer.secho(f"No schema changes since {ref}.", fg=typer.colors.GREEN)
        return

    typer.secho(f"{len(changes)} change(s) since {ref}:", fg=typer.colors.YELLOW)
    for change in changes:
        typer.echo(f"  - {change}")


@app.command()
def audit(
    dictionary_path: DictionaryPathOption,
    data_dir: DataDirOption,
    output: Annotated[Path | None, typer.Option(help="Write the report here instead of printing it.")] = None,
) -> None:
    """Audit natural/business keys for duplicates and enum-threshold risk."""
    results = audit_module.run_audit(dictionary_path, data_dir)
    report = audit_module.build_report(results, dictionary_path, data_dir)

    if output is None:
        typer.echo(report)
        return

    output.write_text(report, encoding="utf-8")
    typer.secho(f"Wrote report to {output}", fg=typer.colors.GREEN)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
