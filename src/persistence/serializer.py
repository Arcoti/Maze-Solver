import array
import pathlib

from ..model.maze import Maze
from ..model.role import Role
from ..model.border import Border
from ..model.square import Square
from .format import FileHeader, FileBody

FORMATVERSION: int = 1

def compress(square: Square) -> int:
    return (square.role << 4) | square.border.value

def decompress(squareValue: int) -> tuple[Border, Role]:
    return Border(squareValue & 0xf), Role(squareValue >> 4)

def serialize(maze: Maze) -> tuple[FileHeader, FileBody]:
    header = FileHeader(FORMATVERSION, maze.width, maze.height)
    body = FileBody(array.array('B', map(compress, maze)))          # map each square in maze to compress function and add it to array.array
    return header, body

def deserialize(header: FileHeader, body: FileBody) -> Maze:
    squares: list[Square] = []

    for index, squareValue in enumerate(body.squareValues):
        row, column = divmod(index, header.width)
        border, role = decompress(squareValue)
        squares.append(Square(index, (row, column), border, role))
    
    return Maze(tuple(squares))

def dump(maze: Maze, path: pathlib.Path) -> None:
    header, body = serialize(maze)

    with path.open(mode="wb") as file:
        header.write(file)
        body.write(file)

def load(path: pathlib.Path) -> Maze:

    with path.open(mode="rb") as file:
        header = FileHeader.read(file)

        if header.formatVersion != FORMATVERSION:
            raise ValueError("Unsupported file format version")
        
        body = FileBody.read(header, file)
        
        return deserialize(header, body)
