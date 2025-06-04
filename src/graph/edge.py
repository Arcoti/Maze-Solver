from typing import NamedTuple, TypeAlias

from ..model.square import Square

Node: TypeAlias = Square

class Edge(NamedTuple):
    source: Node
    destination: Node