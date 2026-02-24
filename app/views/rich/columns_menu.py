from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from app.models.appstate import AppState

def create_all_columns_panel(state: AppState, title: str = "Columns") -> Panel:
    table = Table(show_header=False, show_edge=False, padding=(0, 1))
    for index, column in enumerate(state.columns.available_columns, start=1):
        if state.columns.is_selected(column):
            table.add_row(f"[green][bold]{index})[/bold] {column}[/green]")
        else:
            table.add_row(f"[red][bold]{index})[/bold] {column}[/red]")
    return Panel(table, title=title, border_style="blue", expand=False)

def render_columns_menu(state: AppState, console):
    console.clear()

    console.print(create_all_columns_panel(state, title="Columns Menu"))
    console.print("[blue][bold]0)[/bold] Back to main menu[/blue]")




    
