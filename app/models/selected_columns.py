from typing import Optional


class SelectedColumns:
    available_columns: list[str] = None
    # selected can be optional because if none are we'll show them all
    selected: Optional[list[str]] = None

    def load_columns(self, columns: list[str]):
         self.available_columns = list(dict.fromkeys(columns))
         
         # We'll set a sensible default number of columns
         # The Steam dataset has 40 columns, showing the first 7 seems safe
         # Also handle less than 7 in case somethign went wrong
         
         for x in range(0,6):
             self.toggle(self.available_columns[x])
        
    def clear(self) -> None:
        self.selected = []

    def is_selected(self, column: str) -> bool:
        if self.selected is None:
            return True
        return column in self.selected

    def toggle(self, column: str) -> None:
        if self.selected is None:
            self.selected = []

        if column in self.selected:
            self.selected.remove(column)
        else:
            self.selected.append(column)

    def resolve(self) -> list[str]:
        if self.selected is None:
            return self.available_columns

        selected_set = set(self.selected)
        return [name for name in self.available_columns if name in selected_set]