def on_call():
    import argparse

    from . import __version__
    from .coreutils import datetime, log, path_finder
    from .executor import Executor
    from .masonry import Masonry
    from .messages import message
    from .parser import create_parser

    print(
        """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )
    parser: argparse.ArgumentParser = create_parser()
    masonry: Masonry = Masonry()
    start_time: datetime = datetime.now()

    path_finder()
    try:
        if parser.parse_args().mode:
            log.info(
                message(
                    message_type="info",
                    message_key="program_started",
                    program_name=f"Knew Karma",
                    program_version=__version__,
                    start_time=start_time.strftime("%a %b %d %Y, %H:%M:%S"),
                )
            )
            masonry.api.check_updates()

        Executor(arguments=parser.parse_args(), tree_masonry=masonry).cli()
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
