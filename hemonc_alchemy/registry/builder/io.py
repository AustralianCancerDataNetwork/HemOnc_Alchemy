from dataclasses import asdict
import json
from pathlib import Path
import pandas as pd
from ..registry_model import TableMeta, ColumnSpec, EnumInfo, NormalisationGroup

def save_registry_to_json(registry: dict[str, TableMeta], path: Path):
    serialisable = {k: asdict(v) for k, v in registry.items()}
    path.write_text(json.dumps(serialisable, indent=4, sort_keys=True))
    print(f"Registry written to {path}")

def load_registry_from_json(path: Path) -> dict[str, TableMeta]:
    raw = json.loads(path.read_text())
    registry: dict[str, TableMeta] = {}

    for table_name, meta_dict in raw.items():

        columns = {
            col: ColumnSpec(
                **{
                    **spec,
                    "enum": EnumInfo(**spec["enum"]) if spec.get("enum") else None,
                }
            )
            for col, spec in (meta_dict.get("columns") or {}).items()
        }

        enums = {
            col: EnumInfo(**enum)
            for col, enum in (meta_dict.get("enums") or {}).items()
        }

        groups = [
            NormalisationGroup(**g)
            for g in (meta_dict.get("normalisation_groups") or [])
        ]

        registry[table_name] = TableMeta(
            name=meta_dict["name"],
            classname=meta_dict["classname"],
            kind=meta_dict["kind"],
            maturity=meta_dict["maturity"],
            description=meta_dict["description"],
            pk_columns=meta_dict["pk_columns"],
            identity_keys=meta_dict["identity_keys"],
            filename=meta_dict["filename"],
            columns=columns,
            enums=enums,
            denormalised_columns=meta_dict.get("denormalised_columns"),
            derived_columns=meta_dict.get("derived_columns"),
            source_defined_keys=meta_dict.get("source_defined_keys"),
            normalisation_groups=groups,
        )

    return registry

def load_csv_best(path: Path) -> pd.DataFrame:
    """
    Load CSV using pyarrow backend to preserve nullable types.
    """
    return pd.read_csv(
        path,
        low_memory=False,
        dtype_backend="pyarrow",
        parse_dates=True,
        keep_default_na=True,
        na_values=["", "NA", "N/A", "None", "null"],
    )

def load_folder(folder: Path) -> dict[str, pd.DataFrame]:
    """
    Load all CSV files in a folder and return a mapping of table name to DataFrame.
    """
    folder = folder.resolve()
    dataframes = {}
    for csv in folder.glob("*.csv"):
        name = csv.stem  # assume matches __tablename__
        df = pd.read_csv(csv)
        dataframes[name] = df
    return dataframes  