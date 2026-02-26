import string
from rich import box
from rich.console import Console
from rich.table import Table
from app.models.appstate import AppState
from app.views.rich.active_filters_panel import render_active_filters_panel_rich

# tags were getting in the way and making the dataset table really long
def compact_tags(value, keep: int = 3) -> str:
    text = "" if value is None else str(value).strip()
    if not text:
        return ""
    tags = [t.strip() for t in text.split(",") if t.strip()]
    if len(tags) <= keep:
        return ", ".join(tags)
    remaining = len(tags) - keep
    return f"{', '.join(tags[:keep])} ... ({remaining}+)"


def render_dataset_viewer_rich(state: AppState, console: Console, n: int = 20, p: int = 1, search_term: str = "") -> Table:
    console.clear()
    render_active_filters_panel_rich(state, console)

    dataset = state.last_results if state.last_results is not None else state.dataset
    if dataset is None:
        # To be fair we should never get here, we've already done the whole dataset verification and load, but more error handling is good
        
        table = Table(title="Dataset Viewer", box=box.SQUARE, show_lines=True, header_style="bold")
        table.add_column("Status")
        table.add_row("No dataset loaded")
        return table

    cols = state.columns.resolve()
    available_cols = state.columns.available_columns
    cols = [c for c in cols if c in available_cols]
    if not cols:
        # If no preferred columns are set just show the first 7 columns
        # Another thing that should never be reached because column setting
        # Is handled by the model
        cols = available_cols[:7]

    # Begin creating the table
    total_rows = dataset.row_count()
    total_pages = max(1, (total_rows + n - 1) // n)

    table = Table(
        title=f"Dataset Viewer | Page {p}/{total_pages} | Rows {total_rows}" + (f" | Search: {search_term}" if search_term else ""),
        box=box.SQUARE,      
        show_lines=True,  
        header_style="bold",
    )

    table.add_column("#", justify="right", no_wrap=True)
    
    # Special column formatting handling, overflows and the like
    # TODO: Handle all columns that might overflow
        
    for c in cols:
        if c == "Tags":
            table.add_column(c, overflow="ellipsis", no_wrap=True)
        if c == "About the game":
            table.add_column(c, overflow="ellipsis")
        else:
            table.add_column(c, overflow="fold")

    # Get n rows on page p 
    rows = dataset.get_page(p, n)
    
    # Give each column in the dataset a position 
    col_index = {name: index for index, name in enumerate(available_cols)}

    # run through the n rows in the currently selected page 
    start_row_number = (p - 1) * n + 1
    for row_offset, row in enumerate(rows):
        out = [str(start_row_number + row_offset)] #handy output buffer list
        for c in cols:
            index = col_index.get(c)
            # Set the cell value to an empty string if the value is missing or out of bounds, otherwise use th value
            val = "" if index is None or index >= len(row) else row[index]
            
            # Special rules for cells
            # compact the tags so the table doesn't have 10 lines of tags per rows
            if c == "Tags":
                out.append(compact_tags(val))
            # Remove all [ ] \ characters because these break Rich
            if c == "About the game":
                val = val.replace("[", "").replace("]", "").replace("\'", "")
                val = val[:50] + "..." if len(val) > n else val
                out.append(val)
            #Add currency symbol
            if c == "Price":
                val = "$"+val
                out.append(val)
            else:
                out.append("" if val is None else str(val))
                
        table.add_row(*out)

    return table


def render_analysis_viewer_rich(console: Console, columns: list[str], rows: list[list], p: int = 1, n: int = 20, search_term: str = "", title: str = "Analysis Viewer") -> Table:
    """
    Render analysis rows in a paged table
    
    Args:
        console (Console): Rich Console
        columns (list[str]): Column names for the analysis table
        rows (list[list]): Analysis rows
        p (int): Current page
        n (int): Rows per page
        search_term (str): Current search term
        title (str): Table title
        
    Returns:
        Table
    """
    console.clear()

    total_rows = len(rows)
    total_pages = max(1, (total_rows + n - 1) // n)
    start = max(0, (p - 1) * n)
    end = start + n

    table = Table(
        title=f"{title} | Page {p}/{total_pages} | Rows {total_rows}" + (f" | Search: {search_term}" if search_term else ""),
        box=box.SQUARE,
        show_lines=True,
        header_style="bold",
    )

    table.add_column("#", justify="right", no_wrap=True)
    for column in columns:
        table.add_column(column, overflow="fold")

    page_rows = rows[start:end]
    row_number = start + 1
    for row in page_rows:
        out = [str(row_number)]
        for value in row:
            out.append("" if value is None else str(value))
        table.add_row(*out)
        row_number += 1

    return table
