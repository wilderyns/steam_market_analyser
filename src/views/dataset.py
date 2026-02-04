from controllers.dataset import get_dataset_view
from ..models import AppState, Filters
from ..user_input import input_int, input_float, input_str
from rich.console import Console
from rich.table import Table

def view_dataset(console: Console, state: AppState, n: int = 20) -> None:
    console.clear()
    table = get_dataset_view(state, n)
    console.print(table)