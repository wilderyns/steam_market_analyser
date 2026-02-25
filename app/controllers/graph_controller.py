from app.models.appstate import AppState
from app.services.graph_service import (
    create_bar_graph,
    create_bar_graph_from_analysis,
    create_line_graph,
    create_line_graph_from_analysis,
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

        choice = expect_user_input(int, [0, 1, 2], None, None, console)

        if choice == 0:
            return

        try:
            source_choice = 1
            if state.last_analysis_columns is not None and state.last_analysis_rows is not None:
                source_choice = expect_user_input(
                    int,
                    [1, 2],
                    None,
                    None,
                    console,
                    "Graph source (1=dataset, 2=last analysis): "
                )

            x_column = console.input("X column: ").strip()
            y_column = console.input("Y column (numeric): ").strip()
            start_row = expect_user_input(int, None, 0, None, console, "Start row (0 for first): ")
            end_row = expect_user_input(int, None, 0, None, console, "End row (0 for last): ")
            filename = console.input("Output file name [.png optional]: ").strip()
            if not filename:
                filename = None

            if source_choice == 1:
                if choice == 1:
                    output_path, point_count = create_line_graph(state, x_column, y_column, start_row, end_row, filename)
                    console.print(f"[green]Line graph created with {point_count} points[/green]")
                    console.print(f"Saved to: [bold]{output_path}[/bold]")
                elif choice == 2:
                    output_path, point_count = create_bar_graph(state, x_column, y_column, start_row, end_row, filename)
                    console.print(f"[green]Bar graph created with {point_count} bars[/green]")
                    console.print(f"Saved to: [bold]{output_path}[/bold]")
            elif source_choice == 2:
                if choice == 1:
                    output_path, point_count = create_line_graph_from_analysis(state, x_column, y_column, start_row, end_row, filename)
                    console.print(f"[green]Line graph created from analysis with {point_count} points[/green]")
                    console.print(f"Saved to: [bold]{output_path}[/bold]")
                elif choice == 2:
                    output_path, point_count = create_bar_graph_from_analysis(state, x_column, y_column, start_row, end_row, filename)
                    console.print(f"[green]Bar graph created from analysis with {point_count} bars[/green]")
                    console.print(f"Saved to: [bold]{output_path}[/bold]")

            console.input("\nPress Enter to continue...")

        except Exception as e:
            error = str(e)
