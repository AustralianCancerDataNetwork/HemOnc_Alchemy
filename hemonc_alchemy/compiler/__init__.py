"""Regenerates the model from the HemOnc data dictionary. Maintainers only.

HemOnc's schema changes with each release, so `model/entities.py` and
`model/enums.py` are generated from the dictionary workbook and the CSV
extract rather than hand-written, along with `schema/registry.json` recording
what they were generated from.

Not needed to query HemOnc, and not installed unless you ask for the `author`
extra. Nothing in `model/` or `toolkit/` imports it.
"""
