# Menu display and logic functions

from rich import box
from .models import AppState, Filters
from .user_input import input_int, input_float, input_str
from rich.console import Console
from rich.table import Table

console = Console()

def show_main_menu():
    print("\n" + "=" * 30)
    print("Main Menu")
    print("=" * 30)
    print("1) TODO: View dataset records")
    print("2) TODO: Set / edit filters")
    print("3) TODO: View dataset")
    print("4) TODO: Analysis Toolkit")
    print("5) TODO: Export last results")
    print("99) Quit")
    
def view_dataset(df, n=20) -> None:
    cols = ["Name", "Release date", "Price", "Genres", "Tags", "Windows", "Mac", "Linux", "Positive", "Negative"]
    cols = [c for c in cols if c in df.columns]

    table = Table(
        title=f"First {n} rows (selected columns)",
        box=box.SQUARE,      # border style (try also box.HEAVY, box.ROUNDED, box.MINIMAL_HEAVY_HEAD)
        show_lines=True,     # <-- this draws a line between each row
        header_style="bold",
    )
    for c in cols:
        # You can justify/wrap certain columns if you want
        table.add_column(c, overflow="fold")

    for _, row in df[cols].head(n).iterrows():
        table.add_row(*[str(row[c]) if row[c] == row[c] else "" for c in cols])  # NaN-safe

    console.print(table)


def show_filters_menu(state: AppState) -> None:
    print("\n" + "=" * 30)
    print("Filters Menu")
    print("=" * 30)
    print(f"1) Year range: {state.filters.year_min} - {state.filters.year_max}")
    print(f"2) Price range: {state.filters.price_min} - {state.filters.price_max}")
    print(f"3) Genre contains: {state.filters.genre_contains}")
    print(f"4) Minimum review score: {state.filters.min_review_score}")
    print(f"5) Minimum reviews: {state.filters.min_reviews}")
    print("99) Clear all filters")
    print("0) Back to main menu")
    
    choice = input("Choice: ").strip()
    
    if choice == "0":
        return
    
    f = state.filters
    
    if choice == "1":
        f.year_min = input_int("Minimum year: ")
        f.year_max = input_int("Maximum year: ")
    elif choice == "2":
        f.price_min = input_float(input("Minimum price: "))
        f.price_max = input_float(input("Maximum price: "))
    elif choice == "3":
        f.genre_contains = input_str("Genre contains: ")
    elif choice == "4":
        f.min_review_score = input_float(input("Minimum review score: "))
    elif choice == "5":
        f.min_reviews = input_int("Minimum reviews: ")
    elif choice == "99":
        state.filters = Filters()
    else:
        print("Invalid choice.")