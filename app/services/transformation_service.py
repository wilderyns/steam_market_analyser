from app.models.dataset import Dataset


def transform_create_count(to_transform: str | list[str | int | bool], seperator: str | None, dataset: Dataset ,new_column_name: str):
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

def transform_column_combine():
    """
    Creates a new total reviews column by combining positive and negative review counts 
    
    Args:
        None
        
    Returns:
        None
    """
    return 

def create_review_score():
    """
    Creates a new review score column calculated as positive/(positive + negative)
    
    Args:
        None
        
    Returns:
        None
    """
    return 

def perform_log_transform():
    """
    Creates new log scaled columns for estimated owners, CCU, and total reviews)
    
    Args:
        None
        
    Returns:
        None
    """
    return

def perform_min_max_scale():
    """
    Creates new min/max scaled columns for price,  
    
    Args:
        None
        
    Returns:
        None
    """
    return 

def perform_zscore():
    """
    Creates new min/max scaled columns for price,  
    
    Args:
        None
        
    Returns:
        None
    """
    return 

def create_value_for_money():
    return 
