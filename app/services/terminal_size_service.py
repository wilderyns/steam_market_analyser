import os
import sys

import app.models.appstate

def attempt_resize(cols: int, rows:int) -> None:
    """
    Hacky attempt to resize terminal with ANSI escape codes
    
    Args:
        cols (int): Number of terminal columns to resize (width)
        rows (int): Number of terminal rows to resize (height)
        
    Returns:
        None
    """
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))
    
def detect_size() -> int | int:
    """
    Detect terminal size by piping stty size and examining the result
    #TODO: Will only work on unix because stty, detect if Windows and do something for that?
    
    Args:
        cols (int): Number of terminal columns to resize (width)
        rows (int): Number of terminal rows to resize (height)
        
    Returns:
        None
    """
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(cols), int(rows)

def check_terminal_size(min_width: int, min_height: int, console=None) -> bool:
    """
    Rich console variant to determine if terminal meets size requirements 
    
    Args:
        min_width (int): Number of terminal columns to resize (width)
        min_height (int): Number of terminal rows to resize (height)
        console (Console): Rich console object
    
    Returns:
        True if terminal meets size requirements in args, otherwise False. Also False if Console object not passed.
    """
    if console is None or not hasattr(console, "size"):
        return False

    s = console.size
    return s.width >= min_width and s.height >= min_height
