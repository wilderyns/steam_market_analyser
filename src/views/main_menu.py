from rich.console import Console
from ..models import AppState


def show_main_menu(console: Console, state: AppState) -> None:
    print("\n" + "=" * 30)
    print("Main Menu")
    print("=" * 30)
    print("1) TODO: View dataset records")
    print("2) TODO: Set / edit filters")
    print("3) TODO: View dataset")
    print("4) TODO: Analysis Toolkit")
    print("5) TODO: Export last results")
    print("99) Quit")