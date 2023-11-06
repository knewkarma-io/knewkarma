from rich import print

from knewkarma.brokers import Broker
from knewkarma.coreutils import save_data
from knewkarma.masonry import Masonry


class Subreddit:
    def __init__(self, subreddit: str, tree_masonry: Masonry, data_broker: Broker):
        self.api = tree_masonry.api
        self.data_broker = data_broker
        self.tree_masonry = tree_masonry
        self.subreddit = subreddit

    def profile(self, save_to_json: bool, save_to_csv: bool):
        raw_profile = self.api.get_subreddit_profile(subreddit=self.subreddit)

        if raw_profile:
            (
                profile,
                allows,
                banner,
                header,
                flair,
            ) = self.data_broker.subreddit_data(raw_data=raw_profile)

            print(
                self.tree_masonry.create_tree(
                    tree_title=raw_profile.get("public_description"),
                    tree_data=profile,
                    additional_data=[
                        ("Allows", allows),
                        ("Banner", banner),
                        ("Header", header),
                        ("Flairs", flair),
                    ],
                    additional_text=raw_profile.get("submit_text"),
                )
            )

            save_data(
                data=raw_profile,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{self.subreddit}_profile",
            )

    def posts(self, sort_criterion: str, posts_limit: int, save_to_json: bool):
        self.tree_masonry.posts_tree(
            posts_source=self.subreddit,
            posts_type="subreddit_posts",
            posts_limit=posts_limit,
            sort_criterion=sort_criterion,
            save_to_json=save_to_json,
        )
