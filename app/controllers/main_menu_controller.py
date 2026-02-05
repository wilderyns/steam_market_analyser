from rich.console import Console
from app.models.appstate import AppState
from app.views.rich.main_menu import render_main_menu_rich
from app.utils.user_input_handler import expect_user_input

def main_menu_controller(state: AppState, console=None):
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")
    
    while True:
        render_main_menu_rich(state, console)
        choice = expect_user_input(int, [99, 1, 2, 3, 4], None, None, None, console)
        
        if choice == "99":
            console.print("Goodbye!")
            break
        elif choice == "1":
            print ("View dataset")
        elif choice == "2":
            print ("Set filters")
        elif choice == "3":
            print("TODO: Run analysis")
        elif choice == "4":
            print("TODO: Export last results")
        else:
            print("Invalid choice. Please try again.")   
            
        return True 