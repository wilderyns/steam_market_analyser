from rich.console import Console
from app.controllers.columns_controller import columns_controller
from app.controllers.filters_controller import filters_controller
from app.controllers.dataset_controller import view_dataset_controller
from app.models.appstate import AppState
from app.utils.terminal import clear_terminal
from app.utils.user_input_handler import expect_user_input
from app.views.rich.main_menu import render_main_menu_rich

def main_menu_controller(state: AppState, console=None):
    """
    Handles main menu display loop and input
    
    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console
        
    Returns:
        None
    """
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")

    error = None

    while True:
        render_main_menu_rich(state, console, error)
        
        choice = expect_user_input(int, [1, 2, 3, 99], None, None, console)

        if choice == 99:
            console.print("Goodbye!")
            break
        elif choice == 1:
            clear_terminal(console)
            view_dataset_controller(state, console)
        elif choice == 2:
            clear_terminal(console)
            filters_controller(state, console)
        elif choice == 3:
            clear_terminal(console)
            columns_controller(state, console)
    
    return True
