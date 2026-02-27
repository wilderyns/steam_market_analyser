import math
from app.models.dataset import Dataset, Row
from app.models.filters import Filters


class DatasetNoLib(Dataset):
    """
    DatasetNoLib stores the dataset CSV as 2 lists as in attrbutes below

    Attributes:
    _columns (list[str]): Column headers 
    rows (list[Row]): Dataset rows, where each row is a list of cell values aligned to _columns
    """
    
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

        if filters.show_adult_content is False:
            nsfw_tags = ["nudity", "adult only", "hentai", "erotic"]
            rows = [
                row for row in rows
                if not any(tag in str(cell(row, "Tags") or "").lower() for tag in nsfw_tags)
            ]
        
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

        return DatasetNoLib(self._columns, rows)

    def get_column_values(self, columns: list[str]) -> list[Row]:
        """
        Return row values for the requested columns.
        """
        column_positions: list[int] = []
        missing_columns: list[str] = []

        for column_name in columns:
            if column_name in self._columns:
                column_positions.append(self._columns.index(column_name))
            else:
                missing_columns.append(column_name)

        if missing_columns:
            raise KeyError(f"Columns not found: {missing_columns}")

        selected_rows: list[Row] = []
        for row in self.rows:
            selected_row: Row = []
            for position in column_positions:
                selected_row.append(row[position])
            selected_rows.append(selected_row)

        return selected_rows

    def column_exists(self, column_name: str) -> bool:
        """
        Check if a column exists in the dataset
        
        Args:
            column_name (str): Name of column to check
            
        Returns:
            bool
        """
        return column_name in self._columns

    def transform_create_count(self, new_column_name: str, source_column: str, seperator: str | None, overwrite: bool = False) -> None:
        """
        Create a count column from a source column
        
        Args:
            new_column_name (str): Name of new column to create
            source_column (str): Column to read values from
            seperator (str | None): Seperator to split string values by
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if source_column not in self._columns:
            raise KeyError(f"Missing column: {source_column}")

        source_index = self._columns.index(source_column)

        counts: list[int] = []
        for row in self.rows:
            value = row[source_index]
            if isinstance(value, list):
                counts.append(len(value))
            elif isinstance(value, str):
                if seperator is None:
                    raise ValueError("seperator is required for string values")
                parts = value.split(seperator)
                non_empty_parts = []
                for part in parts:
                    if part.strip():
                        non_empty_parts.append(part)
                counts.append(len(non_empty_parts))
            elif value is None:
                counts.append(0)
            else:
                counts.append(0)

        self.create_new_column(new_column_name, counts, overwrite=overwrite)

    def transform_column_combine(self, column1: str, column2: str, new_column: str, overwrite: bool = False) -> None:
        """
        Create a new column by adding two numeric columns
        
        Args:
            column1 (str): First source column
            column2 (str): Second source column
            new_column (str): New column name
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if column1 not in self._columns or column2 not in self._columns:
            raise KeyError(f"Missing column: {column1} or {column2}")

        left_index = self._columns.index(column1)
        right_index = self._columns.index(column2)
        combined_values: list[float] = []

        for row in self.rows:
            left = self._to_float(row[left_index])
            right = self._to_float(row[right_index])
            combined_values.append(left + right)

        self.create_new_column(new_column, combined_values, overwrite=overwrite)

    def transform_create_log(self, logcolumn: str, newcolumn: str, overwrite: bool = False) -> None:
        """
        Create a log scaled column from a source column
        
        Args:
            logcolumn (str): Source column name
            newcolumn (str): New column name
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if logcolumn not in self._columns:
            raise KeyError(f"Missing column: {logcolumn}")

        source_index = self._columns.index(logcolumn)
        output_values: list[float] = []

        for row in self.rows:
            value = self._to_float(row[source_index])
            if value < 0:
                value = 0.0
            output_values.append(math.log1p(value))

        self.create_new_column(newcolumn, output_values, overwrite=overwrite)

    def transform_create_minmax(self, mmcolumn: str, newcolumn: str, overwrite: bool = False) -> None:
        """
        Create a min max scaled column from a source column
        
        Args:
            mmcolumn (str): Source column name
            newcolumn (str): New column name
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if mmcolumn not in self._columns:
            raise KeyError(f"Missing column: {mmcolumn}")

        source_index = self._columns.index(mmcolumn)
        numbers: list[float] = []
        for row in self.rows:
            numbers.append(self._to_float(row[source_index]))

        if not numbers:
            self.create_new_column(newcolumn, [], overwrite=overwrite)
            return

        min_value = min(numbers)
        max_value = max(numbers)

        if min_value == max_value:
            self.create_new_column(newcolumn, [0.0] * len(numbers), overwrite=overwrite)
            return

        scaled_values: list[float] = []
        for value in numbers:
            scaled_values.append((value - min_value) / (max_value - min_value))

        self.create_new_column(newcolumn, scaled_values, overwrite=overwrite)

    def transform_create_zscore(self, scorecolumn: str, newcolumn: str, overwrite: bool = False) -> None:
        """
        Create a zscore column from a source column
        
        Args:
            scorecolumn (str): Source column name
            newcolumn (str): New column name
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if scorecolumn not in self._columns:
            raise KeyError(f"Missing column: {scorecolumn}")

        source_index = self._columns.index(scorecolumn)
        numbers: list[float] = []
        for row in self.rows:
            numbers.append(self._to_float(row[source_index]))

        if not numbers:
            self.create_new_column(newcolumn, [], overwrite=overwrite)
            return

        mean_value = sum(numbers) / len(numbers)

        variance_total = 0.0
        for value in numbers:
            variance_total += (value - mean_value) ** 2
        std_value = (variance_total / len(numbers)) ** 0.5

        if std_value == 0:
            self.create_new_column(newcolumn, [0.0] * len(numbers), overwrite=overwrite)
            return

        zscores: list[float] = []
        for value in numbers:
            zscores.append((value - mean_value) / std_value)

        self.create_new_column(newcolumn, zscores, overwrite=overwrite)

    def transform_extract_year(self, source_column: str, new_column: str, overwrite: bool = False) -> None:
        """
        Extract a 4-digit year from a source column into a new column
        
        Args:
            source_column (str): Source column name
            new_column (str): New column name
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if source_column not in self._columns:
            raise KeyError(f"Missing column: {source_column}")

        source_index = self._columns.index(source_column)
        years: list[str] = []

        for row in self.rows:
            value = str(row[source_index]) if row[source_index] is not None else ""
            year = ""
            for part in value.replace(",", " ").split():
                if len(part) == 4 and part.isdigit():
                    year = part
                    break
            years.append(year)

        self.create_new_column(new_column, years, overwrite=overwrite)

    def create_new_column(self, column_name: str, rows: list, overwrite: bool = False) -> None:
        """
        Create a new column from provided row values
        
        Args:
            column_name (str): New column name
            rows (list): Values for each row
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        if len(rows) != len(self.rows):
            raise ValueError(f"Expected {len(self.rows)} values for new column '{column_name}'")

        if self.column_exists(column_name) and not overwrite:
            raise ValueError(f"Column already exists: {column_name}")

        if self.column_exists(column_name):
            column_index = self._columns.index(column_name)
            for row_index, row in enumerate(self.rows):
                row[column_index] = rows[row_index]
            return

        self._columns.append(column_name)
        for row_index, row in enumerate(self.rows):
            row.append(rows[row_index])

    def _to_float(self, value) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def search(self, search_term: str) -> DatasetNoLib:
        """
        Dataset viewer search function
        #TODO: test
        
        Args:
            search_term (string): the term to search
            
        Returns:
            Dataset
        """
        
        rows = []
        append_row = rows.append
        to_str = str
        for row in self.rows:
            for cell in row:
                if search_term in to_str(cell).lower():
                    append_row(row)
                    break
                
        return DatasetNoLib(self.columns(), rows)
