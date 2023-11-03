def on_call():
    from . import __version__
    from .executor import Executor
    from .coreutils import arguments, datetime, log, path_finder
    from .masonry import Masonry
    from .messages import message

    print(
        """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )

    tree_masonry = Masonry()
    start_time = datetime.now()
    executor = Executor(arguments=arguments, tree_masonry=tree_masonry)

    path_finder()
    try:
        executor_title = (
            "Command-Line Arguments"
            if arguments.mode
            else "Interactive Command-Line Wizard"
        )
        log.info(
            message(
                message_type="info",
                message_key="program_started",
                program_name=f"Knew Karma",
                executor_title=executor_title,
                program_version=__version__,
                start_time=start_time.strftime("%a %b %d %Y, %H:%M:%S %p"),
            )
        )
        tree_masonry.api.check_updates()
        if arguments.mode:
            executor.execute_cli_arguments()
        else:
            executor.execute_cli_wizards()
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
