from dataclasses import dataclass
from ksuid import Ksuid
from datetime import datetime
from decimal import Decimal


@dataclass
class Provider:
    _id: str = str(Ksuid())
    create_time: datetime = datetime.now()
    name: str = ""
    last_version: str = ""

    def __post_init__(self):
        self._id = str(Ksuid())
        self.create_time = datetime.now()


@dataclass
class Asset:
    _id: str = str(Ksuid())
    create_time: datetime = datetime.now()
    name: str = ""
    last_version: str = ""

    def __post_init__(self):
        self._id = str(Ksuid())
        self.create_time = datetime.now()


@dataclass
class Symbol:
    _id: str = str(Ksuid())
    create_time: datetime = datetime.now()
    name: str = ""
    last_version: str = ""

    def __post_init__(self):
        self._id = str(Ksuid())
        self.create_time = datetime.now()


@dataclass
class OHLCV:
    _id: str = str(Ksuid())
    create_time: datetime = datetime.now()
    provider: str = ""
    asset: str = ""
    symbol: str = ""
    resolution: int = 0
    time: datetime = datetime.now()
    open: Decimal = Decimal()
    high: Decimal = Decimal()
    low: Decimal = Decimal()
    close: Decimal = Decimal()
    volume: Decimal = Decimal()

    def __post_init__(self):
        self._id = str(Ksuid())


@dataclass
class Tick:
    _id: str = str(Ksuid())
    create_time: datetime = datetime.now()
    provider: str = ""
    asset: str = ""
    symbol: str = ""
    time: datetime = datetime.now()
    bid: Decimal = Decimal()
    ask: Decimal = Decimal()
    volume: Decimal = Decimal()

    def __post_init__(self):
        self._id = str(Ksuid())


@dataclass
class Trades:
    _id: str = str(Ksuid())
    create_time: datetime = datetime.now()
    provider: str = ""
    symbol: str = ""
    time: datetime = datetime.now()
    price: Decimal = Decimal()
    quantity: Decimal = Decimal()

    def __post_init__(self):
        self._id = str(Ksuid())
