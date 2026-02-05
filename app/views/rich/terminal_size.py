"""
Intial init screen for checking terminal size and resizing if possible or showing a warning if not.
"""

from rich.console import Console
from rich.panel import Panel

def render_terminal_size_check_rich(console: Console, min_width: int, min_height: int) -> None:
    console.clear()
    
    w = console.size.width
    h = console.size.height
    
    msg = (
        f"[bold yellow]Terminal too small[/bold yellow]\n\n"
        f"Current: [bold]{w}x{h}[/bold]\n"
        f"Recommended: [bold]{min_width}x{min_height}[/bold]\n\n"
        "Resize your terminal if you can.\n"
        "Press any key to continue."
    )
    console.print(Panel(msg, border_style="yellow", expand=False))
    console.input()
