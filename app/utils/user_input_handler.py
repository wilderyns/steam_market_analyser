# Sanitize and error check menu input 
from typing import Optional

def expect_user_input(t: type[str | int | float | bool], choices: Optional[list[str | int | float | bool]] = None, min_val: Optional[int | float] = None, max_val: Optional[int | float] = None, prompt: Optional[str] = "Select an option: ", console=None):
    # If usign Rich life becomes easy because it has inbuilt validation
    if console is not None:
        try:
            if t == str:
                from rich.prompt import Prompt
                if choices is not None:
                    return Prompt.ask(prompt, choices)
                else:
                    return Prompt.ask(prompt)
                
            elif t == int:
                from rich.prompt import IntPrompt
                if choices is not None:
                    val = IntPrompt.ask(prompt, choices)
                else:
                    val = IntPrompt.ask(prompt)
                
                if val <= min_val or val >= max_val:
                    return ValueError("Value not in range")
                else:
                    return val
                
            elif t == int:
                from rich.prompt import FloatPrompt
                if choices is not None:
                    val = FloatPrompt.ask(prompt, choices)
                else:
                    val = FloatPrompt.ask(prompt)
                if val <= min_val or val >= max_val:
                    return ValueError("Value not in range")
                else:
                    return val
                
            elif t == bool:
                from rich.prompt import Confirm
                return Confirm.ask(prompt)
        except Exception:
            pass
        
    # If not using Rich gotta handle that validation ourselves and loop to wait for input
    while True:
        input = input(prompt).strip()
        
        try:
            if t == str:
                if choices is not None and input not in choices:
                    err = "Input is not one of the available options."
                    if console is not None: 
                        console.print(f"[red]{err}[/red]")
                    else:
                        print(err)
                else:
                    return str(input)
            
            elif t == int:
                #TODO: Handle ints properly including min and max
                return int(input)
            
            elif t == float:
                return float(input)
            
            elif t == bool:
                return bool(input)
                 
        except ValueError:
            err = "Invalid input, please enter a {t}"
            if console is not None:
                console.print(f"[red]{err}[/red]")
            else:
                print(err)