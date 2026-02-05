from typing import TypeAlias
from app.models.filters import Filters

Cell: TypeAlias = str | int | float | bool
Row: TypeAlias = list[Cell]

class Dataset:
    def columns(self) -> list[str]:
        raise NotImplementedError

    def row_count(self) -> int:
        raise NotImplementedError

    def filter(self, filters: Filters) -> Dataset:
        raise NotImplementedError
    
    def get_page(self, page: int, page_size: int) -> list[Row]:
        raise NotImplementedError