from sqlalchemy import create_engine
import logging

def connection(host, user, password, database):
    engine = create_engine(f'mysql+pymysql://${user}:${password}@/${host}/${database}')
