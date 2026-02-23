from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.models.appstate import AppState
from app.views.rich.active_filters_panel import render_active_filters_panel_rich


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
    menu.add_row("[bold cyan]5)[/]", "Create sum column (x + y)")
    menu.add_row("[bold cyan]6)[/]", "Create ratio column x / (x + y)")
    menu.add_row("[bold cyan]7)[/]", "Create composite column (x + y) / z")
    menu.add_row("[bold magenta]8)[/]", "Descriptive statistics (view only)")
    menu.add_row("[bold magenta]9)[/]", "Grouped average summary (view only)")
    menu.add_row("[bold magenta]10)[/]", "Top N rows by numeric column (view only)")
    menu.add_row("[bold magenta]11)[/]", "String-list value ranking (view only)")
    menu.add_row("[bold yellow]12)[/]", "Clear active transformations")
    menu.add_row("[bold]0)[/]", "Back to main menu")

    console.print(Panel(menu, title="Transformations and Analysis", border_style="green", expand=False))

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
