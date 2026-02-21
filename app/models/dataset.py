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
        raise NotImplementedError

    def row_count(self) -> int:
        raise NotImplementedError

    def filter(self, filters: Filters) -> Dataset:
        raise NotImplementedError
    
    def get_page(self, page: int, page_size: int) -> list[Row]:
        raise NotImplementedError
    
    def search(self, search_term) -> Dataset:
        raise NotImplementedError
    
    def transform_create_count(self, new_column_name: str, to_transform: str | list[str | int | bool], seperator: str | None):
        """
        Takes a string, splits at the seperator, and creates a new column with the count. Or takes a list and creates a new column with the count.
        
        Args:
            to_transform (str | list[str | int | bool]): The string or list to count
            seperator (str | None): The seperator for a to_tranform given as a string
            dataset (Dataset): The dataset where the new column will be added
            new_column_name (str): The name of the new column to add to the dataset
            
        Returns:
            None
        """
        return 

    def transform_column_combine(self, column1, column2, new_column):
        """
        Creates a new column by combining values from previous columns
        
        Args:
            None
            
        Returns:
            None
        """
        return 

    def transform_create_log(self, logcolumn, newcolumn):
        """
        Creates new log scaled column from a non scaled column
        
        Args:
            None
            
        Returns:
            None
        """
        return

    def transform_create_minmax(self, mmcolumn, newcolumn):
        """
        Creates new min/max scaled column 
        
        Args:
            None
            
        Returns:
            None
        """
        return 

    def transform_create_zscore(self, scorecolumn, newcolumn):
        """
        Creates a zscore column
        
        Args:
            None
            
        Returns:
            None
        """
        return 
    
    def create_new_column(self, column_name, rows):
        return