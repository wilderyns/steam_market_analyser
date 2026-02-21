from typing import TypeAlias
from app.models.filters import Filters

Cell: TypeAlias = str | int | float | bool
Row: TypeAlias = list[Cell]

class Dataset:
    """
    The shared interface for dataset backends

    This class is not used directly but instead exists so the code throughout the application can use a single Dataset type
    """
    
    def columns(self) -> list[str]:
        """
        Return all column names in the dataset
        
        Args:
            None
            
        Returns:
            list[str]
        """
        raise NotImplementedError

    def row_count(self) -> int:
        """
        Return total row count of the dataset
        
        Args:
            None
            
        Returns:
            int
        """
        raise NotImplementedError

    def filter(self, filters: Filters) -> Dataset:
        """
        Apply filters and return a filtered dataset
        
        Args:
            filters (Filters): Filters object with active filter values
            
        Returns:
            Dataset
        """
        raise NotImplementedError
    
    def get_page(self, page: int, page_size: int) -> list[Row]:
        """
        Return one page of row data
        
        Args:
            page (int): The page number to return
            page_size (int): Number of rows per page
            
        Returns:
            list[Row]
        """
        raise NotImplementedError
    
    def search(self, search_term) -> Dataset:
        """
        Search dataset values and return matched rows
        
        Args:
            search_term (str): Search term to match
            
        Returns:
            Dataset
        """
        raise NotImplementedError

    def get_column_values(self, columns: list[str]) -> list[Row]:
        """
        Return row values from one or more columns
        
        Args:
            columns (list[str]): Column names to return data from
            
        Returns:
            list[Row]
        """
        raise NotImplementedError

    def column_exists(self, column_name: str) -> bool:
        """
        Check if a column exists in the dataset
        
        Args:
            column_name (str): Name of column to check
            
        Returns:
            bool
        """
        raise NotImplementedError
    
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
        raise NotImplementedError

    def transform_column_combine(self, column1: str, column2: str, new_column: str, overwrite: bool = False) -> None:
        """
        Create a new column by combining two numeric columns
        
        Args:
            column1 (str): First source column
            column2 (str): Second source column
            new_column (str): New column name
            overwrite (bool): Replace existing target column if True
            
        Returns:
            None
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError
    
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
        raise NotImplementedError
