from app.services.terminal_size_service import check_terminal_size
from app.views.rich.terminal_size import render_terminal_size_check_rich


def terminal_size_controller(state, console=None) -> None:
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")
    
    ok = check_terminal_size(state.sug_term_width, state.sug_term_height, console)
    if not ok:
        render_terminal_size_check_rich(console, state.sug_term_width, state.sug_term_height)
