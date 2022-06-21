import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():

    user = os.environ.get('POSTGRES_USR')
    pwd = os.environ.get('POSTGRES_PWD')
    db = os.environ.get('POSTGRES_DB')
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT')

    database_uri = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(database_uri)

    return engine


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
