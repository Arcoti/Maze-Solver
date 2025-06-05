from dataclasses import dataclass
from functools import reduce
from typing import Iterator

from .square import Square
from .role import Role

@dataclass(frozen=True)
class Solution:
    squares: tuple[Square, ...]

    def __post_init__(self):
        self.validateEntrance()
        self.validateExit()
        reduce(self.validatePath, self.squares)

    # Enable usage of for or while loop
    def __iter__(self) -> Iterator[Square]:
        return iter(self.squares) # Takes in an iterable and returns an iterable object

    # Enable usage of square brackets like solurionObject[1]
    def __getitem__(self, index: int) -> Square:
        return self.squares[index]
    
    # Enable usage of len function
    def __len__(self) -> int:
        return len(self.squares)
    
    def validateEntrance(self):
        assert self.squares[0].role == Role.ENTRANCE, "First square should be Entrance"
    
    def validateExit(self):
        assert self.squares[-1].role == Role.EXIT, "Last square should be Exit"

    def validatePath(self, current: Square, following: Square):
        assert any([
            current.coordinate[0] == following.coordinate[0],
            current.coordinate[1] == following.coordinate[1]
        ]), "Consecutive squares must be on the same row or column"

        return following
