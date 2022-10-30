import requests


CHANNEL_POSTS_URL = "https://api.tgstat.ru/channels/posts"
POST_STATS_URL = "https://api.tgstat.ru/posts/stat"


class LimitError(Exception):
    pass

class RequestError(Exception):
    pass


class TGStatAPI:
    def __init__(self, token):
        self._token = token

    def get_posts(self, channel_id, limit=20):
        if limit > 50:
            raise LimitError(f"Too big limit: {limit}")
        params = {"token":self._token, "channelId": channel_id, "limit": limit}
        r = requests.get(CHANNEL_POSTS_URL, params=params, timeout=5).json()

        if r["status"] != "ok":
            raise RequestError("Error in request params...")

        return r["response"]["items"]

    def get_post_stats(self, post):
        post_id = post["id"]
        params = {"token": self._token, "postId": post_id}
        r = requests.get(POST_STATS_URL, params=params, timeout=5).json()

        if r["status"] != "ok":
            raise RequestError("Error in request params...")

        return r["response"]
