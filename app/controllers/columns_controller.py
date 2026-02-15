from datetime import date

from app.utils.user_input_handler import expect_user_input
from app.models.appstate import AppState
from app.views.rich.columns_menu import render_columns_menu

def columns_controller(state: AppState, console=None):
    """
    Handles column selection menu loop, offering user input and view display
    
    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console
        
    Returns:
        None
    """
    render_columns_menu(state, console)
    
    while True: 
        c = state.columns
               
        choice = expect_user_input(int, None, 0, len(c.available_columns), console)

        if choice == 0:
            return
        
        c.toggle(int(choice-1))
        
        render_columns_menu(state, console)
        

        
        