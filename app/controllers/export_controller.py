from app.models.appstate import AppState
from app.services.export_service import export_current_analysis_csv, export_current_dataset_csv
from app.utils.user_input_handler import expect_user_input
from app.views.rich.export_menu import render_export_menu_rich


def export_controller(state: AppState, console=None):
    """
    Handles export menu loop, offering user input and view display

    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console

    Returns:
        None
    """
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")

    error = None

    while True:
        render_export_menu_rich(state, console, error)
        error = None

        choice = expect_user_input(int, [0, 1, 2], None, None, console)

        if choice == 0:
            return True

        try:
            filename = console.input("Output file name [.csv optional]: ").strip()
            if not filename:
                filename = None

            if choice == 1:
                with console.status("[bold]Exporting dataset...[/bold]"):
                    output_path, row_count, col_count = export_current_dataset_csv(state, filename)
                console.print(f"[green]Dataset exported[/green] ({row_count} rows, {col_count} columns)")
                console.print(f"Saved to: [bold]{output_path}[/bold]")

            elif choice == 2:
                with console.status("[bold]Exporting analysis...[/bold]"):
                    output_path, row_count, col_count = export_current_analysis_csv(state, filename)
                console.print(f"[green]Analysis exported[/green] ({row_count} rows, {col_count} columns)")
                console.print(f"Saved to: [bold]{output_path}[/bold]")

            console.input("\nPress Enter to continue...")

        except Exception as e:
            error = str(e)
