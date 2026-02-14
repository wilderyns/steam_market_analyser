from rich.console import Console
from app.controllers.filters_controller import filters_controller
from app.controllers.dataset_controller import view_dataset_controller
from app.models.appstate import AppState
from app.utils.terminal import clear_terminal
from app.views.rich.main_menu import render_main_menu_rich

def main_menu_controller(state: AppState, console=None):
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")

    error = None

    while True:
        render_main_menu_rich(state, console, error)
        raw = console.input("Select an option: ").strip()

        try:
            choice = int(raw)
        except ValueError:
            error = f"{raw if raw else 'That input'} isn't valid"
            continue

        if choice not in [99, 1, 2]:
            error = f"{choice} isn't valid"
            continue

        error = None

        if choice == 99:
            console.print("Goodbye!")
            break
        elif choice == 1:
            clear_terminal(console)
            view_dataset_controller(state, console)
        elif choice == 2:
            clear_terminal(console)
            filters_controller(state, console)
    
    return True
