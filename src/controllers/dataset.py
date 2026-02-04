from rich.table import Table
from rich import box
import pandas 
from ..models import AppState

def get_dataset_view(state: AppState, n: int = 20):
    df = state.dataframe
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

    return table