from pathlib import Path
from typing import Optional

from app.models.dataset import Dataset
from app.models.features import Features
from app.models.filters import Filters
from app.models.selected_columns import SelectedColumns


class AppState:
    """
    AppState holds crucial attributes used throughout the application

    Attributes:
    dataset_path (Path): Path to the csv dataset. Unset by default.
    dataset_url (str): URL to the dataset zip download. Default: "https://www.kaggle.com/api/v1/datasets/download/fronkongames/steam-games-dataset"
    dataset (DatasetPandas | DatasetNoLib | None): Active dataset instance. This will become a DatasetPandas or a DatasetNoLib (for standard library implementation)
    columns (SelectedColumns): Stores currently selected columns as well as all the availabale columns
    filters (Filters): Activated filter criteria for the dataset 
    last_results (DatasetPandas | DatasetNoLib | None): The most recent search result, type matched to the AppState dataset type
    features (Features): Libraries present, detected by features service at startup
    page (int): current page selected in the dataset viewer
    sug_term_width (int): Suggestd terminal width
    sug_term_height (int): Suggested terminal height
    """
    
    dataset_path: Path
    dataset_url: str = "https://www.kaggle.com/api/v1/datasets/download/fronkongames/steam-games-dataset"
    dataset: Optional[Dataset] = None
    base_dataset: Optional[Dataset] = None
    columns: SelectedColumns = SelectedColumns()
    filters: Filters = Filters()
    last_results: Optional[Dataset] = None
    features: Features = Features()
    transformations_applied: bool = False
    transform_filter_note: Optional[str] = None
    last_analysis_title: Optional[str] = None
    last_analysis_columns: Optional[list[str]] = None
    last_analysis_rows: Optional[list[list]] = None
    page = 1
    sug_term_width = 120
    sug_term_height = 40

    def reset_filters(self):
        self.filters = Filters()
