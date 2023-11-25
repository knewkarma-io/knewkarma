def on_call():
    from . import __version__
    from .executor import Executor
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
                f"[bold]Knew Karma[/] {__version__} started at "
                f"{start_time.strftime('%a %b %d %Y, %I:%M:%S %p')}..."
            )

        tree_masonry.api.get_updates()
        executor = Executor(arguments=arguments, tree_masonry=tree_masonry)
        executor.executor_cli()
    except KeyboardInterrupt:
        log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
    finally:
        log.info(f"Stopped in {datetime.now() - start_time} seconds.")
