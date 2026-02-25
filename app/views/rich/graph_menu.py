from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.models.appstate import AppState
from app.views.rich.active_filters_panel import render_active_filters_panel_rich
from app.views.rich.columns_menu import create_all_columns_panel


def render_graph_menu_rich(state: AppState, console: Console, error: str | None = None) -> None:
    """
    Render graph creation menu

    Args:
        state (AppState): application state controller
        console (Console): Rich Console
        error (str | None): Optional error text

    Returns:
        None
    """
    console.clear()
    render_active_filters_panel_rich(state, console)

    lines = [
        "[bold]Graphs run on current filtered/transformed dataset[/bold]",
        "Select an x column and y column to generate graph image",
    ]

    console.print(Panel("\n".join(lines), title="Graph Context", border_style="cyan", expand=True))

    menu = Table(show_header=False, show_edge=False, padding=(0, 1))
    menu.add_row("[bold cyan]1)[/]", "Create line graph")
    menu.add_row("[bold cyan]2)[/]", "Create bar graph")
    menu.add_row("[bold]0)[/]", "Back to main menu")

    menu_panel = Panel(menu, title="Graph Menu", border_style="green", expand=False)
    columns_panel = create_all_columns_panel(state, title="All Columns")
    console.print(Columns([menu_panel, columns_panel], expand=True, equal=True))

    if error:
        console.print(f"[red]{error}[/red]")
