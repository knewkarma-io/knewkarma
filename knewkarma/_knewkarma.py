# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def on_call():
    import asyncio
    import cProfile
    import pstats

    from . import api
    from ._cli import Cli
    from ._coreutils import datetime, log, path_finder, arguments, create_parser
    from ._masonry import Masonry
    from ._metadata import version

    print(
        """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )

    start_time: datetime = datetime.now()

    if arguments.mode:
        path_finder()
        try:
            log.info(
                f"[bold]Knew Karma[/] {version} started at "
                f"{start_time.strftime('%a %b %d %Y, %I:%M:%S %p')}..."
            )
            profiler = cProfile.Profile()
            profiler.enable()

            asyncio.run(api.get_updates())
            cli = Cli(arguments=arguments, tree_masonry=Masonry(api=api))
            cli.execute_cli()

            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats("cumulative").print_stats(10)
        except KeyboardInterrupt:
            log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        create_parser().print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
