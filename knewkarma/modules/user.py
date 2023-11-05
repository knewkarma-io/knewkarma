from rich import print

from knewkarma.brokers import Broker
from knewkarma.coreutils import save_data, convert_timestamp_to_datetime
from knewkarma.masonry import Masonry


class User:
    def __init__(self, username: str, tree_masonry: Masonry, data_broker: Broker):
        self.api = tree_masonry.api
        self.data_broker = data_broker
        self.tree_masonry = tree_masonry
        self.username = username

    def profile(self, save_to_json: bool, save_to_csv: bool):
        raw_profile = self.api.get_user_profile(username=self.username)
        if raw_profile:
            (
                profile,
                subreddit,
                verification,
                snoovatar,
                karma,
            ) = self.data_broker.user_data(raw_data=raw_profile)

            print(
                self.tree_masonry.create_tree(
                    tree_title=raw_profile.get("subreddit").get("title"),
                    tree_data=profile,
                    additional_data=[
                        ("Snoovatar", snoovatar),
                        (raw_profile.get("subreddit").get("display_name"), subreddit),
                        ("Verification", verification),
                        ("Karma", karma),
                    ],
                )
            )

            save_data(
                data=raw_profile,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{self.username}_profile",
            )

    def posts(self, sort_criterion: str, posts_limit: int, save_to_json: bool):
        self.tree_masonry.posts_tree(
            posts_source=self.username,
            posts_type="user_posts",
            posts_limit=posts_limit,
            sort_criterion=sort_criterion,
            save_to_json=save_to_json,
        )

    def comments(self, sort_criterion: str, comments_limit: int, save_to_json: bool):
        comments_tree = self.tree_masonry.create_tree(
            tree_title=f"Visualising {self.username}'s [green]{sort_criterion}[/] [cyan]{comments_limit}[/] comments"
        )

        raw_comments = self.api.get_posts(
            sort_criterion=sort_criterion,
            posts_limit=comments_limit,
            posts_type="user_comments",
            posts_source=self.username,
        )

        if raw_comments:
            for raw_comment in raw_comments:
                raw_comment_data = raw_comment.get("data")
                self.tree_masonry.add_branch(
                    target_tree=comments_tree,
                    branch_title=convert_timestamp_to_datetime(
                        timestamp=raw_comment_data.get("created")
                    ),
                    branch_data=self.data_broker.comment_data(
                        raw_comment=raw_comment_data
                    ),
                    additional_text=raw_comment_data.get("body"),
                )
            print(comments_tree)

            save_data(
                data=raw_comments[0],
                save_to_json=save_to_json,
                filename=f"{self.username}_comments",
            )
