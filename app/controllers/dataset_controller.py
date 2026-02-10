from rich.panel import Panel
from rich.table import Table
from rich import box
import pandas

from app.services.dataset_service import attempt_data_download, init_dataset 
from app.models.appstate import AppState

# Doing the view view logic here, should be broken into its own view 

def dataset_controller(state, console=None):
    if console is None or not hasattr(console, "size"):
        print("loading dataset")
        init_dataset(state)
    else:
        with console.status("[bold]Loading dataset...[/bold]"):
            try:
                init_dataset(state)
            except FileNotFoundError:
                df = None
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
                f"Records: [bold]{len(state.dataset)}[/bold]\n"
                f"Columns: [bold]{len(state.dataset.columns)}[/bold]",
                border_style="green"
            ))
            console.input("\nPress Enter to continue...")
            return

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
                state.dataframe = init_dataset(state)
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

        return True