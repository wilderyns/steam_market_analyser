from datetime import date

from app.utils.user_input_handler import expect_user_input
from app.models.appstate import AppState
from app.services.transformation_service import clear_transformations
from app.views.rich.filters_menu import render_filters_menu_rich

todays_date = date.today()

def filters_controller(state: AppState, console=None):
    """
    Handles filter menu loop, offering user input and view display
    
    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console
        
    Returns:
        None
    """
    render_filters_menu_rich(state, console)
    
    while True:        
        choice = expect_user_input(int, [0, 99, 1, 2, 3, 4, 5, 6], None, None, console)
    
        if choice == 0:
            return

        if state.transformations_applied and choice in [1, 2, 3, 4, 5, 6, 99]:
            undo = expect_user_input(
                bool,
                None,
                None,
                None,
                console,
                "Changing filters will undo active transformations. Continue? (y/n): "
            )
            if not undo:
                render_filters_menu_rich(state, console)
                continue
            clear_transformations(state)
        
        f = state.filters
        
        if choice == 1:
            f.year_min = expect_user_input(int, None, 1960, todays_date.year, console, "Minimum year: ")
            f.year_max = expect_user_input(int, None, 1960, todays_date.year, console, "Maximum year: ")
        elif choice == 2:
            f.price_min = expect_user_input(float, None, 0.0, None, console, "Minimum price: ")
            f.price_max = expect_user_input(float, None, 0.0, None, console, "Maximum price: ")
        elif choice == 3:
            f.genre_contains = expect_user_input(str, None, None, None, console, "Genre contains: ")
        elif choice == 4:
            f.min_review_score = expect_user_input(float, None, 0.0, 10.0, console, "Minimum review score: ")
        elif choice == 5:
            f.min_reviews = expect_user_input(int, None, 0, None, console, "Minimum reviews: ")
        elif choice == 6:
            f.show_adult_content = expect_user_input(bool, None, None, None, console, "Display adult games? ")
        elif choice == 99:
            state.reset_filters()

        render_filters_menu_rich(state, console)
