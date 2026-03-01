from typing import Optional



class Filters:
    """
    Filters holds applied dataset filters

    Attributes:
    year_min: the minimum year to display applied to release date
    year_max: the maximum year to display applied to release date
    price_min: the minimum price to display applied to price
    price_max: the maximum price to display applied to price
    genre_contains: shows only rows which contain the selected genres
    min_review_score: shows only rows that are above the given review score
    min_reviews: shows only rows which have over the given number of reviews
    show_adult_conent: hides rows based on "adult content" tags defined in the dataset models
    """
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    genre_contains: Optional[str] = None
    min_review_score: Optional[float] = None  
    min_reviews: Optional[int] = None
    show_adult_content: Optional[bool] = False
    
    # Not yet implemented 
    on_windows: Optional[bool] = True
    on_mac: Optional[bool] = True
    on_linux: Optional[bool] = True
    owners_min: Optional[int] = None
    owners_max: Optional[int] = None
    ccu_min: Optional[int] = None
    ccu_max: Optional[int] = None
    minimum_age: Optional[int] = None
    
    
    
    # Peak CCU,Required age,Price,Discount,DLC count,About the game,Supported languages,Full audio languages,Reviews,Header image,Website,Support url,Support email,Windows,Mac,Linux,Metacritic score,Metacritic url,User score,Positive,Negative,Score rank,Achievements,Recommendations,Notes,Average playtime forever,Average playtime two weeks,Median playtime forever,Median playtime two weeks,Developers,Publishers,Categories,Genres,Tags,Screenshots,Movies