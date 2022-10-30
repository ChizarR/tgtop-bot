from typing import NamedTuple


class APIPostData(NamedTuple):
    post: dict
    stats: dict


class Post(NamedTuple):
    post: dict
    shares_count: int
    shares_percent: float   
