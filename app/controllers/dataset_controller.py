from rich.table import Table
from rich import box
import pandas

from app.services.dataset_service import init_dataset 
from ..models import AppState


def dataset_controller(state, console=None):
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")
    
    init_dataset(state)
    return True