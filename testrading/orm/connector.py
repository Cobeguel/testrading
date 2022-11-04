import mapping
import definitions
import yaml

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm.session import Session
from testrading.models import financial


def build_conn_url() -> str:
	url = ""
	with open(definitions.DB_CONFIG_FILE, 'r') as db_config_file:
		try:
			db_config = yaml.safe_load(db_config_file)
			driver_dialect = db_config['driver']
			if db_config['dialect'] != "":
				driver_dialect += '+' + db_config['dialect']
			url += driver_dialect + '://' + db_config['username'] + ':' + db_config['password'] + '@'
			url += db_config['host'] + '/' + db_config['database']

		except yaml.YAMLError as exc:
			print(exc)
		except KeyError as exc:
			print(exc)
	return url


def start_mappers(register: registry):
	register.map_imperatively(financial.ohlcv, mapping.map_table_ohlc(register, 'ohlcv'))
	return register


metadata = MetaData()
mapper_registry = registry(metadata=metadata)
engine = create_engine(build_conn_url())
start_mappers(mapper_registry)
session = Session(bind=engine)
metadata.create_all(engine)

session.add(financial.ohlcv())
session.commit()
