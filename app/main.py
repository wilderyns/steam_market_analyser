from pathlib import Path

from app.controllers.feature_controller import feature_controller
from app.controllers.dataset_controller import dataset_controller
from app.controllers.terminal_size_controller import terminal_size_controller
from app.controllers.main_menu_controller import main_menu_controller
from app.models.appstate import AppState

def main() -> None:
    # Create the app state 
    state = AppState()
    state.dataset_path = Path("data/steam_market_data.csv")
    
    # Load the feature check controller. This will currently return an error if Rich is not availabale
    if not feature_controller(state):
        return 
    
    # We can safely import Rich and start rendering a Rich generated view.
    from rich.console import Console
    console = Console()
    
    # Hand over to the terminal size controller to get things looking how they should, or at least trying to
    terminal_size_controller(state, console)
    
    # Now we can initialize the dataset 
    dataset_controller(state, console)
    
    # And with that out of the way let's call the main_menu controller which will handle (surpisngly) the main menu
    main_menu_controller(state, console)

if __name__ == "__main__":
    main()