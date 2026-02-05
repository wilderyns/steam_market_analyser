"""
We use active filters across the application thus having core functions to format this display
makes sense.
"""

from rich.panel import Panel
from rich.console import Console
from ..models import AppState

def format_range(a, b) -> str:
    """
    format_range takes 2 values and formats them as a > b 

    :param a: range value 1
    :param b: range value 2
    :return: a string of a > b
    """ 
    if a is None and b is None:
        return "-"
    left = "-" if a is None else str(a)
    right = "-" if b is None else str(b)
    return f"{left} > {right}"

def active_filters_text(state: AppState) -> str:
    """
    active_filters_text

    :param state: the AppState to access the currently applied filters
    :return: a string joined filters ready for output on its own or to a panel
    """ 
    
    f = state.filters
    parts = []

    # Year
    if f.year_min is not None or f.year_max is not None:
        parts.append(f"[bold]Year[/bold]: {format_range(f.year_min, f.year_max)}")

    # Price
    if f.price_min is not None or f.price_max is not None:
        parts.append(f"[bold]Price[/bold]: {format_range(f.price_min, f.price_max)}")

    # Genre
    if f.genre_contains:
        parts.append(f"[bold]Genre[/bold]: contains '{f.genre_contains}'")

    # Reviews
    if f.min_review_score is not None:
        parts.append(f"[bold]Min score[/bold]: {f.min_review_score}")
    if f.min_reviews is not None:
        parts.append(f"[bold]Min reviews[/bold]: {f.min_reviews}")

    return " • ".join(parts) if parts else "None"

def print_active_filters_panel(console: Console, state: AppState) -> Console:
    """
    print_active_filters_panel

    :param console: the rich Console object
    :param state: the AppState to access the currently applied filters
    :return: a Console object, however function prints to the console regardless
    """ 
    return console.print(
            Panel(
                f"[bold]Active filters:[/bold] {active_filters_text(state)}",
                border_style="cyan",
                expand=False,
            )
        )