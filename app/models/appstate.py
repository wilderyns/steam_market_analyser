from pathlib import Path
from typing import Optional

from app.models.dataset import Dataset
from app.models.features import Features
from app.models.filters import Filters
from app.models.selected_columns import SelectedColumns


class AppState:
    dataset_path: Path
    dataset_url: str = "https://www.kaggle.com/api/v1/datasets/download/fronkongames/steam-games-dataset"
    dataset: Optional[Dataset] = None
    columns: SelectedColumns = SelectedColumns()
    filters: Filters = Filters()
    last_results: Optional[Dataset] = None
    features: Features = Features()
    page = 1
    sug_term_width = 120
    sug_term_height = 40

    def reset_filters(self):
        self.filters = Filters()