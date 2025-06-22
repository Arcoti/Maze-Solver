from dataclasses import dataclass
from functools import cached_property

from direction import Direction

@dataclass
class Cell:
    coordinate: tuple[int, int]
    direction: Direction

    @cached_property
    def neighbouringCoordinates(self):
        return [
            (self.coordinate[0], self.coordinate[1] + 1),
            (self.coordinate[0], self.coordinate[1] - 1),
            (self.coordinate[0] + 1, self.coordinate[1]),
            (self.coordinate[0] - 1, self.coordinate[1]),
        ]
