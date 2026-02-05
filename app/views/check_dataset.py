"""
Initial loading screen for checking dataset presence and fetching if needed.
"""

from rich.console import Console
from rich.panel import Panel

from ..models import AppState
from ..loader import load_dataset, fetch_dataset

dataset_url = "https://www.kaggle.com/fronkongames/steam-games-dataset"

def check_dataset_view(console: Console, state: AppState) -> None:
    console.clear()

    console.print(Panel.fit(
        "[bold]Dataset check[/bold]\n"
        f"Path: {state.dataset_path}",
        border_style="cyan"
    ))

    # Tru to load existign dataset 
    with console.status("[bold]Loading dataset...[/bold]"):
        try:
            df = load_dataset(state.dataset_path)
            state.dataframe = df
        except FileNotFoundError:
            df = None
        except Exception as e:
            console.print(Panel.fit(
                f"[red]Error loading dataset:[/red]\n{e}",
                border_style="red"
            ))
            console.input("\nPress Enter to exit...")
            raise SystemExit(1)

    if state.dataframe is not None:
        console.print(Panel.fit(
            f"[green]Dataset loaded.[/green]\n"
            f"Records: [bold]{len(state.dataframe)}[/bold]\n"
            f"Columns: [bold]{len(state.dataframe.columns)}[/bold]",
            border_style="green"
        ))
        console.input("\nPress Enter to continue...")
        return

    # If dataset doesn't exist 
    if not state.features.has_requests:
        console.print(Panel.fit(
            "[yellow]Dataset file not found.[/yellow]\n\n"
            "Automatic download is unavailable because [bold]requests[/bold] is not installed.\n\n"
            f"Download manually from:\n{dataset_url}\n"
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
            fetch_dataset(state, dest_path=state.dataset_path)
        except Exception as e:
            console.print(Panel.fit(
                "[red]Automatic download failed.[/red]\n\n"
                f"{e}\n\n"
                f"Manual download link:\n{dataset_url}\n\n"
                "Place the CSV at:\n"
                f"{state.dataset_path}",
                border_style="red"
            ))
            console.input("\nPress Enter to exit...")
            raise SystemExit(1)

    # Load again after fetch
    with console.status("[bold]Loading downloaded dataset...[/bold]"):
        try:
            state.dataframe = load_dataset(state.dataset_path)
        except Exception as e:
            console.print(Panel.fit(
                f"[red]Downloaded dataset but failed to load CSV:[/red]\n{e}",
                border_style="red"
            ))
            console.input("\nPress Enter to exit...")
            raise SystemExit(1)

    console.print(Panel.fit(
        f"[green]Dataset downloaded and loaded. Ready![/green]\n"
        f"Records: [bold]{len(state.dataframe)}[/bold]\n"
        f"Columns: [bold]{len(state.dataframe.columns)}[/bold]",
        border_style="green"
    ))
    console.input("\nPress Enter to continue...")
