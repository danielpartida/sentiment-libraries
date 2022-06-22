from datetime import datetime, timedelta

from src.db.helper import get_session
from src.db.entities import TwitterStreams


def compute_word_clouds():
    pass


def query_last_streams(time_delta: timedelta) -> TwitterStreams:
    """
    Fetches last tweets using sqlalchemy ORM
    :param time_delta: time_delta e.g. datetime.now() - timedelta(hours=12)
    :type time_delta: timedelta
    :return: last twitter streams
    :rtype: TwitterStreams
    """
    last_streams = session.query(TwitterStreams).filter(
        TwitterStreams.domain_id == 66, TwitterStreams.date >= time_delta
    ).order_by(TwitterStreams.id.asc()).all()

    return last_streams


if __name__ == "__main__":

    session = get_session()

    delta = datetime.now() - timedelta(hours=12)
    last_tweets = query_last_streams(time_delta=delta)

    session.close()

    print("Run")
