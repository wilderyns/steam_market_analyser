from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from app.models.appstate import AppState
from app.views.rich.active_filters_panel import render_active_filters_panel_rich
from app.views.rich.columns_menu import create_all_columns_panel


def render_transform_root_rich(state: AppState, console: Console, error: str | None = None) -> None:
    console.clear()
    render_active_filters_panel_rich(state, console)

    status = "No"
    if state.transformations_applied:
        status = "Yes"

    lines = [
        f"[bold]Transformations applied:[/bold] {status}",
        "[bold]Note:[/bold] Transformations run on the filtered dataset",
        "[bold]Changing filters will undo active transformations[/bold]",
    ]

    if state.transform_filter_note:
        lines.append(f"[cyan]{state.transform_filter_note}[/cyan]")

    console.print(Panel("\n".join(lines), title="Transformation Context", border_style="cyan", expand=True))

    menu = Table(show_header=False, show_edge=False, padding=(0, 1))
    menu.add_row("[bold cyan]1)[/]", "Create count column from list/string column")
    menu.add_row("[bold cyan]2)[/]", "Create log1p column")
    menu.add_row("[bold cyan]3)[/]", "Create minmax scaled column")
    menu.add_row("[bold cyan]4)[/]", "Create zscore column")
    menu.add_row("[bold cyan]5)[/]", "Extract year column from date/text column")
    menu.add_row("[bold cyan]6)[/]", "Create sum column (x + y)")
    menu.add_row("[bold cyan]7)[/]", "Create ratio column x / (x + y)")
    menu.add_row("[bold cyan]8)[/]", "Create composite column (x + y) / z")
    menu.add_row("[bold magenta]9)[/]", "Descriptive statistics")
    menu.add_row("[bold magenta]10)[/]", "Grouped average summary")
    menu.add_row("[bold magenta]11)[/]", "Top N rows by numeric column")
    menu.add_row("[bold magenta]12)[/]", "String-list value ranking")
    menu.add_row("[bold yellow]13)[/]", "Clear active transformations")
    menu.add_row("[bold]0)[/]", "Back to main menu")

    transforms_panel = Panel(menu, title="Transformations and Analysis", border_style="green", expand=False)
    columns_panel = create_all_columns_panel(state, title="All Columns")
    console.print(Columns([transforms_panel, columns_panel], expand=True, equal=True))

    if error:
        console.print(f"[red]{error}[/red]")


def render_analysis_table_rich(console: Console, title: str, headers: list[str], rows: list[list], max_rows: int = 25) -> None:
    table = Table(title=title, show_lines=True)
    for header in headers:
        table.add_column(str(header), overflow="fold")

    shown = rows[:max_rows]
    for row in shown:
        table.add_row(*["" if value is None else str(value) for value in row])

    console.print(table)

    if len(rows) > max_rows:
        console.print(f"[yellow]Showing first {max_rows} rows out of {len(rows)}[/yellow]")
