from ..model.border import Border
from ..model.maze import Maze
from ..model.role import Role
from .edge import Node
from .edge import Edge

class Convertor:
    nodes: set[Node] = set()
    edges: set[Edge] = set()

    @classmethod
    def getNodes(cls, maze: Maze):
        for square in maze:
            if square.role == Role.EXTERIOR or square.role == Role.WALL:
                continue

            if square.role is not Role.NONE:
                cls.nodes.add(square)
            
            if square.border.corner or square.border.deadend or square.border.intersection:
                cls.nodes.add(square)
    
        return cls.nodes

    @classmethod
    def getEdges(cls, maze: Maze):
        for sourceNode in cls.nodes:
            node = sourceNode

            # Move right
            for x in range(node.coordinate[1] + 1, maze.width):
                if node.border & Border.EAST:
                    break

                node = maze[node.coordinate[0] * maze.width + x]

                if node in cls.nodes:
                    cls.edges.add(Edge(sourceNode, node))
                    break
            
            # Move down
            for y in range(node.coordinate[0] + 1, maze.height):
                if node.border & Border.SOUTH:
                    break

                node = maze[y * maze.width + node.coordinate[1]]

                if node in cls.nodes:
                    cls.edges.add(Edge(sourceNode, node))
                    break
        
        return cls.edges
    
    @classmethod
    def convertToGraph(cls, maze: Maze):
        return (cls.getNodes(maze), cls.getEdges(maze))