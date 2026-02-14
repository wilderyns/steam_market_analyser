from typing import Optional


class Filters:
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    genre_contains: Optional[str] = None
    min_review_score: Optional[float] = None  
    min_reviews: Optional[int] = None
    adult_content: Optional[bool] = False