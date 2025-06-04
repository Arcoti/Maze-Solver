from dataclasses import dataclass
from functools import cached_property
from typing import Iterator

from .square import Square
from .role import Role
from .border import Border

@dataclass(frozen=True)
class Maze:
    squares: tuple[Square, ...]

    def __post_init__(self):
        self.validateIndices()
        self.validateRowsCols()
        self.validateEntrance()
        self.validateExit()

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
    
    @cached_property
    def entrance(self):
        return next(square for square in self if square.role == Role.ENTRANCE)
    
    @cached_property
    def exit(self):
        return next(square for square in self if square.role == Role.EXIT)
    
    def validateIndices(self):
        assert [square.index for square in self] == list(range(len(self.squares))), "Wrong square indices."

    def validateRowsCols(self):
        for x in range(self.height):
            for y in range(self.width):
                square = self[x * self.width + y]
                assert square.coordinate[0] == x, "Wrong x coordinate."
                assert square.coordinate[1] == y, "Wrong y coordinate."
    
    def validateEntrance(self):
        assert any(square.role == Role.ENTRANCE for square in self) == True, "There must be at least one entrance."
    
    def validateExit(self):
        return any(square.role == Role.EXIT for square in self), "There must be at least one exit."