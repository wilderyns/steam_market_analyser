from rich import box
from rich.console import Console
from rich.table import Table
from app.models.appstate import AppState


def render_dataset_viewer_rich(state: AppState, console: Console, n: int = 20, p: int = 1) -> Table:
    console.clear()
    
    df = state.dataframe
    cols = ["Name", "Release date", "Price", "Genres", "Tags", "Windows", "Mac", "Linux", "Positive", "Negative"]
    cols = [c for c in cols if c in df.columns]

    table = Table(
        title=f"First {n} rows (selected columns)",
        box=box.SQUARE,      
        show_lines=True,  
        header_style="bold",
    )
    for c in cols:
        table.add_column(c, overflow="fold")

    start = p * n
    end = start + n
    df_subset = df[cols].iloc[start:end]

    for _, row in df_subset.iterrows():
        table.add_row(*[str(row[c]) if row[c] == row[c] else "" for c in cols]) 

    return table