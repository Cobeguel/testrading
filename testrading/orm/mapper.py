from sqlalchemy import Table, Column, Numeric, Text, DateTime
from sqlalchemy.orm import registry
from typing import List

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


def map_table_ohlc(register: registry, table_name: str) -> Table:
	return Table(table_name, register.metadata, Column('row_name', Text, primary_key=True, nullable=False),
	             Column('create_time', DateTime), Column('provider', Text), Column('symbol', Text),
	             Column('time', DateTime), Column('open', Numeric(18, 8)), Column('high', Numeric(18, 8)),
	             Column('low', Numeric(18, 8)), Column('close', Numeric(18, 8)), Column('volume', Numeric(18, 8)))
