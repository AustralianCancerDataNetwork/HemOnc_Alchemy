"""Regression tests for compiler/infer.py's confirmed bug fixes (US-9, US-10,
US-13, US-18) and compiler/schema_model.py's identifier-placeholder handling.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from hemonc_alchemy.compiler.infer import (
    detect_numeric,
    infer_pipe_groups,
    parse_unique_key,
    resolve_source_csv,
)
from hemonc_alchemy.compiler.schema_model import _clean_identifier_placeholders


class TestParseUniqueKey:
    """The two real, confirmed cases from hemonc_import's data dictionary."""

    def test_strips_parenthetical_annotation(self):
        assert parse_unique_key("study_id (see note)") == ["study_id"]

    def test_strips_parenthetical_alternatives(self):
        assert parse_unique_key("Date + Type + Affected Table + (Addition|Change|Deletion)") == [
            "date",
            "type",
            "affected",
            "table",
        ]

    def test_plain_key_unaffected(self):
        assert parse_unique_key("drug_cui") == ["drug_cui"]

    def test_or_becomes_alternate_candidates(self):
        assert parse_unique_key("name or person_cui") == ["name", "person_cui"]


class TestInferPipeGroups:
    def test_deterministic_column_order(self):
        df = pd.DataFrame(
            {
                "biomarker4": ["a|b", "c", "d|e|f"],
                "biomarker4_finding": ["x|y", "z", "w|v|u"],
            }
        )
        groups = infer_pipe_groups(df, ["biomarker4", "biomarker4_finding"])
        assert groups == [sorted(["biomarker4", "biomarker4_finding"])]
        # sorted(...), not set(...) -- must be identical every call, not
        # just consistent within one process (that's what the original
        # set()-based bug got wrong: order depended on hash randomization
        # across *different* processes, not within one).
        assert infer_pipe_groups(df, ["biomarker4", "biomarker4_finding"]) == groups

    def test_missing_values_are_handled(self):
        df = pd.DataFrame(
            {
                "biomarker4": pd.array(["a|b", pd.NA, "c"], dtype="string"),
                "biomarker4_finding": pd.array(["x|y", pd.NA, "z"], dtype="string"),
            }
        )
        assert infer_pipe_groups(df, ["biomarker4", "biomarker4_finding"]) == [
            ["biomarker4", "biomarker4_finding"]
        ]


class TestDetectNumeric:
    """detect_numeric's float64-with-NaN fix (US-18)."""

    def test_integer_with_missing_values_is_integer_not_float(self):
        # pandas upcasts to float64 the moment an int column has any NaN --
        # confirmed real case: sigs.variant_cui, studies.condition_cui,
        # indications.component_cui.
        s = pd.Series([1.0, 2.0, None, 4.0])
        assert s.dtype == "float64"
        assert detect_numeric(s) == "Integer"

    def test_genuine_fractional_data_stays_float(self):
        s = pd.Series([1.5, 2.25, None, 4.0])
        assert detect_numeric(s) == "Float"

    def test_clean_integer_dtype_is_integer(self):
        assert detect_numeric(pd.Series([1, 2, 3])) == "Integer"


class TestCleanIdentifierPlaceholders:
    """US-18: variant_eligibility.variant_cui's "TBA" placeholder."""

    def test_tba_nulled_on_cui_column(self):
        s = pd.Series(["129497", "144834", "TBA"])
        cleaned = _clean_identifier_placeholders(s, "variant_cui")
        assert cleaned.dtype == "float64"
        assert cleaned.isna().sum() == 1
        assert detect_numeric(cleaned) == "Integer"

    def test_non_cui_column_untouched(self):
        # "TBD" is a real categorical value elsewhere (Authors_Site_typeEnum)
        # -- must not be treated as a placeholder outside _cui columns.
        s = pd.Series(["Academic Medical Center", "TBD", "Government"])
        cleaned = _clean_identifier_placeholders(s, "site_type")
        assert cleaned.equals(s)

    def test_genuinely_alphanumeric_cui_column_stays_textual(self):
        # If a _cui column doesn't cleanly coerce even after removing
        # placeholders, it must NOT be forced to numeric (which would
        # silently drop real, non-numeric identifier data as NaN).
        s = pd.Series(["ABC123", "DEF456", "TBA"])
        cleaned = _clean_identifier_placeholders(s, "some_cui")
        assert detect_numeric(cleaned) is None  # not coerced to numeric
        assert cleaned.isna().sum() == 1  # only the placeholder, not the real values


class TestResolveSourceCsv:
    def test_excludes_beta_files(self, tmp_path: Path):
        (tmp_path / "study_eligibility beta.csv").write_text("a,b\n1,2\n")
        path, ambiguous = resolve_source_csv(tmp_path, "study_eligibility")
        assert path is None
        assert ambiguous == []

    def test_normalised_match_recovers_dotted_filename(self, tmp_path: Path):
        (tmp_path / "canonical.triples.csv").write_text("a,b\n1,2\n")
        path, ambiguous = resolve_source_csv(tmp_path, "canonicaltriples")
        assert path is not None
        assert path.name == "canonical.triples.csv"
        assert ambiguous == []

    def test_no_match_returns_none(self, tmp_path: Path):
        path, ambiguous = resolve_source_csv(tmp_path, "nonexistent_table")
        assert path is None
        assert ambiguous == []


if __name__ == "__main__":
    pytest.main([__file__])
