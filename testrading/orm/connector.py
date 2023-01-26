import testrading.orm.mapper as mapper
import definitions
import yaml
import toml
import threading

from sqlalchemy import MetaData, create_engine, future
from sqlalchemy.orm import registry
from sqlalchemy.orm.session import Session
from testrading.models import financial
from dataclasses import dataclass


@dataclass
class DBCredentials:
    """
		String connection has the form:
		dialect+driver://username:password@host:port/database
	"""
    filename: str
    dialect: str = ""
    driver: str = ""
    username: str = ""
    password: str = ""
    host: str = ""
    port: str = ""
    database: str = ""

    def __init__(self, filename: str):
        db_params = {}
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            with open(filename, 'r') as db_config_file:
                try:
                    db_params = yaml.safe_load(db_config_file)
                except yaml.YAMLError as exc:
                    print(exc)  # TODO: HANDLE exception
        elif filename.endswith('.toml'):
            import toml
            with open(filename, 'r') as db_config_file:
                try:
                    db_params = toml.load(db_config_file)
                except toml.TomlDecodeError as exc:
                    print(exc)  # TODO: HANDLE exception
        else:
            raise ValueError(f"File {filename} is not found or supported. A yaml or toml file is expected")

        self.dialect = db_params['dialect']
        self.driver = db_params['driver']
        self.username = db_params['username']
        self.password = db_params['password']
        self.host = db_params['host']
        self.port = db_params['port']
        self.database = db_params['database']

    @property
    def db_engine_name(self) -> str:
        if self.dialect != "":
            if self.driver != "":
                return f"{self.dialect}+{self.driver}"
            else:
                return self.dialect
        else:
            return self.driver

    def __str__(self):
        return self.db_engine_name + f"://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


def start_mappers(register: registry):
    register.map_imperatively(financial.OHLCV, mapper.map_table_ohlc(register, 'ohlcv'))
    register.map_imperatively(financial.Provider, mapper.map_table_provider(register, 'providers'))
    register.map_imperatively(financial.Asset, mapper.map_table_asset(register, 'assets'))
    return register


class Singleton(type):
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class AlchemyConn(metaclass=Singleton):

    def __init__(self, str_conn: str):
        self.str_conn = str_conn
        self.metadata = MetaData()
        self.mapper_registry = registry(metadata=self.metadata)
        self.engine = create_engine(self.str_conn)
        start_mappers(self.mapper_registry)
        self.metadata.create_all(self.engine)

    def get_engine(self):
        return self.engine

    def get_conn(self):
        return self.engine.connect()

    def get_session(self):
        return Session(bind=self.engine)

    def get_tables_names(self):
        return self.metadata.tables.keys()
