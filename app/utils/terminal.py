def clear_terminal(console):
    """
    Clear terminal with ASCII escape characers.
    #TODO: Fix this, will notwork without console and need alternative to address that
    
    Escape codes pulled from wikipedia: https://en.wikipedia.org/wiki/ANSI_escape_code
    
    Args:
        console (Console): Rich console argument 
        
    Returns:
        None
    """
    if console is not None and hasattr(console, "file"):
        console.file.write("\033[2J\033[3J\033[H")
        console.file.flush()
    else:
        console.clear(home=True)

def clear_terminal_lines(count, console=None):
    """
    Clear specified number of lines in the terminal
    #TODO: Again, needs non Rich Console variant 
    
    Again escape codes pulled from wikipedia: https://en.wikipedia.org/wiki/ANSI_escape_code
    Args:
        count (int): Number of lines to clear 
        console (Console): Rich console argument 
        
    Returns:
        None
    """
    if console is not None and count > 0:
            console.file.write("\033[1A\033[2K" * count)
            console.file.flush()

