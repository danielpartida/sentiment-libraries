from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

from src.db.helper import get_engine

load_dotenv()

Base = declarative_base()


class TwitterStreams(Base):
    __tablename__ = 'twitter_streams'
    domain_id = Column(Integer)
    entity_id = Column(BigInteger)
    entity_name = Column(String)
    language = Column(String)
    text = Column(String)
    tweet_id = Column(BigInteger, primary_key=True, autoincrement=False)
    # TODO: Add datetime column
    # TODO: Add serial id


if __name__ == "__main__":

    engine = get_engine()
    Base.metadata.create_all(engine)
