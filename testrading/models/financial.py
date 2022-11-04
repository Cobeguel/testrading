from dataclasses import dataclass
from ksuid import Ksuid
from datetime import datetime


@dataclass
class provider:
	_id: str = str(Ksuid())
	create_time: datetime = datetime.now()
	name: str = ""


@dataclass
class ohlcv:
	_id: str = str(Ksuid())
	create_time: datetime = datetime.now()
	provider: str = ""
	symbol: str = ""
	time: datetime = datetime.now()
	open: float = 0.0
	high: float = 0.0
	low: float = 0.0
	close: float = 0.0
	volume: float = 0.0


@dataclass
class tick:
	_id: str = str(Ksuid())
	create_time: datetime = datetime.now()
	provider: str = ""
	symbol: str = ""
	time: datetime = datetime.now()
	bid: float = 0.0
	ask: float = 0.0
	volume: float = 0.0


@dataclass
class tades:
	_id: str = str(Ksuid())
	create_time: datetime = datetime.now()
	provider: str = ""
	symbol: str = ""
	time: datetime = datetime.now()
	price: float = 0.0
	quantity: float = 0.0
