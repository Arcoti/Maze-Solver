from collections import deque

from .edge import Node
from .edge import Edge
from .vertex import Vertex
from .convertor import Convertor
from ..model.role import Role
from ..model.maze import Maze
from ..model.solution import Solution

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
    def getDestination(cls, cord: tuple[int, int], vertices: set[Vertex]):
        return next(vertex for vertex in vertices if vertex.coordinate == cord)

    @classmethod
    def solve(cls, entrance: Vertex, exits: set[Vertex], vertices, edges):
        # Initialize distance travelling from itself to itself
        entrance.dist = 0

        # Initialize unexplored vertices
        explored = set([entrance])

        # Initialize empty stack
        stack = deque()

        source = entrance
        while exits.isdisjoint(explored):
            # Store all the previously visited intersections
            if source.role != Role.ENTRANCE and source.isIntersection:
                stack.append(source)

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
            
                # Get the distance
                distance = relatedEdge.distance

                # Get the vertex of the destination base on the coordinates and add it to places
                destination = cls.getDestination(travellingTo, vertices)
                places.add(destination)

                # Update destination variables if the total distance is less than destination.dist
                if source.dist + distance < destination.dist:
                    destination.dist = source.dist + distance
                    destination.prev = source
            
            # Find the next destination whose distance should be the minimum out of all possible non-visited places
            destinations = sorted(places, key = lambda d : d.dist)

            index = 0
            nextDestination = None
            while index < len(destinations):

                if destinations[index] not in explored:
                    nextDestination = destinations[index]
                    explored.add(nextDestination)
                    break

                index += 1
            
            if nextDestination is None:
                if len(stack) == 0: # Check if stack is empty
                    return [], float('inf')
                
                nextDestination = stack.pop()

            # Update source
            source = nextDestination
        
        # When loop ends, source is now one of the exits
        path = []
        current = source
        while current is not None:
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
            # Reset Vertices
            for vertice in vertices:
                vertice.reset()

            path, dist = cls.solve(entrance, exits, vertices, edges)

            if dist < shortestDist:
                shortestPath = path
                shortestDist = dist
        
        return Solution(tuple(shortestPath))
