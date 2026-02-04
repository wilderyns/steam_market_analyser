# Helper classes to hold application data structures

from typing import Optional
from pathlib import Path
from pandas import DataFrame

    
class Filters:
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    genre_contains: Optional[str] = None
    min_review_score: Optional[float] = None  
    min_reviews: Optional[int] = None

class AppState:
    dataset_path: Path
    dataframe: Optional[DataFrame] = None
    filters: Filters = Filters()
    last_results: Optional[DataFrame] = None
