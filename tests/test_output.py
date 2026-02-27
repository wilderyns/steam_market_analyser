from pathlib import Path

import pytest

pandas = pytest.importorskip("pandas")

from app.models.appstate import AppState
from app.models.dataset_pandas import DatasetPandas
from app.services.dataset_service import load_pandas
from app.services import graph_service, transformation_service


def build_state_from_dataset() -> AppState:
    """
    Build app state using the dataset loaded with pandas

    Args:
        None

    Returns:
        AppState
    """
    repo_root = Path(__file__).resolve().parents[1]
    dataset_path = repo_root / "data" / "steam_market_data.csv"

    if not dataset_path.exists():
        pytest.skip(f"Dataset file not found at {dataset_path}")

    state = AppState()
    state.dataset = load_pandas(dataset_path)
    state.base_dataset = state.dataset
    state.last_results = state.dataset
    state.features.has_pandas = True
    state.features.has_numpy = True
    state.features.has_matplotlib = True
    state.columns.load_columns(state.dataset.columns())

    return state


def store_analysis_as_dataset(state: AppState, title: str, headers: list[str], rows: list[list]) -> None:
    """
    Store analysis rows into state as dataset object

    Args:
        state (AppState): application state controller
        title (str): analysis title
        headers (list[str]): analysis headers
        rows (list[list]): analysis rows

    Returns:
        None
    """
    state.last_analysis_title = title
    state.last_analysis_dataset = DatasetPandas(pandas.DataFrame(rows, columns=headers))


def test_output():
    """
    Create graphs using the dataset with functions called as the user would access them

    Args:
        None

    Returns:
        None
    """
    repo_root = Path(__file__).resolve().parents[1]
    graphs_dir = repo_root / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)

    state = build_state_from_dataset()

    # Build top 10 genres, then graph it as bars
    genre_headers, genre_rows = transformation_service.string_list_value_ranking(
        state,
        "Genres",
        ",",
        10,
        None,
    )
    store_analysis_as_dataset(state, "Top 10 Genres", genre_headers, genre_rows)

    bar_path, bar_count = graph_service.create_bar_graph(
        state,
        "Value",
        "Count",
        0,
        0,
        str(graphs_dir / "top_10_genres_bar"),
        source="analysis",
    )
    assert bar_count > 0
    assert bar_path.exists()

    # Top recommendations
    state.columns.clear()
    state.columns.toggle("Name")
    state.columns.toggle("Recommendations")

    top_headers, top_rows = transformation_service.top_n_rows_selected_columns(state, "Recommendations", 25)
    store_analysis_as_dataset(state, "Top Recommendations", top_headers, top_rows)

    line_path, line_count = graph_service.create_line_graph(
        state,
        "Name",
        "Recommendations",
        0,
        0,
        str(graphs_dir / "top_recommendations_line"),
        source="analysis",
    )
    assert line_count > 0
    assert line_path.exists()

    # Genre count split and show share as a slice of the pie (chart)
    genre_headers_pie, genre_rows_pie = transformation_service.string_list_value_ranking(
        state,
        "Genres",
        ",",
        20,
        None,
    )
    store_analysis_as_dataset(state, "Games per Genre", genre_headers_pie, genre_rows_pie)

    pie_path, pie_count = graph_service.create_pie_graph(
        state,
        "Value",
        "Count",
        0,
        0,
        str(graphs_dir / "games_per_genre_pie"),
        source="analysis",
    )
    assert pie_count > 0
    assert pie_path.exists()

    # Extract year from release date, rank year counts, then bar chart with labels
    transformation_service.transform_extract_year(state, "Release date", "Release Year", overwrite=True)
    year_headers, year_rows = transformation_service.string_list_value_ranking(state, "Release Year", ",", 200, None)
    store_analysis_as_dataset(state, "Games per Year", year_headers, year_rows)

    year_bar_path, year_bar_count = graph_service.create_bar_graph(
        state,
        "Value",
        "Count",
        0,
        0,
        str(graphs_dir / "games_per_year_bar"),
        show_values=True,
        source="analysis",
    )
    assert year_bar_count > 0
    assert year_bar_path.exists()
