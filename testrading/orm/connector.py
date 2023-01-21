import testrading.orm.mapper as mapper
import definitions
import yaml
import toml

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
	register.map_imperatively(financial.ohlcv, mapper.map_table_ohlc(register, 'ohlcv'))
	return register


@dataclass
class AlchemyConn:
	str_conn: str
	metadata: MetaData = None
	mapper_registry: registry = None
	engine: future.Engine = None
	session: Session = None

	def __init__(self, str_conn: str):
		self.str_conn = str_conn
		self.metadata = MetaData()
		self.mapper_registry = registry(metadata=self.metadata)
		self.engine = create_engine(self.str_conn)
		start_mappers(self.mapper_registry)
		self.metadata.create_all(self.engine)

	def close(self):
		self.session.close()

	def Session(self) -> Session:
		return Session(bind=self.engine)
