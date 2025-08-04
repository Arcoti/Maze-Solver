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
    def reconstructPath(cls, node: Vertex):
        path, distance = [], node.dist
        current = node
        while current is not None:
            path.append(current)
            current = current.prev

        return path[::-1], distance
    
    @classmethod
    def dijkstra(cls, entrance: Vertex, exits: set[Vertex], vertices, edges):
        # Initialize entrace g value
        entrance.dist = 0

        # Initialize explored and visited vertices
        explored = [entrance]
        visited = set()

        source = entrance
        while len(explored) != 0:
            # Obtain the node with the lowest g value and add them to the explored list
            source = explored.pop(0)
            visited.add(source)

            if source in exits:
                return cls.reconstructPath(source)

            # Get all the edges whose source or destination is the entrance
            relatedEdges = cls.getEdges(edges, source.coordinate)

            # Loop through all related edges and find the coordinates they are travelling to
            for relatedEdge in relatedEdges:
                if source.coordinate == relatedEdge.source.coordinate:
                    travellingTo = relatedEdge.destination.coordinate
                else:
                    travellingTo = relatedEdge.source.coordinate
            
                # Get the distance
                distance = relatedEdge.distance + source.dist

                # Get the vertex of the destination base on the coordinates and add it to places
                destination = cls.getDestination(travellingTo, vertices)

                if destination in visited:
                    continue

                if destination not in explored:
                    explored.append(destination)
                elif distance >= destination.dist:
                    continue
                
                # Update Vertice details
                destination.dist = distance
                destination.prev = source
            
            explored = sorted(explored, key = lambda d : d.dist)

        return [], 0  
    
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

            path, dist = cls.dijkstra(entrance, exits, vertices, edges)

            if dist < shortestDist:
                shortestPath = path
                shortestDist = dist
        
        return Solution(tuple(shortestPath))
