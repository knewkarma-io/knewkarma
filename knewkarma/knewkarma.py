def on_call():
    from . import __version__
    from .caller import Caller
    from .coreutils import datetime, log, path_finder, arguments
    from .masonry import Masonry

    print(
        """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )
    tree_masonry: Masonry = Masonry()
    start_time: datetime = datetime.now()

    path_finder()
    try:
        if arguments.mode:
            log.info(
                f"Started [bold]Knew Karma[/] {__version__} at "
                f"{start_time.strftime('%a %b %d %Y, %I:%M:%S %p')}..."
            )
            tree_masonry.api.check_updates()

        caller = Caller(arguments=arguments, tree_masonry=tree_masonry)
        caller.call_cli()
    except KeyboardInterrupt:
        log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
    finally:
        log.info(f"Stopped in {datetime.now() - start_time} seconds.")
