from sqlalchemy import Table, Column, Numeric, Text, DateTime, Integer
from sqlalchemy.orm import registry
from typing import List
from testrading.orm import constants

ohlcvbase = [
    Column('id', Text, primary_key=True, nullable=False),
    Column('create_time', DateTime),
    Column('provider', Text),
    Column('symbol', Text),
    Column('datetime', DateTime),
    Column('open', Numeric(18, 8)),
    Column('high', Numeric(18, 8)),
    Column('low', Numeric(18, 8)),
    Column('close', Numeric(18, 8)),
    Column('adj_close', Numeric(18, 8)),
    Column('volume', Numeric(18, 8))
]


def append_columns(table: Table, columns: List[Column]) -> None:
    for column in columns:
        table.append_column(column)


# yapf: disable
def map_table_ohlc(register: registry, table_name: str) -> Table:
    return Table(
      table_name,
      register.metadata, Column('id', Text, primary_key=True, nullable=False, key= '_id'),
      Column('create_time', DateTime, nullable=False),
      Column('provider', Text, nullable=False),
      Column('asset', Text, nullable=False),
      Column('symbol', Text, nullable=False),
      Column('resolution', Integer, nullable=False),
      Column('datetime', DateTime, nullable=False, key='time'),
      Column('open', Numeric(18, 8), nullable=False),
      Column('high', Numeric(18, 8), nullable=False),
      Column('low', Numeric(18, 8), nullable=False),
      Column('close', Numeric(18, 8), nullable=False),
      Column('volume', Numeric(18, 8), server_default='0')
    )
# yapf: enable


# yapf: disable
def map_table_provider(register: registry, table_name: str) -> Table:
    return Table(
        table_name,
        register.metadata, Column('id', Text, primary_key=True, nullable=False, key= '_id'),
        Column('create_time', DateTime, nullable=False),
        Column('name', Text, nullable=False),
        Column('last_version', Text, nullable=False)
    )
# yapf: enable


# yapf: disable
def map_table_asset(register: registry, table_name: str) -> Table:
    return Table(
        table_name,
        register.metadata, Column('id', Text, primary_key=True, nullable=False, key= '_id'),
        Column('create_time', DateTime, nullable=False),
        Column('name', Text, nullable=False),
        Column('last_version', Text, nullable=False)
    )
# yapf: enable