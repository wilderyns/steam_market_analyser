from app.models.dataset import Dataset, Row
from app.models.filters import Filters


class DatasetPandas(Dataset):
    def __init__(self, df):
        self.df = df

    def columns(self) -> list[str]:
        ...

    def row_count(self) -> int:
        ...

    def filter(self, filters: Filters) -> "DatasetPandas":
        ...

    def get_page(self, page: int, page_size: int) -> list[Row]:
        ...