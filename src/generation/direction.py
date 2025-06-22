from enum import IntEnum, auto

class Direction(IntEnum):
    NONE = 0
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()   # Right
    WEST = auto()   # Left