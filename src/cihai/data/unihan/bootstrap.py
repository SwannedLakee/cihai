import typing as t

import sqlalchemy.sql.schema
import sqlalchemy
from sqlalchemy import Column, String, Table

from unihan_etl import process as unihan
from unihan_etl.constants import UNIHAN_MANIFEST
from unihan_etl.util import merge_dict

from .constants import UNIHAN_ETL_DEFAULT_OPTIONS, UNIHAN_FIELDS


def bootstrap_unihan(
    engine: sqlalchemy.Engine,
    metadata: sqlalchemy.sql.schema.MetaData,
    options: t.Optional[t.Dict[str, object]] = None,
) -> None:
    if options is None:
        options = {}

    """Download, extract and import unihan to database."""
    options = merge_dict(UNIHAN_ETL_DEFAULT_OPTIONS.copy(), options)

    unihan_pkgr = unihan.Packager(options)
    unihan_pkgr.download()
    data = unihan_pkgr.export()
    table = create_unihan_table(UNIHAN_FIELDS, metadata)

    metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(sqlalchemy.insert(table), data)
        conn.commit()


TABLE_NAME = "Unihan"


DEFAULT_COLUMNS = ["ucn", "char"]
try:
    DEFAULT_FIELDS = [f for c, f in UNIHAN_MANIFEST.items() if c in ["Unihan"]]
except Exception:
    DEFAULT_FIELDS = [f for f in UNIHAN_MANIFEST.values()]


def is_bootstrapped(metadata: sqlalchemy.sql.schema.MetaData) -> bool:
    """Return True if cihai is correctly bootstrapped."""
    fields = UNIHAN_FIELDS + DEFAULT_COLUMNS
    if TABLE_NAME in metadata.tables.keys():
        table = metadata.tables[TABLE_NAME]

        if set(fields) == {c.name for c in table.columns}:
            return True
        else:
            return False
    else:
        return False


def create_unihan_table(
    columns: t.List[str], metadata: sqlalchemy.sql.schema.MetaData
) -> sqlalchemy.sql.schema.Table:
    """Create table and return  :class:`sqlalchemy.Table`.

    Parameters
    ----------
    columns : list
        columns for table, e.g. ``['kDefinition', 'kCantonese']``
    metadata : :class:`sqlalchemy.schema.MetaData`
        Instance of sqlalchemy metadata

    Returns
    -------
    :class:`sqlalchemy.schema.Table` :
        Newly created table with columns and index.
    """

    if TABLE_NAME not in metadata.tables:
        table = Table(TABLE_NAME, metadata)

        table.append_column(Column("char", String(12), primary_key=True))
        table.append_column(Column("ucn", String(12), primary_key=True))

        for column_name in columns:
            col = Column(column_name, String(256), nullable=True)
            table.append_column(col)

        return table
    else:
        return Table(TABLE_NAME, metadata)
