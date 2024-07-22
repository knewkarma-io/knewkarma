import time

from rich.console import Console

console = Console()
with console.status(
    "Establishing new connection/session...", spinner="dots2"
) as status:
    status.start()
    time.sleep(20)
    print("Oleeeeeeeeeeeee")
