import asyncio
from datetime import datetime

from .coreutils import __version__, args, banner, check_updates, log
from .masonry import TreeMasonry
from .messages import message


def on_call():
    tree_masonry = TreeMasonry()
    start_time = datetime.now()

    if args.mode:
        try:
            print(banner())
            log.info(
                message(
                    message_type="info",
                    message_key="program_started",
                    program_name="Knew Karma",
                    program_version=__version__,
                    start_time=start_time,
                )
            )
            asyncio.run(check_updates())

            if args.mode == "user":
                if args.profile:
                    asyncio.run(tree_masonry.tree_user_profile(username=args.username))
                elif args.posts:
                    asyncio.run(
                        tree_masonry.tree_user_posts(
                            username=args.username, sort=args.sort, limit=args.limit
                        )
                    )
                elif args.comments:
                    asyncio.run(
                        tree_masonry.tree_user_comments(
                            username=args.username, sort=args.sort, limit=args.limit
                        )
                    )
            elif args.mode == "subreddit":
                if args.profile:
                    asyncio.run(
                        tree_masonry.tree_subreddit_profile(subreddit=args.subreddit)
                    )
                elif args.posts:
                    asyncio.run(
                        tree_masonry.tree_subreddit_posts(
                            subreddit=args.subreddit, sort=args.sort, limit=args.limit
                        )
                    )
            elif args.mode == "search":
                asyncio.run(
                    tree_masonry.tree_search_results(
                        query=args.query, sort=args.sort, limit=args.limit
                    )
                )
            elif args.mode == "post":
                asyncio.run(tree_masonry.tree_post_data(arguments=args))
            elif args.mode == "posts":
                if args.listings:
                    asyncio.run(
                        tree_masonry.tree_post_listings(
                            listing=args.listing,
                            sort=args.sort,
                            limit=args.limit,
                        )
                    )
                elif args.frontpage:
                    asyncio.run(
                        tree_masonry.tree_front_page_posts(
                            sort=args.sort,
                            limit=args.limit,
                        )
                    )
        except KeyboardInterrupt:
            log.warning(
                message(
                    message_type="warning",
                    message_key="user_interruption",
                )
            )
        finally:
            log.info(
                message(
                    message_type="info",
                    message_key="program_stopped",
                    run_time=datetime.now() - start_time,
                )
            )
    else:
        log.info(message(message_type="info", message_key="help"))
