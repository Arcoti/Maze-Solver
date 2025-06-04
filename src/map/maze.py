from dataclasses import dataclass
from functools import cached_property
from typing import Iterator

from .square import Square

@dataclass(frozen=True)
class Maze:
    squares: tuple[Square, ...]

    # Enable usage of for or while loop
    def __iter__(self) -> Iterator[Square]:
        return iter(self.squares) # Takes in an iterable and returns an iterable object

    # Enable usage of square brackets like mazeObject[1]
    def __getitem__(self, index: int) -> Square:
        return self.squares[index]
    
    @cached_property # This expensive computation is cached so that it is only generated once
    def width(self):
        return max(square.coordinate[1] for square in self.squares) + 1 # Add 1 to take into account 0 based numbering

    @cached_property
    def height(self):
        return max(square.coordinate[0] for square in self.squares) + 1 # Add 1 to take into account 0 based numbering