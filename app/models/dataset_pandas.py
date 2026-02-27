from app.models.dataset import Dataset, Row
from app.models.filters import Filters

try:
    import pandas
except ImportError:
    pandas = None


class DatasetPandas(Dataset):
    """
    DatasetPandas stores our CSV using a pandas dataframe backend 

    Attributes:
    df (pandas.DataFrame): Dataframe containing all dataset columns and rows
    """
    
    def __init__(self, df):
        self.df = df

    def columns(self) -> list[str]:
        return [str(c) for c in self.df.columns.tolist()]

    def row_count(self) -> int:
        return int(len(self.df))

    def filter(self, filters: Filters) -> "DatasetPandas":
        import pandas

        dataframe = self.df

        # All these filter conditions essentially do the same thing 
        # check if the filter is set
        # loop through the relevant columns 
        # type check the values in each cell and then alter the dataframe to accomodate 
        # move on to next filter 
        
        if filters.show_adult_content is False:
            nsfw_tags = ["nudity", "adult only", "hentai", "erotic"]
            nsfw_pattern = "|".join(nsfw_tags)
            for col in ("Tags",):
                if col in dataframe.columns:
                    has_nsfw_tag = dataframe[col].astype(str).str.contains(nsfw_pattern, case=False, na=False)
                    dataframe = dataframe[has_nsfw_tag == False]
                    break
        
        if filters.year_min is not None or filters.year_max is not None:
            for col in ("Release date"):
                if col in dataframe.columns:
                    years = dataframe[col].astype(str).str.extract(r"(\d{4})", expand=False)
                    years = pandas.to_numeric(years, errors="coerce")
                    if filters.year_min is not None:
                        dataframe = dataframe[years >= filters.year_min]
                        years = years[years >= filters.year_min]
                    if filters.year_max is not None:
                        dataframe = dataframe[years <= filters.year_max]
                    break

        if filters.price_min is not None or filters.price_max is not None:
            for col in ("Price"):
                if col in dataframe.columns:
                    prices = pandas.to_numeric(dataframe[col], errors="coerce")
                    if filters.price_min is not None:
                        dataframe = dataframe[prices >= filters.price_min]
                        prices = prices[prices >= filters.price_min]
                    if filters.price_max is not None:
                        dataframe = dataframe[prices <= filters.price_max]
                    break

        if filters.genre_contains:
            for col in ("Genres", "Tags"):
                if col in dataframe.columns:
                    dataframe = dataframe[dataframe[col].astype(str).str.contains(filters.genre_contains, case=False, na=False)]
                    break

        if filters.min_review_score is not None:
            for col in ("User score", "Review score"):
                if col in dataframe.columns:
                    scores = pandas.to_numeric(dataframe[col], errors="coerce")
                    dataframe = dataframe[scores >= filters.min_review_score]
                    break

        if filters.min_reviews is not None:
            for col in ("Recommendations", "Positive"):
                if col in dataframe.columns:
                    reviews = pandas.to_numeric(dataframe[col], errors="coerce")
                    dataframe = dataframe[reviews >= filters.min_reviews]
                    break
        
        return DatasetPandas(dataframe)

    def get_page(self, page: int, page_size: int) -> list[Row]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 1
        start = (page - 1) * page_size
        end = start + page_size
        rows: list[Row] = []
        for _, row in self.df.iloc[start:end].iterrows():
            rows.append([value.item() if hasattr(value, "item") else value for value in row.tolist()])
        return rows
    
    def get_column_values(self, columns: list[str]) -> list[Row]:
        """
        Takes 1 or more columns and returns all the rows within those column/s
        
        Args:
        columns (list[str]): the column names to return values of
        
        Returns:
        None
        """
        selection = self.df.loc[:, columns]
        return [list(values) for values in selection.itertuples(index=False, name=None)]

    def column_exists(self, column_name: str) -> bool:
        """
        Check if a column exists in the dataframe
        
        Args:
            column_name (str): Name of column to check
            
        Returns:
            bool
        """
        return column_name in self.df.columns

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
        if source_column not in self.df.columns:
            raise KeyError(f"Missing column: {source_column}")

        counts: list[int] = []
        for value in self.df[source_column]:
            if isinstance(value, list):
                counts.append(len(value))
            elif isinstance(value, str):
                if seperator is None:
                    raise ValueError("seperator is required for string values")
                parts = value.split(seperator)
                non_empty_parts = [part for part in parts if part.strip()]
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
        if pandas is None:
            raise RuntimeError("Pandas is not available.")

        if column1 not in self.df.columns or column2 not in self.df.columns:
            raise KeyError(f"Missing column: {column1} or {column2}")

        left = pandas.to_numeric(self.df[column1], errors="coerce").fillna(0.0)
        right = pandas.to_numeric(self.df[column2], errors="coerce").fillna(0.0)
        self.create_new_column(new_column, (left + right).tolist(), overwrite=overwrite)

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
        import numpy
        if pandas is None:
            raise RuntimeError("Pandas is not available.")

        if logcolumn not in self.df.columns:
            raise KeyError(f"Missing column: {logcolumn}")

        values = pandas.to_numeric(self.df[logcolumn], errors="coerce").fillna(0.0)
        values = values.clip(lower=0)
        self.create_new_column(newcolumn, numpy.log1p(values).tolist(), overwrite=overwrite)

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
        if pandas is None:
            raise RuntimeError("Pandas is not available.")

        if mmcolumn not in self.df.columns:
            raise KeyError(f"Missing column: {mmcolumn}")

        values = pandas.to_numeric(self.df[mmcolumn], errors="coerce").fillna(0.0)
        min_value = float(values.min())
        max_value = float(values.max())

        if max_value == min_value:
            self.create_new_column(newcolumn, [0.0] * len(values), overwrite=overwrite)
            return

        scaled = (values - min_value) / (max_value - min_value)
        self.create_new_column(newcolumn, scaled.tolist(), overwrite=overwrite)

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
        if pandas is None:
            raise RuntimeError("Pandas is not available.")

        if scorecolumn not in self.df.columns:
            raise KeyError(f"Missing column: {scorecolumn}")

        values = pandas.to_numeric(self.df[scorecolumn], errors="coerce").fillna(0.0)
        mean_value = float(values.mean())
        std_value = float(values.std(ddof=0))

        if std_value == 0:
            self.create_new_column(newcolumn, [0.0] * len(values), overwrite=overwrite)
            return

        zscores = (values - mean_value) / std_value
        self.create_new_column(newcolumn, zscores.tolist(), overwrite=overwrite)

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
        if pandas is None:
            raise RuntimeError("Pandas is not available.")

        if source_column not in self.df.columns:
            raise KeyError(f"Missing column: {source_column}")

        extracted = self.df[source_column].astype(str).str.extract(r"(\d{4})", expand=False).fillna("")
        self.create_new_column(new_column, extracted.tolist(), overwrite=overwrite)

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
        if len(rows) != len(self.df):
            raise ValueError(f"Expected {len(self.df)} values for new column '{column_name}'")
        if self.column_exists(column_name) and not overwrite:
            raise ValueError(f"Column already exists: {column_name}")
        self.df[column_name] = rows

    def search(self, search_term: str) -> DatasetPandas:
        """
        Dataset viewer search function
        
        Args:
            search_term (string): the term to search
            
        Returns:
            Dataset
        """
        
        if not search_term:
            return self

        search_term = search_term.lower()

        # Very cool casting of our entire dataset as strings 
        text = self.df.astype(str)
            
        # Cool pandas stuff, allowing you to apply a function to an entire dataset
        # And then pythons anonymous functions make for some very neat coding 
        matches = text.apply(lambda col: col.str.contains(search_term, case=False, na=False)).any(axis=1)
        return DatasetPandas(self.df[matches])
