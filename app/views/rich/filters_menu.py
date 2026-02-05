from rich.console import Console
from rich.panel import Panel
from app.models.appstate import AppState


def render_filters_menu_rich(console: Console, state: AppState) -> None:
    f = state.filters
    console.clear()

    lines = [
        f"[bold]1)[/bold] Year range: {f.year_min} - {f.year_max}",
        f"[bold]2)[/bold] Price range: {f.price_min} - {f.price_max}",
        f"[bold]3)[/bold] Genre contains: {f.genre_contains or '—'}",
        f"[bold]4)[/bold] Minimum review score: {f.min_review_score if f.min_review_score is not None else '—'}",
        f"[bold]5)[/bold] Minimum reviews: {f.min_reviews if f.min_reviews is not None else '—'}",
        "",
        "[bold red]99)[/bold red] Clear all filters",
        "[bold]0)[/bold] Back to main menu",
    ]

    console.print(Panel("\n".join(lines), title="Filters Menu", border_style="cyan", expand=False))