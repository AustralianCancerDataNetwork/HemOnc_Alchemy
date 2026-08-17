from __future__ import annotations
import pandas as pd
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, Enum, ForeignKey, Text, Float
from datetime import datetime

from hemonc_alchemy.load import  _to_enum_literal, cast_value, perform_cast
from hemonc_alchemy.registry.builder import load_csv_best
from hemonc_alchemy.registry.heuristics import safe_identifier, safe_enum_key
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import inspect as sa_inspect

from typing import Optional, List, TYPE_CHECKING, Any
import os, enum, re

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")

TABLE_PATH = os.getenv('table_path', './data')

class Base(DeclarativeBase):
    pass

@staticmethod
def resolve_normalisation_groups(meta: dict) -> list[list[str]]:
    """
    Ensure every denormalised column belongs to exactly one group.
    """
    explicit = [set(g) for g in meta.get("normalisation_groups", [])]
    denorm = set(meta.get("denormalised_columns", []))

    grouped = set().union(*explicit) if explicit else set()
    singletons = [{c} for c in denorm - grouped]

    return [sorted(g, key=len) for g in (explicit + singletons)]

def cast_identity_value(v):
    """
    Cast identity-backed values safely.

    - preserves strings
    - strips .0 from floats
    - treats NA consistently
    """
    if pd.isna(v):
        return None

    # floats from pandas inference
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v))
        return str(v)

    return str(v).strip()

def _prepare_denorm_dataframe(df, entity_pk: list[str], group: list[str]):
    mask = df[group].isna().any(axis=1)

    load_df = (
        df[entity_pk + group][~mask]
        .assign(**{c: df[c].map(cast_identity_value).str.split("|") for c in group})
        .explode(group, ignore_index=True)
    )

    return load_df

def load_vocab_denorm_group(
    session,
    df,
    vocab_cls,
    map_cls,
    entity_pk,
    group,
):
    load_df = _prepare_denorm_dataframe(df, entity_pk, group)

    # vocab
    vocab_cols = [c.name for c in vocab_cls.__table__.columns]
    vpk = [c.name for c in vocab_cls.__table__.primary_key.columns]

    vocab_terms = (
        load_df[vocab_cols]
        .drop_duplicates(subset=vpk)
        .to_dict(orient="records")
    )
    vocab_obj = [vocab_cls(**vt) for vt in vocab_terms]  # type: ignore

    # map
    map_cols = [c.name for c in map_cls.__table__.columns]
    mpk = [c.name for c in map_cls.__table__.primary_key.columns]

    null_mask = load_df[mpk].isna().any(axis=1)
    if null_mask.any():
        print(
            f"[WARN] NaN PKs in {map_cls.__name__}; "
            f"skipping {null_mask.sum()} rows"
        )

    map_entries = (
        load_df[~null_mask][map_cols]
        .drop_duplicates()
        .to_dict(orient="records")
    )
    map_obj = [map_cls(**me) for me in map_entries]  # type: ignore

    session.bulk_save_objects(vocab_obj)
    session.bulk_save_objects(map_obj)

def load_identity_denorm_group(
    session,
    df,
    map_cls,
    entity_pk,
    group,
):
    load_df = _prepare_denorm_dataframe(df, entity_pk, group)

    map_cols = [c.name for c in map_cls.__table__.columns]
    mpk = [c.name for c in map_cls.__table__.primary_key.columns]

    null_mask = load_df[mpk].isna().any(axis=1)
    if null_mask.any():
        print(
            f"[WARN] NaN PKs in {map_cls.__name__}; "
            f"skipping {null_mask.sum()} rows"
        )

    map_entries = (
        load_df[~null_mask][map_cols]
        .drop_duplicates()
        .to_dict(orient="records")
    )
    map_obj = [map_cls(**me) for me in map_entries]  # type: ignore

    session.bulk_save_objects(map_obj)


class EntityBase:
    filename: str
    pk_columns: list[str]
    source_defined_keys: list[str]
    denormalised_columns: list[str]
    normalisation_groups: list[list[str]]
    derived_columns: list[str]
    enum_lookup: dict[str, Any]

    @classmethod
    def __load__(cls, engine):
        folder = Path(TABLE_PATH)
        path = folder / cls.filename
        if not path.exists():
            print(f"[WARN] Missing CSV for {cls.__name__}: {path}")
            return
        df = load_csv_best(path)
        cols_to_load = [
            c for c in df.columns
            if safe_identifier(c).lower() in cls.pk_columns
            or (
                safe_identifier(c).lower() not in cls.denormalised_columns
                and safe_identifier(c).lower() not in cls.derived_columns
            )
        ]
        df = df[cols_to_load].rename(columns={c: safe_identifier(c).lower() for c in cols_to_load}).copy()
        mapper = sa_inspect(cls)
        model_columns = {col.key: col for col in mapper.columns} # type: ignore
        pks = [safe_identifier(pk).lower() for pk in cls.pk_columns if safe_identifier(pk).lower() in df.columns]

        for col in df.columns:
            if col not in model_columns:
                df = df.drop(columns=[col])
                continue
            column = model_columns[col]
            col_type = column.type
            if cls.enum_lookup and isinstance(col_type, Enum):
                enum_cls = cls.enum_lookup.get(f'{col}', None)
                if enum_cls:
                    df[col] = df[col].map(lambda v: enum_cls[safe_enum_key(v)] if not pd.isna(v) else None) # type: ignore
            else:   
                df[col] = df[col].map(lambda v: perform_cast(v, col_type))
        non_unique = len(df[df[pks].isnull().any(axis=1)])
        dupes = len(df[df.duplicated(subset=pks)])
        if non_unique > 0:
            print(f"[WARN] Null primary keys found in {cls.__name__} data. Dropping {non_unique} rows out of total {len(df)}.")
            df = df.dropna(subset=pks)
        if dupes > 0:
            print(f"[WARN] Duplicate primary keys found in {cls.__name__} data. Dropping {dupes} rows out of total {len(df)}.")
            df = df.drop_duplicates(subset=pks)
        casted_records = df.to_dict(orient="records")
        casted_records = [{k:v for k,v in record.items() if not pd.isna(v)} for record in casted_records]
        objs = [cls(**r) for r in casted_records]  # type: ignore
        session = Session(engine)
        try:
            print(f"[LOAD] Inserting {len(casted_records)} rows into {cls.__name__}")
            for i in range(0, len(objs), 5000):
                session.add_all(objs[i:i+5000])
                session.commit()
                if i % 50000 == 0:
                    print(f"  - inserted {i + len(objs[i:i+5000])} / {len(objs)} rows into {cls.__name__}")
        except SQLAlchemyError as e:
            errs = 0
            session.rollback()
            print(f"[ERROR] Bulk insert failed for {cls.__name__}: {e}")
            # Fallback: insert row-by-row
            for obj in objs[i:]:
                try:
                    session.add(obj)
                    session.commit()
                except SQLAlchemyError as e2:
                    session.rollback()
                    print(f"[ERROR:ROW] {obj} → {e2}")
                    if errs > 100:
                        break
                    errs += 1
        finally:
            session.close()

    @classmethod
    def _resolve_denorm_classes(cls, key: str):
        """
        Returns (vocab_cls, map_cls)

        vocab_cls is None for identity-backed groups
        map_cls must exist or the group is skipped
        """
        module = __import__(cls.__module__, fromlist=["*"])

        vocab_name = f"{cls.__name__}_{key.capitalize()}"
        map_name = f"{cls.__name__}_{key.capitalize()}Map"

        vocab_cls = getattr(module, vocab_name, None)
        map_cls = getattr(module, map_name, None)

        return vocab_cls, map_cls

    @classmethod
    def __load_denormalised__(cls, engine):

        if not cls.denormalised_columns:
            return

        path = Path(TABLE_PATH) / cls.filename
        if not path.exists():
            print(f"[WARN] Missing CSV for {cls.__name__}: {path}")
            return

        df = load_csv_best(path)
        df.columns = [safe_identifier(c).lower() for c in df.columns]

        entity_pk = [safe_identifier(c).lower() for c in cls.pk_columns]
        df = df.dropna(subset=entity_pk)

        groups = resolve_normalisation_groups({
            "denormalised_columns": cls.denormalised_columns,
            "normalisation_groups": cls.normalisation_groups,
        })

        for group in groups:
            key = group[0]
            vocab_cls, map_cls = cls._resolve_denorm_classes(key)

            if map_cls is None:
                continue

            print(f"[LOAD] {cls.__name__}: denormalised group {group}")

            session = Session(engine)
            try:
                if vocab_cls is not None:
                    load_vocab_denorm_group(
                        session, df, vocab_cls, map_cls, entity_pk, group
                    )
                else:
                    load_identity_denorm_group(
                        session, df, map_cls, entity_pk, group
                    )

                session.commit()

            except Exception as e:
                session.rollback()
                print(
                    f"[WARN] Denormalised load skipped for "
                    f"{cls.__name__}.{group}: {e}"
                )

            finally:
                session.close()

