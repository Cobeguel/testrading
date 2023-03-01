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
    provider: str = ""
    asset: str = ""
    symbol: str = ""
    resolution: int = 0
    ts_datetime: datetime = datetime.now()
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
class Resolution:
    name: str
    seconds: int

    def get_seconds_pandas_resample(self):
        return str(self.seconds) + 'S'

    def from_seconds(seconds: int):
        if seconds == res_seconds_5.seconds:
            return Resolution(name=res_seconds_5.name, seconds=res_seconds_5.seconds)
        elif seconds == res_seconds_15.seconds:
            return Resolution(name=res_seconds_15.name, seconds=res_seconds_15.seconds)
        elif seconds == res_seconds_30.seconds:
            return Resolution(name=res_seconds_30.name, seconds=res_seconds_30.seconds)
        elif seconds == res_minute_1.seconds:
            return Resolution(name=res_minute_1.name, seconds=res_minute_1.seconds)
        elif seconds == res_minute_5.seconds:
            return Resolution(name=res_minute_5.name, seconds=res_minute_5.seconds)
        elif seconds == res_minute_15.seconds:
            return Resolution(name=res_minute_15.name, seconds=res_minute_15.seconds)
        elif seconds == res_minute_30.seconds:
            return Resolution(name=res_minute_30.name, seconds=res_minute_30.seconds)
        elif seconds == res_hour_1.seconds:
            return Resolution(name=res_hour_1.name, seconds=res_hour_1.seconds)
        elif seconds == res_hour_2.seconds:
            return Resolution(name=res_hour_2.name, seconds=res_hour_2.seconds)
        elif seconds == res_hour_4.seconds:
            return Resolution(name=res_hour_4.name, seconds=res_hour_4.seconds)
        elif seconds == res_day.seconds:
            return Resolution(name=res_day.name, seconds=res_day.seconds)
        elif seconds == res_month.seconds:
            return Resolution(name=res_month.name, seconds=res_month.seconds)
        elif seconds == res_year.seconds:
            return Resolution(name=res_year.name, seconds=res_year.seconds)

        return None

    def get_next_resolution(self):
        if self.seconds == res_seconds_5.seconds:
            return res_seconds_15
        elif self.seconds == res_seconds_15.seconds:
            return res_seconds_30
        elif self.seconds == res_seconds_30.seconds:
            return res_minute_1
        elif self.seconds == res_minute_1.seconds:
            return res_minute_5
        elif self.seconds == res_minute_5.seconds:
            return res_minute_15
        elif self.seconds == res_minute_15.seconds:
            return res_minute_30
        elif self.seconds == res_minute_30.seconds:
            return res_hour_1
        elif self.seconds == res_hour_1.seconds:
            return res_hour_2
        elif self.seconds == res_hour_2.seconds:
            return res_hour_4
        elif self.seconds == res_hour_4.seconds:
            return res_day
        elif self.seconds == res_day.seconds:
            return res_month
        elif self.seconds == res_month.seconds:
            return res_year

        return None


res_seconds_5_name = '5 seconds'
res_seconds_15_name = '15 seconds'
res_seconds_30_name = '30 seconds'
res_minute_1_name = '1 minute'
res_minute_5_name = '5 minutes'
res_minute_15_name = '15 minutes'
res_minute_30_name = '30 munutes'
res_hour_1_name = '1 hour'
res_hour_2_name = '2 hour'
res_hour_4_name = '4 hour'
res_day_name = 'daily'
res_month_name = 'monthly'
res_year_name = 'yearly'

res_seconds_5 = Resolution(name='5 seconds', seconds=5)
res_seconds_15 = Resolution(name='15 seconds', seconds=15)
res_seconds_30 = Resolution(name='30 seconds', seconds=30)
res_minute_1 = Resolution(name='1 minute', seconds=60)
res_minute_5 = Resolution(name='5 minutes', seconds=300)
res_minute_15 = Resolution(name='15 minutes', seconds=900)
res_minute_30 = Resolution(name='30 munutes', seconds=1800)
res_hour_1 = Resolution(name='1 hour', seconds=3600)
res_hour_2 = Resolution(name='2 hour', seconds=7200)
res_hour_4 = Resolution(name='4 hour', seconds=14400)
res_day = Resolution(name='daily', seconds=86400)
res_month = Resolution(name='monthly', seconds=2592000)
res_year = Resolution(name='yearly', seconds=31536000)

# yapf: disable
resolutions_str = [
    res_seconds_5.name,
    res_seconds_15.name,
    res_seconds_30.name,
    res_minute_1.name,
    res_minute_5.name,
    res_minute_15.name,
    res_minute_30.name,
    res_hour_1.name,
    res_hour_2.name,
    res_hour_4.name,
    res_day.name,
    res_month.name,
    res_year.name
]
# yapf: enable

# yapf: disable
resolution_seconds = [
    res_seconds_5.seconds,
    res_seconds_15.seconds,
    res_seconds_30.seconds,
    res_minute_1.seconds,
    res_minute_5.seconds,
    res_minute_15.seconds,
    res_minute_30.seconds,
    res_hour_1.seconds,
    res_hour_2.seconds,
    res_hour_4.seconds,
    res_day.seconds,
    res_month.seconds,
    res_year.seconds
]
# yapf: enable
