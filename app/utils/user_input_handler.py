# Sanitize and error check menu input 
from typing import Optional

def expect_user_input(t: type[str | int | float | bool], choices: Optional[list[str | int | float | bool]] = None, min_val: Optional[int | float] = None, max_val: Optional[int | float] = None, console=None, prompt: str = "Select an option: "):
    had_error = False

    def clear_last_error():
        if console is not None and had_error:
            console.file.write("\033[1A\033[2K")
            console.file.flush()

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
        clear_last_error()
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
                    val = parse_bool(raw)
                except ValueError:
                    raise ValueError("Invalid input, please enter yes/no.")
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
            show_error(msg)
