from datetime import date

from app.utils.user_input_handler import expect_user_input
from app.models.appstate import AppState
from app.views.rich.filters_menu import render_filters_menu_rich

todays_date = date.today()

def filters_controller(state: AppState, console=None):
    render_filters_menu_rich(state, console)
    
    while True:        
        choice = expect_user_input(int, [0, 99, 1, 2, 3, 4, 5], None, None, console)
    
        if choice == 0:
            return
        
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
        elif choice == 99:
            state.reset_filters()

        render_filters_menu_rich(state, console)
