from rich.console import Console
from rich.panel import Panel
from app.models.appstate import AppState

def render_columns_menu(state: AppState, console):
    console.clear()
    
    lines = []
    for x, column in enumerate(state.columns.available_columns):
        if state.columns.is_selected(column):
            lines.append(f"[green][bold]{x+1})[/bold] {column}[/green]",)
        else:
            lines.append(f"[red][bold]{x+1})[/bold] {column}[/red]",)
    
    lines.append("")
    lines.append(f"[blue][bold]0)[/bold] Back to main menu[/blue]",)
    console.print(Panel("\n".join(lines), title="Columns Menu", border_style="blue", expand=False))




    