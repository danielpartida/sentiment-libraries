from datetime import datetime, timedelta

from src.db.helper import get_session
from src.db.entities import TwitterStreams

if __name__ == "__main__":

    session = get_session()
    test = session.query(TwitterStreams).filter(
        TwitterStreams.domain_id == 66, TwitterStreams.date >= datetime.now() - timedelta(hours=12)
    ).order_by(TwitterStreams.id.asc()).all()

    session.close()

    print("Run")
