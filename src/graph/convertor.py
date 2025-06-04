from ..model.border import Border
from ..model.maze import Maze
from ..model.role import Role
from .edge import Node
from .edge import Edge

from ..model.square import Square # For main function, delete when not needed

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
            
            node = sourceNode
            
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
    
if __name__ == "__main__":
    maze = Maze(
        squares=(
            Square(0, (0, 0), Border.NORTH | Border.WEST),
            Square(1, (0, 1), Border.NORTH | Border.EAST),
            Square(2, (0, 2), Border.WEST | Border.EAST, Role.EXIT),
            Square(3, (0, 3), Border.NORTH | Border.WEST | Border.EAST),
            Square(4, (1, 0), Border.SOUTH | Border.WEST | Border.EAST),
            Square(5, (1, 1), Border.WEST | Border.EAST),
            Square(6, (1, 2), Border.SOUTH | Border.WEST),
            Square(7, (1, 3), Border.EAST),
            Square(8, (2, 0), Border.NORTH | Border.WEST, Role.ENTRANCE),
            Square(9, (2, 1), Border.SOUTH),
            Square(10, (2, 2), Border.NORTH | Border.SOUTH),
            Square(11, (2, 3), Border.SOUTH | Border.EAST),
        )
    )

    nodes, edges = Convertor.convertToGraph(maze)
    for node in nodes:
        print(node.coordinate)
    
    for edge in edges:
        print(edge.source.coordinate, " -> ", edge.destination.coordinate)