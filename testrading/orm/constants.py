from dataclasses import dataclass


@dataclass(frozen=True)
class Database:
    undefined = 'UNDEFINED'
    unknown = 'UNKNOWN'
