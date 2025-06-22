from dataclasses import dataclass
from functools import cached_property

from .direction import Direction

@dataclass
class Cell:
    coordinate: tuple[int, int]
    direction: Direction

    def __hash__(self):
        return hash(self.coordinate)
    
    def __eq__(self, other):
        return isinstance(other, Cell) and self.coordinate == other.coordinate

    @cached_property
    def neighbouringCoordinates(self):
        return [
            (self.coordinate[0], self.coordinate[1] + 1),
            (self.coordinate[0], self.coordinate[1] - 1),
            (self.coordinate[0] + 1, self.coordinate[1]),
            (self.coordinate[0] - 1, self.coordinate[1]),
        ]
