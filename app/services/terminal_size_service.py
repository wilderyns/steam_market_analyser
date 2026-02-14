import os
import sys

import app.models.appstate

def attempt_resize(cols: int, rows:int) -> None:
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))
    
def detect_size() -> int | int:
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(cols), int(rows)

def check_terminal_size(min_width: int, min_height: int, console=None) -> bool:
    if console is None or not hasattr(console, "size"):
        return False

    s = console.size
    return s.width >= min_width and s.height >= min_height
