import os
import yaml
import logging
from sqlalchemy import create_engine

logging.basicConfig(filename='database.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseConnection:
    __slots__ = ('db_name', 'credentials', 'engine')
    __instance = None

    def __init__(self, db_name: str) -> None:
            self.db_name = db_name
            # Check if there's another db with same name. (Singleton)
            self.credentials = self._get_credentials()
            self.engine = self._create_engine()

    def _get_credentials(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        config = os.path.join(cwd, "config.yaml")
        with open(config) as f:
            db_settings = yaml.safe_load(f)['database']
            try:
                conn_info = db_settings.get(self.db_name, None)
                # Check if conn_info and all its keys have values. Return credentials.
            except Exception as e:
                    logging.exception("An error has ocurred: %s", str(e))

    def _create_engine(self):
        try:
            create_engine(f'{0}+psycopg2://{1}:{2}@{3}:{4}/{5}')
        except:
            pass