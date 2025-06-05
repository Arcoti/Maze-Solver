from .edge import Node

class Vertex():
    def __init__(self, node: Node):
        self.dist = float('inf')
        self.prev: Vertex | None = None
        self.node = node

    @property
    def role(self):
        return self.node.role
    
    @property
    def coordinate(self):
        return self.node.coordinate
    
    @property
    def isIntersection(self):
        return self.node.border.intersection
