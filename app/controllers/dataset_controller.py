from rich.panel import Panel

from app.services.dataset_service import attempt_data_download, init_dataset 
from app.models.appstate import AppState
from app.models.dataset_nolib import DatasetNoLib
from app.models.dataset_pandas import DatasetPandas
from app.utils.terminal import clear_terminal
from app.views.rich.dataset_viewer import render_analysis_viewer_rich, render_dataset_viewer_rich

# Doing the view view logic here, should be broken into its own view 

def dataset_controller(state, console=None):
    """
    Handles app initilisation dataset loading 
    
    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console
        
    Returns:
        Can return None, however will return True if everything went okay or raise a SystemExist if it didn't
    """
    if console is None or not hasattr(console, "size"):
        print("loading dataset")
        init_dataset(state)
    else:
        with console.status("[bold]Loading dataset...[/bold]"):
            try:
                init_dataset(state)
            except Exception as e:
                console.print(Panel.fit(
                    f"[red]Error loading dataset:[/red]\n{e}",
                    border_style="red"
                ))
                console.input("\nPress Enter to exit...")
                raise SystemExit(1)

        if state.dataset is not None:
            console.print(Panel.fit(
                f"[green]Dataset loaded.[/green]\n"
                f"Records: [bold]{state.dataset.row_count()}[/bold]\n"
                f"Columns: [bold]{len(state.dataset.columns())}[/bold]",
                border_style="green"
            ))
            
            console.print(Panel.fit(
                f"[green]Selected the following default columns:[/green]\n"
                f"Selected: [bold]{state.columns.resolve() if state.dataset is not None else 0}[/bold]\n"
                f"[purple]Change selected columns from the main menu[/purple]\n",
                border_style="purple"
            ))
            console.input("\nPress Enter to continue...")
            return True

        # If dataset doesn't exist 
        if not state.features.has_requests:
            console.print(Panel.fit(
                "[yellow]Dataset file not found.[/yellow]\n\n"
                "Automatic download is unavailable because [bold]requests[/bold] is not installed.\n\n"
                f"Download manually from:\n{state.dataset_url}\n"
                "and place the CSV at:\n"
                f"{state.dataset_path}\n\n"
                "Or install requests:\n"
                "pip install requests",
                border_style="yellow"
            ))
            console.input("\nPress Enter to exit...")
            raise SystemExit(1)

        # Try fetching automatically
        console.print(Panel.fit(
            "[yellow]Dataset not found.[/yellow]\n"
            "Attempting automatic download...",
            border_style="yellow"
        ))

        with console.status("[bold]Downloading and extracting dataset...[/bold]"):
            try:
                attempt_data_download(state, dest_path=state.dataset_path)
            except Exception as e:
                console.print(Panel.fit(
                    "[red]Automatic download failed.[/red]\n\n"
                    f"{e}\n\n"
                    f"Manual download link:\n{state.dataset_url}\n\n"
                    "Place the CSV at:\n"
                    f"{state.dataset_path}",
                    border_style="red"
                ))
                console.input("\nPress Enter to exit...")
                raise SystemExit(1)

        # Load again after fetch
        with console.status("[bold]Loading downloaded dataset...[/bold]"):
            try:
                init_dataset(state)
            except Exception as e:
                console.print(Panel.fit(
                    f"[red]Downloaded dataset but failed to load CSV:[/red]\n{e}",
                    border_style="red"
                ))
                console.input("\nPress Enter to exit...")
                raise SystemExit(1)

        console.print(Panel.fit(
            f"[green]Dataset downloaded and loaded. Ready![/green]\n"
            f"Records: [bold]{state.dataset.row_count() if state.dataset is not None else 0}[/bold]\n"
            f"Columns: [bold]{len(state.dataset.columns()) if state.dataset is not None else 0}[/bold]",
            border_style="green"
        ))
        
        console.print(Panel.fit(
            f"[green]Selected the following default columns:[/green]\n"
            f"Selected: [bold]{state.columns.resolve() if state.dataset is not None else 0}[/bold]\n"
            f"[purple]Change selected columns from the main menu[/purple]\n",
            border_style="purple"
        ))
        console.input("\nPress Enter to continue...")

        return True

def view_dataset_controller(state: AppState, console, page_size: int = 20):
    """
    Handles dataset viewer menu loop, offering user input and view display
    
    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console
        page_size (int): How many rows to display per page
        
    Returns:
        None
    """
    if state.dataset is None:
        console.print("[red]Dataset not loaded.[/red]")
        console.input("Press Enter to return...")
        return

    search_term = ""
    state.page = 1
    error = None
    view_mode = "dataset"

    while True:
        clear_terminal(console)

        if view_mode == "dataset":
            if state.transformations_applied:
                filtered = state.dataset
            else:
                filtered = state.dataset.filter(state.filters)
            searched = filtered.search(search_term)
            state.last_results = searched

            total_rows = searched.row_count()
            total_pages = max(1, (total_rows + page_size - 1) // page_size)
            if state.page > total_pages:
                state.page = total_pages
            if state.page < 1:
                state.page = 1

            table = render_dataset_viewer_rich(state, console, n=page_size, p=state.page, search_term=search_term)
        else:
            if state.last_analysis_columns is None or state.last_analysis_rows is None:
                error = "No analysis available. Run an analysis in transformations first."
                view_mode = "dataset"
                continue

            analysis_rows = state.last_analysis_rows
            if search_term:
                searched_rows = []
                lowered = search_term.lower()
                for row in analysis_rows:
                    for cell in row:
                        if lowered in str(cell).lower():
                            searched_rows.append(row)
                            break
            else:
                searched_rows = analysis_rows

            total_rows = len(searched_rows)
            total_pages = max(1, (total_rows + page_size - 1) // page_size)
            if state.page > total_pages:
                state.page = total_pages
            if state.page < 1:
                state.page = 1

            title = state.last_analysis_title if state.last_analysis_title else "Analysis Viewer"
            table = render_analysis_viewer_rich(
                console,
                state.last_analysis_columns,
                searched_rows,
                p=state.page,
                n=page_size,
                search_term=search_term,
                title=title,
            )

        console.print(table)
        mode_text = "Dataset" if view_mode == "dataset" else "Last Analysis"
        console.print(f"[bold]Mode:[/bold] {mode_text}")
        console.print("[bold]Commands:[/bold] n=next, p=prev, s=search, c=clear search, t=toggle dataset/analysis, q=back")
        if error:
            console.print(f"[red]{error}[/red]")

        cmd = console.input("Select an option: ").strip()
        error = None

        if cmd == "q":
            return
        elif cmd == "n":
            if state.page < total_pages:
                state.page += 1
            else:
                error = "Already on last page"
        elif cmd == "p":
            if state.page > 1:
                state.page -= 1
            else:
                error = "Already on first page"
        elif cmd == "s":
            search_term = console.input("Search term: ").strip()
            state.page = 1
        elif cmd == "c":
            search_term = ""
            state.page = 1
        elif cmd == "t":
            if view_mode == "dataset":
                if state.last_analysis_columns is None or state.last_analysis_rows is None:
                    error = "No analysis available. Run one in transformations first."
                else:
                    view_mode = "analysis"
                    state.page = 1
                    search_term = ""
            else:
                view_mode = "dataset"
                state.page = 1
                search_term = ""
        else:
            error = f"{cmd if cmd else 'That input'} is an invalid option"
