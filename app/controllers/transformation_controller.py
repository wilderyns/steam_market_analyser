from rich.console import Console

from app.models.appstate import AppState
from app.services.dataset_service import factory_create_dataset
from app.services import transformation_service
from app.utils.user_input_handler import expect_user_input
from app.views.rich.transform_root import render_analysis_table_rich, render_transform_root_rich


def target_dataset(state: AppState):
    """
    Determine what dataset to apply transformations to

    Args:
        state (AppState): application state controller

    Returns:
        Dataset
    """
    if state.transformations_applied and state.dataset is not None:
        return state.dataset
    if state.base_dataset is not None:
        return state.base_dataset
    return state.dataset


def resolve_overwrite(state: AppState, console: Console, column_name: str) -> bool:
    """
    Determine if the user selected column name exists and if so prompt to overwrite

    Args:
        state (AppState): application state controller
        console (Console): Rich console
       column_name (str): The column name to be created

    Returns:
        Bool: True if user has selected to overwrite, otherwise false
    """
    dataset = target_dataset(state)
    if dataset is None:
        return False
    if not dataset.column_exists(column_name):
        return False

    console.print(f"[yellow]Column '{column_name}' already exists[/yellow]")
    return expect_user_input(bool, None, None, None, console, "Overwrite it? (y/n): ")


def sync_state_columns(state: AppState) -> None:
    if state.dataset is None:
        return
    state.columns.available_columns = state.dataset.columns()


def store_analysis(state: AppState, title: str, headers: list[str], rows: list[list]) -> None:
    """
    Store analysis output in app state

    Args:
        state (AppState): application state controller
        title (str): Analysis output title
        headers (list[str]): Output headers
        rows (list[list]): Output rows

    Returns:
        None
    """
    state.last_analysis_title = title
    active_dataset = state.dataset if state.dataset is not None else state.base_dataset
    backend = "pandas" if state.features.has_pandas else "nolib"
    state.last_analysis_dataset = factory_create_dataset(state, rows, headers, backend=backend)


def transformation_controller(state: AppState, console: Console) -> None:
    if state.dataset is None and state.base_dataset is None:
        console.print("[red]Dataset not loaded[/red]")
        console.input("Press Enter to return...")
        return

    error = None

    while True:
        render_transform_root_rich(state, console, error)
        error = None

        choice = expect_user_input(int, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], None, None, console)

        if choice == 0:
            return

        try:
            if choice == 1:
                source = expect_user_input(str, None, None, None, console, "Source column: ")
                seperator = console.input("Separator (required for strings): ").strip()
                default_col_name = f"{source.lower().replace(' ', '_')}_count"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_count(state, source, seperator if seperator else None, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 2:
                source = expect_user_input(str, None, None, None, console, "Source column: ")
                default_col_name = f"{source.lower().replace(' ', '_')}_log1p"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_log(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 3:
                source = expect_user_input(str, None, None, None, console, "Source column: ")
                default_col_name = f"{source.lower().replace(' ', '_')}_minmax"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_minmax(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 4:
                source = expect_user_input(str, None, None, None, console, "Source column: ")
                default_col_name = f"{source.lower().replace(' ', '_')}_zscore"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_zscore(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 5:
                source = expect_user_input(str, None, None, None, console, "Source column: ")
                default_col_name = f"{source.lower().replace(' ', '_')}_year"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_extract_year(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 6:
                column1 = expect_user_input(str, None, None, None, console, "Column x: ")
                column2 = expect_user_input(str, None, None, None, console, "Column y: ")
                default_col_name = f"{column1.lower().replace(' ', '_')}_plus_{column2.lower().replace(' ', '_')}"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.create_sum_column(state, column1, column2, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 7:
                column_x = expect_user_input(str, None, None, None, console, "Column x: ")
                column_y = expect_user_input(str, None, None, None, console, "Column y: ")
                default_col_name = f"{column_x.lower().replace(' ', '_')}_over_sum"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.create_ratio_of_sum(state, column_x, column_y, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 8:
                column_x = expect_user_input(str, None, None, None, console, "Column x: ")
                column_y = expect_user_input(str, None, None, None, console, "Column y: ")
                column_z = expect_user_input(str, None, None, None, console, "Column z: ")
                default_col_name = f"{column_x.lower().replace(' ', '_')}_plus_{column_y.lower().replace(' ', '_')}_over_{column_z.lower().replace(' ', '_')}"
                new_column = expect_user_input(str, None, None, None, console, f"Output column name [{default_col_name}]: ") or default_col_name
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.create_composite_three_column(state, column_x, column_y, column_z, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 9:
                raw = console.input("Columns (comma separated): ").strip()
                columns = [item.strip() for item in raw.split(",") if item.strip()]
                headers, rows = transformation_service.descriptive_statistics(state, columns)
                store_analysis(state, "Descriptive Statistics", headers, rows)
                render_analysis_table_rich(console, "Descriptive Statistics", headers, rows)

            elif choice == 10:
                group_column = expect_user_input(str, None, None, None, console, "Group by column: ")
                value_column = expect_user_input(str, None, None, None, console, "Value column for average: ")
                seperator = console.input("Optional split separator (leave blank for no split): ").strip()
                headers, rows = transformation_service.grouped_average(
                    state,
                    group_column,
                    value_column,
                    seperator if seperator else None,
                )
                store_analysis(state, "Grouped Average", headers, rows)
                render_analysis_table_rich(console, "Grouped Average", headers, rows)

            elif choice == 11:
                rank_column = expect_user_input(str, None, None, None, console, "Rank by column: ")
                n = expect_user_input(int, None, 1, 200, console, "Top N rows: ")
                with console.status("[bold]Calculating Top N rows...[/bold]"):
                    headers, rows = transformation_service.top_n_rows_selected_columns(state, rank_column, n)
                store_analysis(state, "Top N Rows", headers, rows)
                render_analysis_table_rich(console, "Top N Rows", headers, rows)

            elif choice == 12:
                list_column = expect_user_input(str, None, None, None, console, "String-list column: ")
                seperator = console.input("Separator [,]: ").strip()
                if not seperator:
                    seperator = ","
                top_n = expect_user_input(int, None, 1, 200, console, "Top N values: ")
                score_column = console.input("Optional score column (leave blank to skip): ").strip()
                headers, rows = transformation_service.string_list_value_ranking(state, list_column, seperator, top_n, score_column if score_column else None)
                store_analysis(state, "String-list Value Ranking", headers, rows)
                render_analysis_table_rich(console, "String-list Value Ranking", headers, rows)

            elif choice == 13:
                transformation_service.clear_transformations(state)
                sync_state_columns(state)
                console.print("[green]Transformations cleared and base dataset restored[/green]")

            console.input("\nPress Enter to continue...")

        except Exception as e:
            error = str(e)
