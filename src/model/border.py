from enum import IntFlag, auto

class Border(IntFlag):
    EMPTY = 0
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

    @property
    def deadend(self) -> bool:
        return self.bit_count() == 3
    
    @property
    def corner(self) -> bool:
        return self in (
            self.NORTH | self.EAST,
            self.NORTH | self.WEST,
            self.SOUTH | self.EAST,
            self.SOUTH | self.WEST
        )

    @property
    def intersection(self) -> bool: # Find squares which has more than two pathways (e.g. a T junction or a cross road)
        return self.bit_count() < 2