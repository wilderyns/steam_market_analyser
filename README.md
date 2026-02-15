
# Steam Market Analyser
The Steam Market Analyser (SMA) takes the Steam Games dataset from Kaggle and aims to provide useful display and analysis of this data including:
- Viewing the dataset with filters such as:
- Name (contains, begins with, ends with)
- Genres 
- Tags
- Year range
- Platform selection
- Owners range 
- Minimum review volume
- Minimum review score (as transformed percentage) 
- Calculating average price of games in the dataset (with or without filters)
- Review score transformation expressed as a percentage
- Top 10 games by review score (with minimum reviews)
- Platform distribution 
- Genre vs price comparison 
- Average games released per year

## Project Structure
├── app
│   ├── __init__.py
│   ├── __main__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-314.pyc
│   │   ├── __main__.cpython-314.pyc
│   │   ├── banner.cpython-314.pyc
│   │   ├── dataset.cpython-314.pyc
│   │   ├── features.cpython-314.pyc
│   │   ├── helpers.cpython-314.pyc
│   │   ├── loader.cpython-314.pyc
│   │   ├── main.cpython-314.pyc
│   │   ├── menus.cpython-314.pyc
│   │   ├── models.cpython-314.pyc
│   │   └── user_input.cpython-314.pyc
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-314.pyc
│   │   │   ├── columns_controller.cpython-314.pyc
│   │   │   ├── dataset_controller.cpython-314.pyc
│   │   │   ├── dataset.cpython-314.pyc
│   │   │   ├── feature_controller.cpython-314.pyc
│   │   │   ├── filters_controller.cpython-314.pyc
│   │   │   ├── main_menu_controller.cpython-314.pyc
│   │   │   └── terminal_size_controller.cpython-314.pyc
│   │   ├── columns_controller.py
│   │   ├── dataset_controller.py
│   │   ├── feature_controller.py
│   │   ├── filters_controller.py
│   │   ├── main_menu_controller.py
│   │   └── terminal_size_controller.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-314.pyc
│   │   │   ├── appstate.cpython-314.pyc
│   │   │   ├── dataset_nolib.cpython-314.pyc
│   │   │   ├── dataset_pandas.cpython-314.pyc
│   │   │   ├── dataset.cpython-314.pyc
│   │   │   ├── features.cpython-314.pyc
│   │   │   ├── filters.cpython-314.pyc
│   │   │   └── selected_columns.cpython-314.pyc
│   │   ├── appstate.py
│   │   ├── dataset_nolib.py
│   │   ├── dataset_pandas.py
│   │   ├── dataset.py
│   │   ├── features.py
│   │   ├── filters.py
│   │   └── selected_columns.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-314.pyc
│   │   │   ├── dataset_service.cpython-314.pyc
│   │   │   ├── feature_service.cpython-314.pyc
│   │   │   └── terminal_size_service.cpython-314.pyc
│   │   ├── dataset_service.py
│   │   ├── feature_service.py
│   │   └── terminal_size_service.py
│   ├── utils
│   │   ├── __pycache__
│   │   │   ├── terminal.cpython-314.pyc
│   │   │   └── user_input_handler.cpython-314.pyc
│   │   ├── terminal.py
│   │   └── user_input_handler.py
│   └── views
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-314.pyc
│       │   ├── active_filters.cpython-314.pyc
│       │   ├── banner.cpython-314.pyc
│       │   ├── check_dataset.cpython-314.pyc
│       │   ├── check_terminal.cpython-314.pyc
│       │   ├── dataset.cpython-314.pyc
│       │   ├── filters.cpython-314.pyc
│       │   └── main_menu.cpython-314.pyc
│       ├── banner.py
│       ├── nolib
│       │   ├── __pycache__
│       │   │   └── feature_check.cpython-314.pyc
│       │   └── feature_check.py
│       └── rich
│           ├── __pycache__
│           │   ├── active_filters_panel.cpython-314.pyc
│           │   ├── columns_menu.cpython-314.pyc
│           │   ├── dataset_viewer.cpython-314.pyc
│           │   ├── filters_menu.cpython-314.pyc
│           │   ├── main_menu.cpython-314.pyc
│           │   └── terminal_size.cpython-314.pyc
│           ├── active_filters_panel.py
│           ├── columns_menu.py
│           ├── dataset_viewer.py
│           ├── filters_menu.py
│           ├── main_menu.py
│           └── terminal_size.py
├── data
│   ├── exports
│   └── steam_market_data.csv
├── docs
│   └── writeup.md
├── README.md
├── requirements.txt
└── Week 5 Accompanying Video.mov

  
## Columns in dataset
    AppID
    Name
    Release date
    Estimated owners
    Peak CCU
    Required age
    Price
    DiscountDLC count**
    *Should be Discount | DLC Count, fixed in processing
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
