"""
View for setting filters.
"""
from rich.console import Console
from rich.panel import Panel

from app.models.appstate import AppState

def format_range(a, b) -> str:
    if a is None and b is None:
        return "-"
    left = "-" if a is None else str(a)
    right = "-" if b is None else str(b)
    return f"{left} → {right}"

def assemble_active_filters_panel(state: AppState):
    f = state.filters
    parts = []

    # year
    if f.year_min is not None or f.year_max is not None:
        parts.append(f"[bold]Year[/bold]: {format_range(f.year_min, f.year_max)}")

    # price
    if f.price_min is not None or f.price_max is not None:
        parts.append(f"[bold]Price[/bold]: {format_range(f.price_min, f.price_max)}")

    # genre
    if f.genre_contains:
        parts.append(f"[bold]Genre[/bold]: contains '{f.genre_contains}'")

    # reviews
    if f.min_review_score is not None:
        parts.append(f"[bold]Min score[/bold]: {f.min_review_score}")
    if f.min_reviews is not None:
        parts.append(f"[bold]Min reviews[/bold]: {f.min_reviews}")

    # adult content 
    if f.show_adult_content is not None:
        parts.append(f"[bold]Adult content[/bold]: {f.show_adult_content}")
        
    return " : ".join(parts) if parts else "None"

def render_active_filters_panel_rich(state: AppState, console: Console=None):
    if console is not None:
        console.print(
            Panel(
                f"[bold]Active filters:[/bold] {assemble_active_filters_panel(state)}",
                border_style="cyan",
                expand=False,
            )
        )