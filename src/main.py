import os
from pathlib import Path

from .graph.solver import Solver
from .view.renderer import SVGRenderer
from .persistence.serializer import load

if __name__ == "__main__":
    currentDirectory = os.getcwd()
    filePath = currentDirectory + "\\static\\miniature.maze"

    # Load the sample miniature maze
    maze = load(Path(filePath))

    # Solve the maze
    solution = Solver.findShortestPath(maze)

    # Render the maze solution
    renderer = SVGRenderer()
    # svg = renderer.render(maze, solution)

    # # Save the maze solution as an svg file
    # with Path("static/maze.svg").open(mode="w", encoding="utf-8") as file:
    #     file.write(svg.xmlContent)

    # Preview of Solution
    renderer.render(maze, solution).preview()