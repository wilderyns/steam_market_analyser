from mimetypes import init

from pandas import DataFrame

from .helpers import attempt_resize, clear_terminal, detect_size
from .banner import print_banner
from .features import check_features
from .menus import show_filters_menu, show_main_menu, view_dataset
from .models import AppState
from .dataset import fetch_dataset, load_dataset
import sys, os

terminal_width = 120
terminal_height = 40

def main() -> None:
    state = AppState()
    state.dataset_path = os.path.join(os.path.dirname(__file__), "../data/steam_market_data.csv")
    
    # Do some terminal housekeeping here, there's going to be a lot of data and a fancy banner to show
    clear_terminal()
    if detect_size() < (terminal_width, terminal_height):
        attempt_resize(terminal_width, terminal_height)
        if detect_size() < (terminal_width, terminal_height):
            print(f"Warning: Terminal size is smaller than recommended {terminal_width}x{terminal_height}. Some content may not display correctly.")
            print(f"Please resize and then press any key to continue...")
            input()
            clear_terminal()
            
    print_banner()
    
    check_features()
    
    # Let's do all the dataset loading and verification here 
    print("\n" + "=" * 30)
    print("Checking dataset...")
    
    dataset = load_dataset(state.dataset_path)
    if isinstance(dataset, Exception):
        print(f"Error loading dataset: {dataset}")
        
        if (dataset is FileNotFoundError) and (not state.features.has_requests):
            print("Dataset not found at data/steam_market_data.csv and requests library not available.")
            print("Please download the dataset manually from:")
            print("https://www.kaggle.com/fronkongames/steam-games-dataset")
            print("And place it at data/steam_market_data.csv")
            print("Or install requests library with pip install requests to allow SMA to fetch the dataset automatically.")
            print("Exiting...")
            sys.exit(1)
        elif(dataset is FileNotFoundError) and state.features.has_requests:
            print("Dataset not found at data/steam_market_data.csv but requests library is available.")
            print("Attempting to fetch dataset automatically...")
            fetch_dataset(state.features)
            # TODO: Double check the whole dataset fetching thing
            
        else:
            print("Unrecoverable error loading dataset. Exiting...")
            sys.exit(1)
        
    if isinstance(dataset, DataFrame):
        state.dataframe = dataset
        print("Dataset initialised successfully")
    else:
        print("Unknown error loading dataset. Exiting...")
        sys.exit(1)
    print("\n" + "=" * 30)
    # Main app loop. Main menu show function called and input handled here as opposed
    # to inside the menu function 
    while True:
        active_filters = []
        if state.filters.year_min is not None:
            active_filters.append(f"Year: {state.filters.year_min} - {state.filters.year_max}")
        if state.filters.price_min is not None:
            active_filters.append(f"Price: ${state.filters.price_min} - ${state.filters.price_max}")
        if state.filters.genre_contains is not None:
            active_filters.append(f"Genre contains: '{state.filters.genre_contains}'")
        if state.filters.min_review_score is not None:
            active_filters.append(f"Min review score: {state.filters.min_review_score}")
        if state.filters.min_reviews is not None:
            active_filters.append(f"Min reviews: {state.filters.min_reviews}")
            
        print("\nActive filters: " + ", ".join(active_filters) if active_filters else "No active filters")
        
        show_main_menu()
        choice = input("Choice: ").strip()
        
        if choice == "99":
            print("Goodbye!")
            break
        elif choice == "1":
            view_dataset(state.dataframe, n=20)
        elif choice == "2":
            show_filters_menu(state)
        elif choice == "3":
            print("TODO: Run analysis")
        elif choice == "4":
            print("TODO: Export last results")
        elif choice == "5":
            print("TODO: Verification")
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()