from pathlib import Path
from datetime import datetime

from app.models.appstate import AppState


def get_pyplot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.ioff()
    return plt


def get_graph_dataset(state: AppState):
    """
    Return dataset to use for graph creation

    Args:
        state (AppState): application state controller

    Returns:
        Dataset
    """
    if state.dataset is None:
        raise RuntimeError("Dataset not loaded")

    if state.transformations_applied:
        return state.dataset

    return state.dataset.filter(state.filters)


def get_analysis_table(state: AppState) -> tuple[list[str], list[list]]:
    """
    Return last analysis table from state

    Args:
        state (AppState): application state controller

    Returns:
        tuple[list[str], list[list]]
    """
    if state.last_analysis_dataset is None:
        raise RuntimeError("No analysis table available. Run an analysis first.")
    columns = state.last_analysis_dataset.columns()
    rows = state.last_analysis_dataset.get_page(1, state.last_analysis_dataset.row_count())
    return columns, rows


def normalise_range(total_rows: int, start_row: int, end_row: int) -> tuple[int, int]:
    """
    Convert user row range input into safe Python slice positions

    Args:
        total_rows (int): Number of rows in source dataset
        start_row (int): Start row (1-based), use 0 for first row
        end_row (int): End row (1-based), use 0 for last row

    Returns:
        tuple[int, int]: (start_index, end_index_exclusive)
    """
    if total_rows <= 0:
        return 0, 0

    if start_row <= 0:
        start_index = 0
    else:
        start_index = start_row - 1

    if end_row <= 0:
        end_index = total_rows
    else:
        end_index = end_row

    if start_index < 0:
        start_index = 0
    if end_index > total_rows:
        end_index = total_rows
    if start_index >= end_index:
        raise ValueError("Invalid row range")

    return start_index, end_index


def create_output_path(filename: str | None) -> Path:
    """
    Build output path for graph image

    Args:
        filename (str | None): Optional output filename

    Returns:
        Path
    """
    graphs_dir = Path("graphs")
    graphs_dir.mkdir(parents=True, exist_ok=True)

    if filename is None or not filename.strip():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graph_{stamp}.png"

    if not filename.lower().endswith(".png"):
        filename = f"{filename}.png"

    return graphs_dir / filename


def build_graph_series(state: AppState, x_column: str, y_column: str, start_row: int, end_row: int, source: str = "dataset"):
    """
    Build x and y values for graphing

    Args:
        state (AppState): application state controller
        x_column (str): Column name to use on x axis
        y_column (str): Column name to use on y axis
        start_row (int): Start row (1-based), use 0 for first row
        end_row (int): End row (1-based), use 0 for last row

    Returns:
        tuple[list, list]: x_values, y_values
    """
    if source == "dataset":
        dataset = get_graph_dataset(state)
        rows = dataset.get_column_values([x_column, y_column])
        x_index = 0
        y_index = 1
    elif source == "analysis":
        headers, rows = get_analysis_table(state)
        if x_column not in headers or y_column not in headers:
            raise KeyError("Analysis column not found")
        x_index = headers.index(x_column)
        y_index = headers.index(y_column)
    else:
        raise ValueError("source must be 'dataset' or 'analysis'")

    start_index, end_index = normalise_range(len(rows), start_row, end_row)
    selected = rows[start_index:end_index]

    x_values: list = []
    y_values: list[float] = []

    for row in selected:
        if x_index >= len(row) or y_index >= len(row):
            continue

        x_value = row[x_index]
        y_value = row[y_index]

        try:
            y_number = float(y_value)
        except (TypeError, ValueError):
            continue

        x_values.append(x_value)
        y_values.append(y_number)

    if not y_values:
        raise ValueError("No numeric data found in selected range")

    return x_values, y_values


def plot_line_values(plt, x_values: list, y_values: list[float]) -> None:
    """
    Plot line values and handle string labels safely

    Args:
        plt: matplotlib pyplot module
        x_values (list): x axis values
        y_values (list[float]): y axis values

    Returns:
        None
    """
    numeric_x: list[float] = []
    all_numeric = True
    for value in x_values:
        try:
            numeric_x.append(float(value))
        except (TypeError, ValueError):
            all_numeric = False
            break

    if all_numeric:
        plt.plot(numeric_x, y_values, marker="o", linewidth=1.5)
        return

    positions = list(range(len(y_values)))
    labels = [str(value) for value in x_values]
    plt.plot(positions, y_values, marker="o", linewidth=1.5)
    plt.xticks(positions, labels, rotation=45, ha="right")


def create_line_graph(state: AppState, x_column: str, y_column: str, start_row: int, end_row: int, filename: str | None = None, source: str = "dataset"):
    """
    Create and save a line graph from selected columns

    Args:
        state (AppState): application state controller
        x_column (str): Column name to use on x axis
        y_column (str): Column name to use on y axis
        start_row (int): Start row (1-based), use 0 for first row
        end_row (int): End row (1-based), use 0 for last row
        filename (str | None): Optional output filename
        source (str): dataset or analysis

    Returns:
        tuple[Path, int]: output path and point count
    """
    if not state.features.has_matplotlib:
        raise RuntimeError("Matplotlib is required for graph creation")

    plt = get_pyplot()

    x_values, y_values = build_graph_series(state, x_column, y_column, start_row, end_row, source=source)
    output_path = create_output_path(filename)

    plt.figure(figsize=(10, 5))
    plot_line_values(plt, x_values, y_values)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} vs {x_column}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path, len(y_values)


def create_bar_graph(state: AppState, x_column: str, y_column: str, start_row: int, end_row: int, filename: str | None = None, show_values: bool = False, source: str = "dataset"):
    """
    Create and save a bar graph from selected columns

    Args:
        state (AppState): application state controller
        x_column (str): Column name to use on x axis
        y_column (str): Column name to use on y axis
        start_row (int): Start row (1-based), use 0 for first row
        end_row (int): End row (1-based), use 0 for last row
        filename (str | None): Optional output filename
        show_values (bool): Show numeric values above each bar
        source (str): dataset or analysis

    Returns:
        tuple[Path, int]: output path and bar count
    """
    if not state.features.has_matplotlib:
        raise RuntimeError("Matplotlib is required for graph creation")

    plt = get_pyplot()

    x_values, y_values = build_graph_series(state, x_column, y_column, start_row, end_row, source=source)
    output_path = create_output_path(filename)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(x_values, y_values)
    if show_values:
        for bar, value in zip(bars, y_values):
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_height()
            plt.text(x, y, str(round(value, 4)), ha="center", va="bottom", fontsize=8)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} by {x_column}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path, len(y_values)


def create_pie_graph(state: AppState, x_column: str, y_column: str, start_row: int, end_row: int, filename: str | None = None, source: str = "dataset"):
    """
    Create and save a pie graph from selected columns

    Args:
        state (AppState): application state controller
        x_column (str): Column name to use as labels
        y_column (str): Column name to use as values
        start_row (int): Start row (1-based), use 0 for first row
        end_row (int): End row (1-based), use 0 for last row
        filename (str | None): Optional output filename
        source (str): dataset or analysis

    Returns:
        tuple[Path, int]: output path and slice count
    """
    if not state.features.has_matplotlib:
        raise RuntimeError("Matplotlib is required for graph creation")

    plt = get_pyplot()

    x_values, y_values = build_graph_series(state, x_column, y_column, start_row, end_row, source=source)
    output_path = create_output_path(filename)

    labels = [str(value) for value in x_values]
    plt.figure(figsize=(8, 8))
    plt.pie(y_values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title(f"{y_column} share by {x_column}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path, len(y_values)
