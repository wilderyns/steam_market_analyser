from datetime import date

from app.controllers.main_menu_controller import expect_user_input
from app.models.appstate import AppState
from app.views.rich.filters_menu import render_filters_menu_rich

todays_date = date.today()

def filters_controller(state: AppState, console=None):
    
    
    
    while True:
        render_filters_menu_rich(console, state)
        
        choice = expect_user_input(int, [99, 1, 2, 3, 4, 5], None, None, None, console)
    
        if choice == "0":
            return
        
        f = state.filters
        
        if choice == "1":
            f.year_min = expect_user_input(int, None, 1960, todays_date.year, "Minimum year: ", console)
            f.year_max = expect_user_input(int, None, 1960, todays_date.year, "Maximum year: ", console)
        elif choice == "2":
            f.price_min = expect_user_input(float, None, 0.0, None, "Minimum price: ", console)
            f.price_max = expect_user_input(float, None, 0.0, None, "Maximum price: ", console)
        elif choice == "3":
            f.genre_contains = expect_user_input(str, None, None, None, "Genre contains: ", console)
        elif choice == "4":
            f.min_review_score = expect_user_input(float, None, 0.0, 10.0, "Minimum review score: ", console)
        elif choice == "5":
            f.min_reviews = expect_user_input(int, None, 0, None, "Minimum reviews: ", console)
        elif choice == "99":
            state.filters = state.reset_filters
        else:
            print("Invalid choice.")