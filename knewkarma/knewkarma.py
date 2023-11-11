def on_call():
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
    parser = create_parser()
    tree_masonry = Masonry()
    start_time = datetime.now()

    if parser.parse_args().mode:
        executor = Executor(arguments=parser.parse_args(), tree_masonry=tree_masonry)
        path_finder()
        try:
            log.info(
                message(
                    message_type="info",
                    message_key="program_started",
                    program_name=f"Knew Karma",
                    program_version=__version__,
                    start_time=start_time.strftime("%a %b %d %Y, %H:%M:%S"),
                )
            )
            tree_masonry.api.check_updates()
            executor.execute_cli_arguments()
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
        parser.print_usage()
