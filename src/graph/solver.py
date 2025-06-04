import math

from .edge import Node
from .edge import Edge
from .vertex import Vertex
from .convertor import Convertor
from ..model.role import Role
from ..model.maze import Maze

from ..model.square import Square # For main function, delete when not needed
from ..model.border import Border # For main function, delete when not needed

class Solver():

    @classmethod
    def initializeVertices(cls, nodes: set[Node]):
        vertices: set[Vertex] = set()

        for node in nodes:
            vertices.add(Vertex(node))

        return vertices

    @classmethod
    def getEntrances(cls, vertices):
        return set(vertex for vertex in vertices if vertex.role == Role.ENTRANCE)
    
    @classmethod
    def getExits(cls, vertices):
        return set(vertex for vertex in vertices if vertex.role == Role.EXIT)
    
    @classmethod
    def getEdges(cls, edges: set[Edge], target: tuple[int, int]):
        return filter(lambda edge : edge.source.coordinate == target or edge.destination.coordinate == target, edges)

    @classmethod
    def calculateDistance(cls, point1: tuple[int, int], point2: tuple[int, int]):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))
    
    @classmethod
    def getDestination(cls, cord: tuple[int, int], vertices: set[Vertex]):
        return next(vertex for vertex in vertices if vertex.coordinate == cord)

    @classmethod
    def solve(cls, entrance: Vertex, exits: set[Vertex], vertices, edges):
        # Initialize distance travelling from itself to itself
        entrance.dist = 0

        # Initialize unexplored vertices
        explored = set([entrance])

        source = entrance
        while exits.isdisjoint(explored):
            # Get all the edges whose source or destination is the entrance
            relatedEdges = cls.getEdges(edges, source.coordinate)

            # Store all the possible destinations for this current source
            places = set()

            # Loop through all related edges and find the coordinates they are travelling to
            for relatedEdge in relatedEdges:
                if source.coordinate == relatedEdge.source.coordinate:
                    travellingTo = relatedEdge.destination.coordinate
                else:
                    travellingTo = relatedEdge.source.coordinate
            
                # Calculate the distance
                distance = cls.calculateDistance(source.coordinate, travellingTo)

                # Get the vertex of the destination base on the coordinates and add it to places
                destination = cls.getDestination(travellingTo, vertices)
                places.add(destination)

                # Update destination variables if the total distance is less than destination.dist
                if source.dist + distance < destination.dist:
                    destination.dist = source.dist + distance
                    destination.prev = source
            
            # Find the next destination whose distance should be the minimum out of all possible places
            nextDestination = min(places, key=lambda p : p.dist)
            explored.add(nextDestination)

            # Update source
            source = nextDestination
        
        # When loop ends, source is now one of the exits
        path = []
        current = source
        while current.prev is not None:
            path.append(current.node)
            current = current.prev
        path = path[::-1]
        distance = source.dist

        return path, distance    
    
    @classmethod
    def findShortestPath(cls, maze: Maze):
        nodes, edges = Convertor.convertToGraph(maze)

        vertices = cls.initializeVertices(nodes)

        entrances = cls.getEntrances(vertices)
        exits = cls.getExits(vertices)

        shortestPath = []
        shortestDist = float('inf')

        for entrance in entrances:
            path, dist = cls.solve(entrance, exits, vertices, edges)

            if dist < shortestDist:
                shortestPath = path
                shortestDist = dist
        
        return shortestPath

    
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

    path = Solver.findShortestPath(maze)
    print(path)