from dataclasses import dataclass
from functools import cached_property

from .direction import Direction
from ..model.border import Border
from ..model.role import Role

@dataclass
class Cell:
    """
    Represents a cell for generation of a maze using Wilson's Algorithm.
    """
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

@dataclass
class Transit:
    """
    Represents a cell or more specifically a square in transit, allowing its properties to be changed in 
    the process of generation of squares and maze. 
    """
    coordinate: tuple[int, int]
    border: Border = Border.NORTH | Border.SOUTH | Border.EAST | Border.WEST
    role: Role = Role.NONE

    def generateIndex(self, rows: int):
        coordinate = self.reverseCoordinates(rows)
        return (coordinate[0] * rows + coordinate[1])
    
    def reverseCoordinates(self, rows: int):
        return (rows - self.coordinate[0] - 1, self.coordinate[1])