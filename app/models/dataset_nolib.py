from app.models.dataset import Dataset, Row
from app.models.filters import Filters


class DatasetNoLib(Dataset):
    def __init__(self, columns: list[str], rows: list[Row]):
        self._columns = columns
        self.rows = rows

    def columns(self) -> list[str]:
        return self._columns

    def row_count(self) -> int:
        return len(self.rows)

    def filter(self, filters: Filters) -> "DatasetNoLib":
        rows = self.rows
        col_map = {name: idx for idx, name in enumerate(self._columns)}

        def cell(row: Row, *names: str):
            for name in names:
                if name in col_map:
                    return row[col_map[name]]
            return None

        # each filter has a function which is defined when the corresponding filter is set
        # these function is responisble for type checking and seeing if the row arg passed to it
        # meets the filter it's defined for
        # then work through each filter (if set) looping through the rows and gradually cutting them down
        
        if filters.year_min is not None or filters.year_max is not None:
            def year_ok(row: Row) -> bool:
                value = cell(row, "Release date")
                if value is None:
                    return True
                year = int(str(value)[-4:]) if str(value)[-4:].isdigit() else None
                if year is None:
                    return False
                if filters.year_min is not None and year < filters.year_min:
                    return False
                if filters.year_max is not None and year > filters.year_max:
                    return False
                return True
            rows = [row for row in rows if year_ok(row)]

        if filters.price_min is not None or filters.price_max is not None:
            def price_ok(row: Row) -> bool:
                value = cell(row, "Price")
                if value is None:
                    return True
                try:
                    price = float(value)
                except (TypeError, ValueError):
                    return False
                if filters.price_min is not None and price < filters.price_min:
                    return False
                if filters.price_max is not None and price > filters.price_max:
                    return False
                return True
            rows = [row for row in rows if price_ok(row)]

        if filters.genre_contains:
            search_term = filters.genre_contains.lower()
            rows = [
                row for row in rows
                if search_term in str(cell(row, "Genres", "Tags") or "").lower()
            ]

        if filters.min_review_score is not None:
            def score_ok(row: Row) -> bool:
                value = cell(row, "User score", "Review score")
                if value is None:
                    return True
                try:
                    return float(value) >= filters.min_review_score
                except (TypeError, ValueError):
                    return False
            rows = [row for row in rows if score_ok(row)]

        if filters.min_reviews is not None:
            def reviews_ok(row: Row) -> bool:
                value = cell(row, "Recommendations", "Positive")
                if value is None:
                    return True
                try:
                    return int(float(value)) >= filters.min_reviews
                except (TypeError, ValueError):
                    return False
            rows = [row for row in rows if reviews_ok(row)]

        if filters.adult_content is not None:
            def adult_ok(row: Row) -> bool:
                value = cell(row, "Required age")
                if value is None:
                    return True
                if filters.adult_content is not None and value < 18:
                    return False
                if filters.adult_content is not None and value >= 18:
                    return False
                return True
                
                    
        return DatasetNoLib(self._columns, rows)

    def get_page(self, page: int, page_size: int) -> list[Row]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 1
        start = (page - 1) * page_size
        end = start + page_size
        return self.rows[start:end]
