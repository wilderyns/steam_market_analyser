from rich.console import Console
from rich.panel import Panel

from app.models.appstate import AppState
from app.views.rich.active_filters_panel import render_active_filters_panel_rich


def render_export_menu_rich(state: AppState, console: Console, error: str | None = None) -> None:
    """
    Render export menu

    Args:
        state (AppState): application state controller
        console (Console): Rich Console
        error (str | None): Optional error message

    Returns:
        None
    """
    console.clear()
    render_active_filters_panel_rich(state, console)

    lines = [
        "[bold]1)[/bold] Export current dataset with active filters",
        "[bold]2)[/bold] Export current analysis",
        "",
        "[bold]0)[/bold] Back to main menu",
    ]

    if state.last_analysis_dataset is None:
        lines.append("[yellow]No analysis table available yet[/yellow]")
    else:
        lines.append("[green]Analysis table available for export[/green]")

    console.print(Panel("\n".join(lines), title="Export Menu", border_style="cyan", expand=True))

    if error:
        console.print(f"[red]{error}[/red]")
