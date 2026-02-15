from app.services.terminal_size_service import check_terminal_size
from app.views.rich.terminal_size import render_terminal_size_check_rich


def terminal_size_controller(state, console=None) -> None:
    """
    During initilisation handle terminal size checking and displaying results
    
    Args:
        state (AppState): application state controller
        console (optional, Console): Rich Console
        
    Returns:
        None
        
    Exceptions:
        RuntimeError: if Rich is unavailable 
        #TODO: When the Nolib display variant is done allow things to progress
    
    """
    if console is None or not hasattr(console, "size"):
        raise RuntimeError("Console from Rich not defined")
    
    ok = check_terminal_size(state.sug_term_width, state.sug_term_height, console)
    if not ok:
        render_terminal_size_check_rich(console, state.sug_term_width, state.sug_term_height)
