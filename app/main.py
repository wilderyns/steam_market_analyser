from pathlib import Path

from app.controllers import dataset_controller, feature_controller, main_menu_controller, terminal_size_controller
from app.models import AppState

def main() -> None:
    # Create the app state 
    state = AppState(dataset_path=Path("data/steam_market_data.csv"))
    
    # Load the feature check controller. This will currently return an error if Rich is not availabale
    if not feature_controller(state):
        return 
    
    # We can safely import Rich and start rendering a Rich generated view.
    from rich import Console
    console = Console()
    
    # Hand over to the terminal size controller to get things looking how they should, or at least trying to
    terminal_size_controller(state, console)
    
    # Now we can initialize the dataset 
    dataset_controller(state, console)
    
    # And with that out of the way let's call the main_menu controller which will handle (surpisngly) the main menu
    main_menu_controller(state, console)

if __name__ == "__main__":
    main()