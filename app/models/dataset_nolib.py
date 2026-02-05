from app.models.dataset import Dataset, Row
from app.models.filters import Filters


class DatasetNoLib(Dataset):
    def __init__(self, columns: list[str], rows: list[Row]):
        self.columns = columns
        self.rows = rows

    def columns(self) -> list[str]:
        ...

    def row_count(self) -> int:
        ...

    def filter(self, filters: Filters) -> "DatasetNoLib":
        ...

    def get_page(self, page: int, page_size: int) -> list[Row]:
        ...