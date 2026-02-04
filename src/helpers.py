import os, sys
def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    print(chr(27) + "[2J")
    
def attempt_resize(cols: int, rows:int) -> None:
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))
    
def detect_size() -> int | int:
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(cols), int(rows)