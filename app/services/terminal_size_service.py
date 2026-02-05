import os
import sys

import app.models.appstate

def attempt_resize(cols: int, rows:int) -> None:
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))
    
def detect_size() -> int | int:
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(cols), int(rows)

def check_terminal_size(min_width: int, min_height: int, console=None) -> bool:
    def too_small() -> bool:
        if console is not None and hasattr(console, "size"):
            s = console.size
            return s.width < min_width or s.height < min_height
        
    if not too_small():
        return 1
    else:
        return 0

