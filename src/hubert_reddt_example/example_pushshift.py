from envt import e
from pmaw import PushshiftAPI
import requests
import os
import time
import pandas as pd

class Connect:
    """
    Supported: Pushshift, Reddit
    """
    def pushshift(self):
        subreddit_list = e['subreddit_list']
        limit = 1000000
        pushshift_inst = PushshiftAPI(shards_down_behavior='stop')
        return limit, pushshift_inst

    @staticmethod
    def twitter_bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """
        bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def twitter(self):
        r = requests.post('https://api.twitter.com/oauth2/token')
        r.headers["Authorization"] = f"Bearer {e['twitter_bearer_token']}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

class Get:
    def __init__(self):
        self.connect = Connect()

    def get_pushshift_comments(self, t1, t2, subreddit=['wallstreetbets']):
        """
        Get the comments from the Pushshift API and store them in a DF
        Note that before and after are switched for a reason I haven't been
        able to decipher just yet.
        If a request is made to get comments between t1 and t2 with t2 after t1,
        then you need to provide in the request before with t2 and after with t1.
        """
        if (type(t1) != int) or (type(t2) != int):
            type_t1 = type(t1)
            type_t2 = type(t2)
            raise TypeError(f"""Both arguments 'before' and 'after' should be of time
                                int (epoch timestamp), provided types: {type_t1}
                                for before and {type_t2} for after""")

        if isinstance(subreddit, str):
            subreddit = [subreddit]
        limit, inst = self.connect.pushshift()
        try:
            resp = inst.search_comments(subreddit=subreddit,
                                                limit=limit,
                                                safe_exit=True,
                                                mem_safe=False,
                                                after=t1,
                                                before=t2)
        except requests.exceptions.ConnectionError:
            # Connection fails, we try every 30 seconds, 3 tries
            time.sleep(30)
            if hasattr(self, 'retries_count'):
                self.retries_count += 1
            else:
                self.retries_count = 1
            self.log.warning(f"""Connection Failed, Restarting in
                                 30 seconds, Attempt {self.retries_count}
                                 out of 3""")
            return None
        except IndexError:
            return pd.DataFrame()
        except RuntimeError as run_err:
            self.log.warn(f"""Restarting the connection after a RuntimeError: {run_err}""")
            time.sleep(10)
            comments = self.get_pushshift_comments(t1, t2)
            return comments
        except Exception as e:
            raise RuntimeError(f"Could not fetch comments: {e}")
        comments = pd.DataFrame(resp)
        # need to sleep 1 second to avoid overloading the API
        time.sleep(1)
        return comments