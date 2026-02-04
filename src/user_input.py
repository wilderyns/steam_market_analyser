# Sanitize and error check menu input 
from typing import Optional

def input_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            # TODO: Add checks to ensure value is within min/max bounds if provided
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            
def input_float(prompt: str, min_value: Optional[float] = None, max_value: Optional[float] = None) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            # TODO: Add checks to ensure value is within min/max bounds if provided
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def input_str(prompt: str, min_length: Optional[int] = None, max_length: Optional[int] = None, allowed_values: Optional[list] = None) -> str:
    while True:
        try:
            value = input(prompt).strip()
            return value
        except ValueError:
            print("Invalid input. Please enter a valid string.")
