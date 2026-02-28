
# Steam Market Analyser
The Steam Market Analyser (SMA) takes the Steam Games dataset from Kaggle and aims to provide useful display and analysis of this data including:
- Viewing the dataset with filters such as:
- Year range
- Genres  
- Minimum review score
- Minimum reviews 
- Include/exclude games marked as adult

One can then use a suite of transformation and analysis functions to perform analyses on the dataset and from this produce new data or graphs.

## Setup and Use

### 1. Get SMA
```bash
git clone https://github.com/wilderyns/steam_market_analyser
cd steam_market_analyser
```

### 2. Create Python virtual environment 
```bash
python3 -m venv .env
source .env/bin/activate
```

### 3. Install dependencies & run
```bash
pip install -r requirements.txt
python -m app.main
```

## Requirements
- Python 3.11+ (tested on Python 3.14)
- A Steam Games Dataset CSV at `data/steam_market_data.csv`
- - The application will attempt to automatically download this if it doesn't exist. The application comes with a dataset that has removed a number of columns to reduce file size (see Dataset Structure below).

### Libraries

- `rich`: required for full CLI UI (menus, tables, panels)
- `pandas`: enables pandas dataset backend
- `numpy`: enables numeric transforms 
- `matplotlib`: enables graph creation 
- `requests`: enables automatic dataset download from configured dataset URL
- `pytest`: used for testing

### Fallbacks
- In the event Pandas is not present the application will use a standard library implementation, the downside being a reduction in performance.
- A non-Rich UI is planned however not yet implemented

## Known issues
- No fallback to a standard library UI without Rich
- Adult games filtering only filters based on tags, not genre 
- Dataset loading view is handled in controller as opposed to Rich/Stdlib veiw
- Lack of customisation during graph generation
- Lack of graphing options 

## Project Structure
```
steam_market_analyser/
├─ app/
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ main.py
│  ├─ controllers/
│  │  ├─ columns_controller.py
│  │  ├─ dataset_controller.py
│  │  ├─ export_controller.py
│  │  ├─ feature_controller.py
│  │  ├─ filters_controller.py
│  │  ├─ graph_controller.py
│  │  ├─ main_menu_controller.py
│  │  ├─ terminal_size_controller.py
│  │  └─ transformation_controller.py
│  ├─ models/
│  │  ├─ appstate.py
│  │  ├─ dataset.py
│  │  ├─ dataset_nolib.py
│  │  ├─ dataset_pandas.py
│  │  ├─ features.py
│  │  ├─ filters.py
│  │  └─ selected_columns.py
│  ├─ services/
│  │  ├─ dataset_service.py
│  │  ├─ export_service.py
│  │  ├─ feature_service.py
│  │  ├─ graph_service.py
│  │  ├─ terminal_size_service.py
│  │  └─ transformation_service.py
│  ├─ utils/
│  │  ├─ terminal.py
│  │  └─ user_input_handler.py
│  └─ views/
│     ├─ banner.py
│     ├─ nolib/
│     │  └─ feature_check.py
│     └─ rich/
│        ├─ active_filters_panel.py
│        ├─ columns_menu.py
│        ├─ dataset_viewer.py
│        ├─ export_menu.py
│        ├─ filters_menu.py
│        ├─ graph_menu.py
│        ├─ main_menu.py
│        ├─ terminal_size.py
│        └─ transform_root.py
├─ data/
│  ├─ PLACE_STEAM_MARKET_DATA_CSV_HERE
│  └─ steam_market_data.csv
├─ docs/
│  └─ writeup.md
├─ exports/
│  └─ *.csv
├─ graphs/
│  └─ *.png
├─ tests/
│  └─ test_output.py
├─ README.md
└─ requirements.txt
```
  
## Dataset Structure
```
    AppID
    Name
    Release date
    Estimated owners
    Peak CCU
    Required age
    Price
    DiscountDLC count**
    About the game !
    Supported languages
    Full audio languages !
    Reviews !
    Header image !
    Website !
    Support url !
    Support email !
    Windows
    Mac
    Linux
    Metacritic score
    Metacritic url !
    User score !
    Positive
    Negative
    Score rank
    Achievements
    Recommendations
    Notes !
    Average playtime forever
    Average playtime two weeks !
    Median playtime forever !
    Median playtime two weeks !
    Developers
    Publishers
    Categories
    Genres
    Tags
    Screenshots !
    Movies !
```

**Should be 2 columns: "Discount" and "DLC Count", fixed in processing

! Denotes columns removed in the dataset included with SMA

