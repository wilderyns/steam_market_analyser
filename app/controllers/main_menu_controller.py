from rich.console import Console
from app.controllers.filters_controller import filters_controller
from app.models.appstate import AppState
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
            error = f"{raw if raw else 'That input'} is an invalid option"
            continue

        if choice not in [99, 1, 2]:
            error = f"{choice} is an invalid option"
            continue

        error = None

        if choice == 99:
            console.print("Goodbye!")
            break
        elif choice == 1:
             console.print ("View dataset")
        elif choice == 2:
            filters_controller(state, console)
    
    return True
