def on_call():
    import argparse

    from knewkarma.caller import Caller
    from . import __version__
    from .coreutils import datetime, log, path_finder
    from .masonry import Masonry
    from .parser import create_parser

    print(
        """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )
    parser: argparse.ArgumentParser = create_parser()
    arguments: argparse = parser.parse_args()
    tree_masonry: Masonry = Masonry()
    start_time: datetime = datetime.now()

    path_finder()
    try:
        if arguments.mode:
            log.info(f"Started [bold]Knew Karma[/] {__version__} at {start_time}...")
            tree_masonry.api.check_updates()

        caller = Caller(arguments=arguments, tree_masonry=tree_masonry)
        caller.call_cli()
    except KeyboardInterrupt:
        log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
    finally:
        log.info(f"Stopped in {datetime.now() - start_time} seconds.")
