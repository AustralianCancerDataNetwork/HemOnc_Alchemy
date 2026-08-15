"""hemonc-alchemy CLI — one entry point (US-7, US-24), mirroring
omop-alchemy's maintenance/cli.py assembly pattern.

Replaces hemonc_import's three inconsistent invocation styles
(registry_main.py: no CLI args, env-vars only; natural_key_audit.py: its own
argparse CLI; sa_create.py: no CLI at all, driven ad hoc from a notebook).

Subcommands are placeholders until compiler/generate.py, validate.py,
diff.py, and audit.py are ported — each raises a clear NotImplementedError
pointing at the module that will implement it, rather than doing nothing
silently or presenting a command that looks finished but isn't.
"""

from __future__ import annotations

import typer

app = typer.Typer(
    help="hemonc-alchemy schema compiler and maintenance utilities.",
    rich_markup_mode="rich",
)


@app.command()
def regen() -> None:
    """Regenerate model/entities.py, model/enums.py, and
    schema/hemonc.linkml.yaml from the HemOnc data dictionary.

    Runs infer -> generate -> validate -> diff as one gated pipeline
    (US-8) — pending compiler/generate.py.
    """
    raise NotImplementedError(
        "compiler/generate.py has not been ported yet — see "
        "_design/hemonc-alchemy-spec.md TS-6 step 3."
    )


@app.command()
def validate() -> None:
    """Check the currently generated model for structural correctness."""
    raise NotImplementedError(
        "compiler/validate.py has not been ported yet — see "
        "_design/hemonc-alchemy-spec.md TS-6 step 3."
    )


@app.command()
def diff() -> None:
    """Diff the freshly generated schema against the last committed one."""
    raise NotImplementedError(
        "compiler/diff.py has not been ported yet — see "
        "_design/hemonc-alchemy-spec.md TS-6 step 3."
    )


@app.command()
def audit() -> None:
    """Audit natural/business keys for duplicates and enum-threshold risk."""
    raise NotImplementedError(
        "compiler/audit.py has not been ported yet — see "
        "_design/hemonc-alchemy-spec.md TS-6 step 3."
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
