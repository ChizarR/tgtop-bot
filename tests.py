from pprint import pprint

from config import Config
from services import posts_stats as ps
from services import TGStatAPI
from utils import my_types


def test():
    tg_api = TGStatAPI(Config.API_TOKEN)

    channels = [
        "https://t.me/joinchat/AAAAAEW7PysA07Xr68XQgg",
        # "https://t.me/joinchat/AAAAAEVZR6NQqIVytzIEJQ",
        # "@nationaI_geographic",
        # "@mir_animalsss",
        # "@sobake_n",
    ]

    posts_data = []

    for channel in channels:
        posts = tg_api.get_posts(channel)
        
        for post in posts:
            stats = tg_api.get_post_stats(post)
            posts_data.append(my_types.APIPostData(post=post, stats=stats))
        
        posts_analyse = ps.PostStats(posts_data)
        best_posts = posts_analyse.get_best_posts()
        pprint(best_posts, depth=3)
            

