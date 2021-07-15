"""
This type stub file was generated by pyright.
"""

class FieldCursor:
    def __init__(self, data_getter, pre_history_setter, post_history_setter, data_max_length, data_view_length, data_count) -> None:
        ...
    
    @property
    def x(self): # -> int:
        ...
    
    @property
    def y(self): # -> Literal[0]:
        ...
    
    @property
    def data(self):
        ...
    
    def move(self, x, y): # -> None:
        ...
    
    def move_left(self): # -> None:
        ...
    
    def move_right(self): # -> None:
        ...
    
    def move_up(self): # -> None:
        ...
    
    def move_down(self): # -> None:
        ...
    
    def insert(self, value): # -> None:
        ...
    
    def backspace(self): # -> None:
        ...
    
    def delete(self): # -> None:
        ...
    
    def process_input(self): # -> None:
        ...
    


