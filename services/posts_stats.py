from utils import my_types


class PostStats:
    def __init__(self, posts: list[my_types.APIPostData]) -> None:
        self.posts: list[my_types.APIPostData] = posts
        self.result: list = []
        self.shares_percent: dict = self._calculate_shares_persent()
        self.mean_shares_percent: float = self._calculate_mean_shares_percent()
        self.top_post_id: int = self.get_top_post()
        self.res_percent: float = self._calculate_res_percent()

    def get_best_posts(self):
        suitable_posts = self._sort_posts()
        for post in self.posts:
            curr_post = post.post
            if curr_post["id"] in suitable_posts.keys():
                self._add_to_result(post)
            else:
                continue
        return self.result

    def get_top_post(self):
        max_v = 0.0
        max_k = 0
        for k, v in self.shares_percent.items():
            if v > max_v:
                max_v = v
                max_k = k
        return max_k

    def _add_to_result(self, p):
        post = p.post
        stats = p.stats
        shares_count = stats["sharesCount"]
        shares_perc = self.shares_percent[post["id"]]
        self.result.append(my_types.Post(
            post=post,
            shares_count=shares_count,
            shares_percent=shares_perc
        ))

    def _calculate_shares_persent(self):
        shares_percent = {}
        for post in self.posts:
            stats = post.stats
            views = stats["viewsCount"]
            if views == 0:
                shares_percent[post.post["id"]] = 0
                continue
            shares = stats["sharesCount"]
            shares_percent[post.post["id"]] = (100 / views) * shares
        return shares_percent

    def _calculate_mean_shares_percent(self):
        res = float(sum(self.shares_percent.values()) / len(self.shares_percent))
        return res

    def _calculate_res_percent(self):
        top_post_v = self.shares_percent[self.top_post_id]
        res = (self.mean_shares_percent + top_post_v) / 2 
        return res

    def _sort_posts(self):
        res = {}
        for k, v in self.shares_percent.items():
            if v > self.res_percent:
                res[k] = v
        return res
