import os
from typing import Self
import yaml
import logging
import sqlalchemy as sql


class DatabaseConnection:
    __slots__ = ("db_name", "credentials", "engine", "logger")
    __instances = {}

    def __new__(cls, db_name):
        if db_name not in cls.__instances:
            instance = super(DatabaseConnection, cls).__new__(cls)
            instance.db_name = db_name
            instance.logger = instance._get_logger()
            instance.credentials = instance._get_credentials()
            instance.engine = instance._create_engine()
            cls.__instances[db_name] = instance
        return cls.__instances[db_name]

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.logger = self._get_logger()
        self.credentials = self._get_credentials()
        self.engine = self._create_engine()

    def _get_credentials(self) -> dict:
        cwd = os.path.dirname(os.path.realpath(__file__))
        config = os.path.join(cwd, "..", "config.yaml")
        with open(config) as f:
            db_settings = yaml.safe_load(f)["database"]["connections"]
            try:
                conn_info = db_settings[self.db_name]
                return conn_info
            except KeyError as ke:
                self.logger.exception("Failed to load DB credentials: %s", str(ke))
                raise ke

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger("database")
        logger.setLevel(logging.DEBUG)
        cwd = os.path.dirname(os.path.realpath(__file__))
        logs_dir = os.path.join(cwd, "..", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        logger.addHandler(
            logging.FileHandler(
                filename=os.path.join(logs_dir, f"{self.db_name}_database.log"),
                mode="a",
            )
        )
        logger.handlers[0].setFormatter(
            logging.Formatter(
                fmt="%(asctime)s ::: [%(levelname)s] >>> %(message)s",
                datefmt="%d/%m/%Y - %I:%M:S",
            )
        )
        return logger

    def _create_engine(self) -> sql.Engine:
        try:
            return sql.create_engine(
                "{dialect}+{driver}://{username}:{password}@{host}:{port}/{schema}".format(
                    **self._get_credentials()
                )
            )
        except ConnectionError as ce:
            self.logger.exception("Failed to instantiate engine: %s", str(ce))
            raise ce
