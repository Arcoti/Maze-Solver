import os
import pathlib

from .cell import Cell, Transit
from .direction import Direction
from ..model.border import Border
from ..model.square import Square
from ..persistence.serializer import dump

from .generator import Generator
from ..model.maze import Maze
from ..model.role import Role
from ..view.renderer import SVGRenderer

class Modeler:

    @staticmethod
    def generateTransit(maze: set["Cell"]) -> list[tuple["Cell", "Transit"]]:
        cells = sorted(list(maze), key = lambda c : c.coordinate)
        transits = [Transit(cell.coordinate) for cell in cells]
        return list(zip(cells, transits))
    
    @staticmethod
    def updateBorders(current: tuple["Cell", "Transit"], rest: list[tuple["Cell", "Transit"]]):
        direction = current[0].direction 
        border = current[1].border
        coordinate = current[1].coordinate

        if direction == Direction.NONE:
            return

        match = {
            Direction.NORTH: border & ~Border.NORTH, 
            Direction.SOUTH: border & ~Border.SOUTH,
            Direction.EAST: border & ~Border.EAST,
            Direction.WEST: border & ~Border.WEST
        }

        current[1].border = match[direction]

        mapping = {
            Direction.NORTH: ((coordinate[0] + 1, coordinate[1]), Border.SOUTH),
            Direction.SOUTH: ((coordinate[0] - 1, coordinate[1]), Border.NORTH),
            Direction.EAST: ((coordinate[0], coordinate[1] + 1), Border.WEST),
            Direction.WEST: ((coordinate[0], coordinate[1] - 1), Border.EAST)
        }

        nextCord, target = mapping[direction]
        nextCell = next((cell for cell in rest if cell[1].coordinate == nextCord), None)

        if nextCell != None:
            nextCell[1].border = nextCell[1].border & ~target

    @staticmethod
    def generateSquareAttri(maze: set["Cell"], row: int, col: int) -> list["Transit"]:
        mazeInTransit = Modeler.generateTransit(maze)
        result = []

        for cellInTransit in mazeInTransit:

            if cellInTransit[1].coordinate == (0, 0):
                cellInTransit[1].role = Role.ENTRANCE
                cellInTransit[1].border = cellInTransit[1].border & ~Border.SOUTH
            elif cellInTransit[0].coordinate == (row - 1, col - 1):
                cellInTransit[1].role = Role.EXIT
                cellInTransit[1].border = cellInTransit[1].border & ~Border.NORTH

            Modeler.updateBorders(cellInTransit, mazeInTransit)
            result.append(cellInTransit[1])

        return result

    @staticmethod
    def generateSquares(squareAttri: list["Transit"], rows: int) -> list["Square"]:
        return sorted([Square(cell.generateIndex(rows), cell.reverseCoordinates(rows), cell.border, cell.role) for cell in squareAttri], key = lambda s: s.coordinate)
    
    @staticmethod
    def generate(row: int, col: int, path: pathlib.Path):
        maze = Generator.generateMaze(row, col)
        inTransit = Modeler.generateSquareAttri(maze, row, col)
        squares = Modeler.generateSquares(inTransit, row)

        maze = Maze(tuple(squares))

        dump(maze, path)

        renderer = SVGRenderer()
        renderer.render(maze).preview()


if __name__ == "__main__":
    currentDirectory = os.getcwd()
    filePath = currentDirectory + "\\static\\random(8x8).maze"

    Modeler.generate(8, 8, pathlib.Path(filePath))