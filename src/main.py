import os
from pathlib import Path

from .model.maze import Maze
from .model.role import Role
from .model.square import Square
from .model.border import Border
from .graph.solver import Solver
from .view.renderer import SVGRenderer
from .persistence.serializer import dump, load

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
    
    currentDirectory = os.getcwd()
    filePath = currentDirectory + "\\static\\miniature.maze"

    dump(maze, Path(filePath))
    maze = load(Path(filePath))

    solution = Solver.findShortestPath(maze)
    renderer = SVGRenderer()
    svg = renderer.render(maze, solution)

    with Path("static/maze.svg").open(mode="w", encoding="utf-8") as file:
        file.write(svg.xmlContent)

    renderer.render(maze).preview()
    renderer.render(maze, solution).preview()