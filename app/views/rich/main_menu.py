from rich.console import Console
from app.models.appstate import AppState
from app.views.banner import print_banner
from app.views.rich.active_filters_panel import render_active_filters_panel_rich


def render_main_menu_rich(state: AppState, console: Console, error: str | None = None):
    console.clear()
    print_banner()

    render_active_filters_panel_rich(state, console)

    console.print("\n[bold]Main Menu[/bold]")
    console.print("1) View dataset")
    console.print("2) Filters")
    console.print("99) Quit")
    if error:
        console.print(f"[red]{error}[/red]")
