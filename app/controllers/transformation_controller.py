from rich.console import Console

from app.models.appstate import AppState
from app.models.dataset_nolib import DatasetNoLib
from app.models.dataset_pandas import DatasetPandas
from app.services import transformation_service
from app.utils.user_input_handler import expect_user_input
from app.views.rich.transform_root import render_analysis_table_rich, render_transform_root_rich


def default_name(source: str, suffix: str) -> str:
    cleaned = source.lower().replace(" ", "_")
    return f"{cleaned}_{suffix}"


def prompt_column(console: Console, label: str) -> str:
    return console.input(f"{label}: ").strip()


def prompt_output_column(console: Console, default_name: str) -> str:
    value = console.input(f"Output column name [{default_name}]: ").strip()
    return value if value else default_name


def target_dataset(state: AppState):
    if state.transformations_applied and state.dataset is not None:
        return state.dataset
    if state.base_dataset is not None:
        return state.base_dataset
    return state.dataset


def resolve_overwrite(state: AppState, console: Console, column_name: str) -> bool:
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
    if active_dataset is not None and hasattr(active_dataset, "df"):
        import pandas
        dataframe = pandas.DataFrame(rows, columns=headers)
        state.last_analysis_dataset = DatasetPandas(dataframe)
    else:
        copied_rows = [list(row) for row in rows]
        state.last_analysis_dataset = DatasetNoLib(headers, copied_rows)


def transformation_controller(state: AppState, console: Console) -> None:
    if state.dataset is None and state.base_dataset is None:
        console.print("[red]Dataset not loaded[/red]")
        console.input("Press Enter to return...")
        return

    error = None

    while True:
        render_transform_root_rich(state, console, error)
        error = None

        choice = expect_user_input(int, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], None, None, console)

        if choice == 0:
            return

        try:
            if choice == 1:
                source = prompt_column(console, "Source column")
                seperator = console.input("Separator (required for strings): ").strip()
                default_col_name = default_name(source, "count")
                new_column = prompt_output_column(console, default_col_name)
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_count(state, source, seperator if seperator else None, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 2:
                source = prompt_column(console, "Source column")
                default_col_name = default_name(source, "log1p")
                new_column = prompt_output_column(console, default_col_name)
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_log(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 3:
                source = prompt_column(console, "Source column")
                default_col_name = default_name(source, "minmax")
                new_column = prompt_output_column(console, default_col_name)
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_minmax(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 4:
                source = prompt_column(console, "Source column")
                default_col_name = default_name(source, "zscore")
                new_column = prompt_output_column(console, default_col_name)
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.transform_create_zscore(state, source, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 5:
                column1 = prompt_column(console, "Column x")
                column2 = prompt_column(console, "Column y")
                new_column = prompt_output_column(console, default_name(column1, "plus") + "_" + column2.lower().replace(" ", "_"))
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.create_sum_column(state, column1, column2, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 6:
                column_x = prompt_column(console, "Column x")
                column_y = prompt_column(console, "Column y")
                new_column = prompt_output_column(console, default_name(column_x, "over_sum"))
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.create_ratio_of_sum(state, column_x, column_y, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 7:
                column_x = prompt_column(console, "Column x")
                column_y = prompt_column(console, "Column y")
                column_z = prompt_column(console, "Column z")
                new_column = prompt_output_column(console, default_name(column_x, "plus_" + column_y.lower().replace(" ", "_") + "_over_" + column_z.lower().replace(" ", "_")))
                overwrite = resolve_overwrite(state, console, new_column)
                transformation_service.create_composite_three_column(state, column_x, column_y, column_z, new_column, overwrite=overwrite)
                sync_state_columns(state)

            elif choice == 8:
                raw = console.input("Columns (comma separated): ").strip()
                columns = [item.strip() for item in raw.split(",") if item.strip()]
                headers, rows = transformation_service.descriptive_statistics(state, columns)
                store_analysis(state, "Descriptive Statistics", headers, rows)
                render_analysis_table_rich(console, "Descriptive Statistics", headers, rows)

            elif choice == 9:
                group_column = prompt_column(console, "Group by column")
                value_column = prompt_column(console, "Value column for average")
                headers, rows = transformation_service.grouped_average(state, group_column, value_column)
                store_analysis(state, "Grouped Average", headers, rows)
                render_analysis_table_rich(console, "Grouped Average", headers, rows)

            elif choice == 10:
                rank_column = prompt_column(console, "Rank by column")
                n = expect_user_input(int, None, 1, 200, console, "Top N rows: ")
                with console.status("[bold]Calculating Top N rows...[/bold]"):
                    headers, rows = transformation_service.top_n_rows(state, rank_column, n)
                selected_headers = [name for name in state.columns.resolve() if name in headers]
                if not selected_headers:
                    selected_headers = headers

                selected_indexes = [headers.index(name) for name in selected_headers]
                filtered_rows: list[list] = []
                for row in rows:
                    filtered_rows.append([row[i] if i < len(row) else "" for i in selected_indexes])

                store_analysis(state, "Top N Rows", selected_headers, filtered_rows)
                render_analysis_table_rich(console, "Top N Rows", selected_headers, filtered_rows)

            elif choice == 11:
                list_column = prompt_column(console, "String-list column")
                seperator = console.input("Separator [,]: ").strip()
                if not seperator:
                    seperator = ","
                top_n = expect_user_input(int, None, 1, 200, console, "Top N values: ")
                score_column = console.input("Optional score column (leave blank to skip): ").strip()
                headers, rows = transformation_service.string_list_value_ranking(state, list_column, seperator, top_n, score_column if score_column else None)
                store_analysis(state, "String-list Value Ranking", headers, rows)
                render_analysis_table_rich(console, "String-list Value Ranking", headers, rows)

            elif choice == 12:
                transformation_service.clear_transformations(state)
                sync_state_columns(state)
                console.print("[green]Transformations cleared and base dataset restored[/green]")

            console.input("\nPress Enter to continue...")

        except Exception as e:
            error = str(e)
