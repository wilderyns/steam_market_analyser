from rich.panel import Panel

from app.services.dataset_service import attempt_data_download, init_dataset 
from app.models.appstate import AppState
from app.models.dataset_nolib import DatasetNoLib
from app.models.dataset_pandas import DatasetPandas
from app.utils.terminal import clear_terminal
from app.views.rich.dataset_viewer import render_dataset_viewer_rich

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


def apply_search(dataset: DatasetPandas | DatasetNoLib, search_term: str):
    """
    Dataset viewer search function
    #TODO: stop doing the actual search here, move that to our model, then use the pm Dataset
    
    Args:
        dataset (AppState): Our dataset
        search_term (string): the term to search
        
    Returns:
        DatasetPandas or DatasetNolib depending on the passed initial dataset
        #TODO: Again, move the search logic outta here so a generic dataset can be returned 
    """
    
    if not search_term:
        return dataset

    search_term = search_term.lower()

    # If our dataset is using Pandas
    if isinstance(dataset, DatasetPandas):
        dataframe = dataset.df
        
        # Very cool casting of our entire dataset as strings 
        text = dataframe.astype(str)
        
        # Again more cool pandas stuff, allowing you to apply a function to an entire dataset
        # And then pythons anonymous functions make for some very neat coding 
        matches = text.apply(lambda col: col.str.contains(search_term, case=False, na=False)).any(axis=1)
        return DatasetPandas(dataframe[matches])

    # As contrasted to our nolib dataset where we do a loop through the rows
    # TODO: Might be fun to do a time comparison here l
    if isinstance(dataset, DatasetNoLib):
        rows = []
        append_row = rows.append
        to_str = str
        for row in dataset.rows:
            for cell in row:
                if search_term in to_str(cell).lower():
                    append_row(row)
                    break
        return DatasetNoLib(dataset.columns(), rows)

    return dataset


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

    while True:
        clear_terminal(console)
        filtered = state.dataset.filter(state.filters)
        searched = apply_search(filtered, search_term)
        state.last_results = searched

        total_rows = searched.row_count()
        total_pages = max(1, (total_rows + page_size - 1) // page_size)
        if state.page > total_pages:
            state.page = total_pages
        if state.page < 1:
            state.page = 1

        table = render_dataset_viewer_rich(state, console, n=page_size, p=state.page, search_term=search_term)
        console.print(table)
        console.print("[bold]Commands:[/bold] n=next, p=prev, s=search, c=clear search, q=back")
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
        else:
            error = f"{cmd if cmd else 'That input'} is an invalid option"
