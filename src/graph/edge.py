import math
from typing import NamedTuple, TypeAlias

from ..model.square import Square

Node: TypeAlias = Square

class Edge(NamedTuple):
    source: Node
    destination: Node

    @property
    def distance(self) -> float:
        point1 = self.source.coordinate
        point2 = self.destination.coordinate
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))