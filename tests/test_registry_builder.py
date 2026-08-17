from pathlib import Path

import pandas as pd

from hemonc_alchemy.registry.builder import build_registry_from_dictionary


def _write_dictionary(path: Path) -> None:
    content = pd.DataFrame(
        {
            "Content Tables": ["Sigs"],
            "Maturity": ["prod"],
            "Description": ["Signature rows"],
            "Unique Key": ["sig_cui"],
            "Identity Key": ["variant_cui, component_cui"],
        }
    )
    lookup = pd.DataFrame(
        {
            "Lookup and Metadata Tables": ["Routes"],
            "Maturity": ["prod"],
            "Description": ["Route lookup"],
            "Unique Key": ["route"],
            "Identity Key": ["route"],
        }
    )
    sigs = pd.DataFrame(
        {
            "Variable": ["sig_cui", "route", "study"],
            "Type": ["Integer", "Enum", "String"],
            "Multiple Values Allowed": ["", "", "yes"],
            "Allowed Values/Format": ["", "IV;PO;SC", "pipe-delimited"],
        }
    )

    with pd.ExcelWriter(path) as writer:
        content.to_excel(writer, sheet_name="Content", index=False)
        lookup.to_excel(writer, sheet_name="Lookup", index=False)
        sigs.to_excel(writer, sheet_name="sigs", index=False)


def test_build_registry_populates_dictionary_metadata(tmp_path):
    dictionary = tmp_path / "data.dictionary.xlsx"
    _write_dictionary(dictionary)

    registry = build_registry_from_dictionary(dictionary)

    sigs = registry["sigs"]
    assert sigs.classname == "Sigs"
    assert sigs.pk_columns == ["sig_cui"]
    assert sigs.identity_keys == ["variant_cui", "component_cui"]
    assert sigs.columns is not None
    assert sigs.columns["route"].dtype == "Enum"
    assert sigs.enums is not None
    assert sigs.enums["route"].values == ["IV", "PO", "SC"]
    assert sigs.denormalised_columns == ["study"]


def test_build_registry_enriches_from_observed_csvs(tmp_path):
    dictionary = tmp_path / "data.dictionary.xlsx"
    _write_dictionary(dictionary)
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    pd.DataFrame(
        {
            "sig_cui": [1, 2],
            "route": ["IV", "IV"],
            "study": ["NCT1|NCT2", "NCT1|NCT2"],
        }
    ).to_csv(data_dir / "sigs.csv", index=False)

    registry = build_registry_from_dictionary(dictionary, data_dir=data_dir)

    sigs = registry["sigs"]
    assert sigs.source_defined_keys == ["sig_cui"]
    assert sigs.normalisation_groups is not None
    assert sigs.normalisation_groups[0].columns == ["study"]
