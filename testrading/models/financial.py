from dataclasses import dataclass
from ksuid import Ksuid
from datetime import datetime
from decimal import Decimal


@dataclass
class provider:
	_id: str = str(Ksuid())
	create_time: datetime = datetime.now()
	name: str = ""


@dataclass
class ohlcv:
	row_name: str = str(Ksuid())
	create_time: datetime = datetime.now()
	provider: str = ""
	symbol: str = ""
	time: datetime = datetime.now()
	open: Decimal = Decimal()
	high: Decimal = Decimal()
	low: Decimal = Decimal()
	close: Decimal = Decimal()
	volume: Decimal = Decimal()


@dataclass
class tick:
	row_name: str = str(Ksuid())
	create_time: datetime = datetime.now()
	provider: str = ""
	symbol: str = ""
	time: datetime = datetime.now()
	bid: Decimal = Decimal()
	ask: Decimal = Decimal()
	volume: Decimal = Decimal()


@dataclass
class trades:
	row_name: str = str(Ksuid())
	create_time: datetime = datetime.now()
	provider: str = ""
	symbol: str = ""
	time: datetime = datetime.now()
	price: Decimal = Decimal()
	quantity: Decimal = Decimal()
