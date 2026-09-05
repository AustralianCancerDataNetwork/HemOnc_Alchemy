import os
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as so

from hemonc_alchemy.model import entities
from hemonc_alchemy.model.base import Base, concrete_entities, register_enum_casts
from hemonc_alchemy.toolbox.loading import load_all

data_dir = Path("/workspace/hemonc-alchemy/data/Tables")
engine = sa.create_engine(os.environ["DATABASE_URL"])

# This script is a full rebuild for the disposable development database. The
# denormalised child tables are loaded with INSERTs, so dropping first also
# makes reruns after a partial import deterministic.
with engine.begin() as connection:
    inspector = sa.inspect(connection)
    for table_name in inspector.get_table_names():
        if table_name.startswith("_staging_"):
            quoted_name = connection.dialect.identifier_preparer.quote(table_name)
            connection.exec_driver_sql(f"DROP TABLE IF EXISTS {quoted_name} CASCADE")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
register_enum_casts()

source_entities = sorted(
    (
        cls for cls in concrete_entities(entities)
        if getattr(cls, "filename", None)
    ),
    key=lambda cls: cls.__tablename__,
)

with so.Session(engine) as session:
    for entity_cls in source_entities:
        counts = load_all(
            session,
            entity_cls,
            data_dir,
            chunksize=100_000,
        )
        session.commit()
        print(entity_cls.__tablename__, counts)
