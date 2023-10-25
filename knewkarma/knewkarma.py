def on_call():
    from datetime import datetime

    from .coreutils import __version__, args, log, path_finder
    from .messages import message
    from .tree_masonry import Masonry

    tree_masonry = Masonry()
    start_time = datetime.now()

    if args.mode:
        print(
            """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
        )

        try:
            path_finder()
            log.info(
                message(
                    message_type="info",
                    message_key="program_started",
                    version=__version__,
                    start_time=start_time,
                )
            )
            tree_masonry.api.check_updates()

            if args.mode == "user":
                if args.profile:
                    tree_masonry.tree_user_profile(
                        username=args.username,
                        save_to_csv=args.csv,
                        save_to_json=args.json,
                    )
                elif args.posts:
                    tree_masonry.tree_user_posts(
                        username=args.username,
                        sort=args.sort,
                        limit=args.limit,
                        save_to_json=args.json,
                    )
                elif args.comments:
                    tree_masonry.tree_user_comments(
                        username=args.username,
                        sort=args.sort,
                        limit=args.limit,
                        save_to_json=args.json,
                    )
            elif args.mode == "subreddit":
                if args.profile:
                    tree_masonry.tree_subreddit_profile(
                        subreddit=args.subreddit,
                        save_to_csv=args.csv,
                        save_to_json=args.json,
                    )
                elif args.posts:
                    tree_masonry.tree_subreddit_posts(
                        subreddit=args.subreddit,
                        sort=args.sort,
                        limit=args.limit,
                        save_to_json=args.json,
                    )
            elif args.mode == "search":
                tree_masonry.tree_search_results(
                    query=args.query,
                    sort=args.sort,
                    limit=args.limit,
                    save_to_json=args.json,
                )
            elif args.mode == "post":
                tree_masonry.tree_post_data(
                    post_id=args.post_id,
                    post_subreddit=args.post_subreddit,
                    sort=args.sort,
                    limit=args.limit,
                    show_comments=args.comments,
                    save_to_csv=args.csv,
                    save_to_json=args.json,
                )
            elif args.mode == "posts":
                if args.listings:
                    tree_masonry.tree_post_listings(
                        listing=args.listing,
                        sort=args.sort,
                        limit=args.limit,
                        save_to_json=args.json,
                    )
                elif args.frontpage:
                    tree_masonry.tree_front_page_posts(
                        sort=args.sort,
                        limit=args.limit,
                        save_to_json=args.json,
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
