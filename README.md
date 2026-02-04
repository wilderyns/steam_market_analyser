
# Steam Market Analyser
Using the Steam Games Dataset, the Steam Market Analyser (SMA) interprets the current Steam game library and provides useful information and statistics. Current features include:

 - Counting total number of games and filtering by genre, tag, release
   year range, price range, and review score
 - Log transform of the number of reviews or game owners
 - Min-max scaling of price and review score
 - Mean/median price by genre
 - Min/max/percentile selection of games by price or review score
 - Top 10 best value based on the formula value=normalised_review_score * log(1 + review_count) / (1 +normalised_price)
 - Pattern identification such as genre popularity (by average review
   score / count) and how pricebands relate to review scores
- Recognise errors like missing file, bad columns, non-numeric values
- User input and flow control
- Count records

## Project Structure

    ├── README.md
    ├── __init__.py
    ├── data
    │   ├── datasets
    │   │   └── games.csv
    │   └── exports
    ├── docs
    └── src
        ├── analysis.py
        ├── cleaning.py
        ├── io.py
        ├── main.py
        ├── menus.py
        ├── models.py
        ├── reporting.py
        ├── requirements.txt
        ├── transforms.py
        ├── user_input.py
        └── verify.py

  

## Columns in dataset
    AppID
    Name
    Release date
    Estimated owners
    Peak CCU
    Required age
    Price
    DiscountDLC count
    About the game
    Supported languages
    Full audio languages
    Reviews
    Header image
    Website
    Support url
    Support email
    Windows
    Mac
    Linux
    Metacritic score
    Metacritic url
    User score
    Positive
    Negative
    Score rank
    Achievements
    Recommendations
    Notes
    Average playtime forever
    Average playtime two weeks
    Median playtime forever
    Median playtime two weeks
    Developers
    Publishers
    Categories
    Genres
    Tags
    Screenshots
    Movies
