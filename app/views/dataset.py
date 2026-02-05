"""
View for displaying the dataset, with the dataset information passed in from the controller 
"""

from .active_filters import print_active_filters_panel
from ..controllers.dataset_controller import get_dataset_view
from ..models import AppState
from ..user_input import input_int, input_float, input_str
from rich.console import Console

def view_dataset(console: Console, state: AppState, n: int = 10) -> None:
    console.clear()
    while True:
        console.clear()
        table = get_dataset_view(state, n, p=state.page)
        console.print(table)
        print_active_filters_panel(console, state)
        
        console.print("\nUse n and p keys to navigate pages, q to return to main menu.")
        
        key = console.input("\nKey: ").strip().lower()
        if key == "q":
            return
        elif key == "p" and state.page > 1:
            state.page -= 1
        elif key == "n":
            state.page += 1
        
    