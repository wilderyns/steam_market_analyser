# Sanitize and error check menu input 
from typing import Optional

from app.utils.terminal import clear_terminal_lines

def expect_user_input(t: type[str | int | float | bool], choices: Optional[list[str | int | float | bool]] = None, min_val: Optional[int | float] = None, max_val: Optional[int | float] = None, console=None, prompt: str = "Select an option: "):
    """
    Handles user input prompts, checks types, handles displaying user input error
    
    Args:
        t (str | int | float | bool): Type of user input to expect
        choices (Optional, list[str | int | float | bool]): List of user inputs that are allowed 
        min_val (Optional, int | float): Minimum integer value expected 
        max_val (Optional, int | float): Maximum integer value expected
        console (Console): Rich console object
        prompt (Optional, str): Text display before user input area
        
    Returns:
        val: A string, integer, float, or bool, depending on user input type allowed
    """
    
    had_error = False
    last_error: Optional[str] = None
    rendered_error = False
    
    def show_error(msg: str):
        if console is not None:
            console.print(f"[red]{msg}[/red]")
        else:
            print(msg)

    def parse_bool(raw: str) -> bool:
        value = raw.strip().lower()
        if value in ("y", "yes", "true", "1"):
            return True
        if value in ("n", "no", "false", "0"):
            return False
        raise ValueError

    while True:
        if had_error:
            if console is not None:
                # keeping the console clean by only showing one error
                clear_terminal_lines(2 if rendered_error else 1, console)
            if last_error is not None:
                show_error(last_error)
                rendered_error = True
            
        raw = console.input(prompt).strip() if console is not None else input(prompt).strip()

        try:
            if t == str:
                val = raw
            elif t == int:
                try:
                    val = int(raw)
                except ValueError:
                    raise ValueError("Invalid input, please enter a valid int.")
            elif t == float:
                try:
                    val = float(raw)
                except ValueError:
                    raise ValueError("Invalid input, please enter a valid float.")
            elif t == bool:
                try:
                    val = bool(raw)
                    val = parse_bool(raw)
                except ValueError:
                    raise ValueError("Invalid input, please enter yes/no, y/n, 1/0.")
            else:
                raise ValueError

            if choices is not None and val not in choices:
                raise ValueError(f"Input must be one of: {', '.join(str(c) for c in choices)}")
            if min_val is not None and val < min_val:
                raise ValueError(f"Input must be >= {min_val}")
            if max_val is not None and val > max_val:
                raise ValueError(f"Input must be <= {max_val}")

            return val
        except ValueError as e:
            had_error = True
            msg = str(e)
            if not msg:
                msg = f"Invalid input, please enter a valid {t.__name__}."
            last_error = msg
            if console is None:
                show_error(msg)
