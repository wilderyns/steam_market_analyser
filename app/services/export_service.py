import csv
from datetime import datetime
from pathlib import Path

from app.models.appstate import AppState
from app.models.dataset import Dataset


def create_export_path(filename: str | None) -> Path:
    """
    Build output path for csv export

    Args:
        filename (str | None): Optional output filename

    Returns:
        Path
    """
    export_dir = Path("exports")
    export_dir.mkdir(parents=True, exist_ok=True)

    if filename is None or not filename.strip():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{stamp}.csv"

    if not filename.lower().endswith(".csv"):
        filename = f"{filename}.csv"

    return export_dir / filename


def resolve_dataset_for_export(state: AppState) -> Dataset:
    """
    Resolve current dataset view for export

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


def resolve_selected_columns(state: AppState, dataset: Dataset) -> list[str]:
    """
    Resolve export columns from selected columns model

    Args:
        state (AppState): application state controller
        dataset (Dataset): dataset being exported

    Returns:
        list[str]
    """
    selected = state.columns.resolve()
    available = dataset.columns()
    columns = [name for name in selected if name in available]

    if not columns:
        columns = available

    return columns


def write_dataset_csv(dataset: Dataset, columns: list[str], output_path: Path) -> int:
    """
    Write dataset rows to csv file

    Args:
        dataset (Dataset): dataset to export
        columns (list[str]): columns to include
        output_path (Path): output path

    Returns:
        int: number of exported rows
    """
    rows = dataset.get_column_values(columns)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)

    return len(rows)


def export_current_dataset_csv(state: AppState, filename: str | None = None) -> tuple[Path, int, int]:
    """
    Export current dataset view to csv

    Args:
        state (AppState): application state controller
        filename (str | None): Optional output filename

    Returns:
        tuple[Path, int, int]: output path, row count, column count
    """
    dataset = resolve_dataset_for_export(state)
    columns = resolve_selected_columns(state, dataset)
    output_path = create_export_path(filename)
    row_count = write_dataset_csv(dataset, columns, output_path)
    return output_path, row_count, len(columns)


def export_current_analysis_csv(state: AppState, filename: str | None = None) -> tuple[Path, int, int]:
    """
    Export last analysis dataset to csv

    Args:
        state (AppState): application state controller
        filename (str | None): Optional output filename

    Returns:
        tuple[Path, int, int]: output path, row count, column count
    """
    if state.last_analysis_dataset is None:
        raise RuntimeError("No analysis dataset available")

    dataset = state.last_analysis_dataset
    columns = dataset.columns()
    output_path = create_export_path(filename)
    row_count = write_dataset_csv(dataset, columns, output_path)
    return output_path, row_count, len(columns)
