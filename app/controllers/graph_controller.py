from app.models.appstate import AppState
from app.services.graph_service import (
    create_bar_graph,
    create_line_graph,
    create_pie_graph,
)
from app.utils.user_input_handler import expect_user_input
from app.views.rich.graph_menu import render_graph_menu_rich


def graph_controller(state: AppState, console=None):
    """
    Handles graph menu loop, offering user input and view display

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
        render_graph_menu_rich(state, console, error)
        error = None

        choice = expect_user_input(int, [0, 1, 2, 3], None, None, console)

        if choice == 0:
            return

        try:
            source_choice = 1
            if state.last_analysis_dataset is not None:
                source_choice = expect_user_input(
                    int,
                    [1, 2],
                    None,
                    None,
                    console,
                    "Graph source (1=dataset, 2=last analysis): "
                )

            x_column = expect_user_input(str, None, None, None, console, "X column: ")
            y_column = expect_user_input(str, None, None, None, console, "Y column (numeric): ")
            start_row = expect_user_input(int, None, 0, None, console, "Start row (0 for first): ")
            end_row = expect_user_input(int, None, 0, None, console, "End row (0 for last): ")
            filename = expect_user_input(str, None, None, None, console, "Output file name [.png optional]: ")
            if not filename:
                filename = None

            source = "dataset" if source_choice == 1 else "analysis"
            source_label = "from analysis " if source == "analysis" else ""

            if choice == 1:
                output_path, point_count = create_line_graph(state, x_column, y_column, start_row, end_row, filename, source=source)
                console.print(f"[green]Line graph created {source_label}with {point_count} points[/green]")
                console.print(f"Saved to: [bold]{output_path}[/bold]")
            elif choice == 2:
                show_values = expect_user_input(bool, None, None, None, console, "Show values on bars? (y/n): ")
                output_path, point_count = create_bar_graph(state, x_column, y_column, start_row, end_row, filename, show_values=show_values, source=source)
                console.print(f"[green]Bar graph created {source_label}with {point_count} bars[/green]")
                console.print(f"Saved to: [bold]{output_path}[/bold]")
            elif choice == 3:
                output_path, point_count = create_pie_graph(state, x_column, y_column, start_row, end_row, filename, source=source)
                console.print(f"[green]Pie graph created {source_label}with {point_count} slices[/green]")
                console.print(f"Saved to: [bold]{output_path}[/bold]")

            console.input("\nPress Enter to continue...")

        except Exception as e:
            error = str(e)
