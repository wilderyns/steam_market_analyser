from rich.console import Console
from rich.panel import Panel
from app.models.appstate import AppState
from app.views.rich.dataset_viewer import Table


def render_transform_root_rich(state: AppState, console: Console) -> None:
    console.clear()

    console.clear()
    table = Table(show_header=False, show_edge=False, padding=(0, 1))
    for idx, op in enumerate(operations, start=1):
        table.add_row(f"[bold cyan]{idx}[/]", op)
    panel = Panel(
        table,
        title="[bold]Upcoming transformations[/bold]",
        border_style="cyan",
        expand=False,
    )
    console.print(panel)
    console.print("\nPress [bold green]Enter[/bold] to start, or press [bold red]Q[/bold] to cancel.")

    console.print(Panel("\n".join(lines), title="Filters Menu", border_style="cyan", expand=True))