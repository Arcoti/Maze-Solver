import tempfile
import textwrap
import webbrowser
from dataclasses import dataclass

from ..model.maze import Maze
from ..model.role import Role
from ..model.square import Square
from ..model.solution import Solution
from .decomposer import decompose
from .primitives import tag, Rect, Point, Polyline, Text

ROLEEMOJI = {
    Role.ENTRANCE: "\N{pedestrian}",
    Role.EXIT: "\N{chequered flag}",
    Role.ENEMY: "\N{ghost}",
    Role.REWARD: "\N{white medium star}",
}

@dataclass(frozen=True)
class SVG:
    xmlContent: str

    @property
    def htmlContent(self) -> str:
        return textwrap.dedent("""\
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title> SVG Preview </title>
            </head>
            <body>
            {0}                   
            </body>
            </html>
        """).format(self.xmlContent)
        # dedent -> remove prior whitespaces
        # {0} -> Use positional placeholder
        # format -> replace {0} with self.xmlContent
    
    def preview(self) -> None:
        # Create temporary file with .html suffix
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix="html", delete=False # to prevent automatic deleting
        ) as file:
            file.write(self.htmlContent)
        webbrowser.open(f"file://{file.name}") # display the rendered SVG image

@dataclass(frozen=True)
class SVGRenderer:
    squareSize: int = 100
    lineWidth: int = 6

    @property
    def offset(self): # Distance from the top and left edge of the drawing space
        return self.lineWidth // 2
    
    def _getBody(self, maze: Maze, solution: Solution | None) -> str:
        return "".join([
            arrowMarker(),
            background(),
            *map(self._drawSquare, maze),
            self._drawSolution(solution) if solution else "",
        ])
    
    def render(self, maze: Maze, solution: Solution | None = None) -> SVG:
        margins = 2 * (self.offset + self.lineWidth)
        width = margins + maze.width * self.squareSize
        height = margins + maze.height * self.squareSize

        return SVG(
            tag(
                "svg",
                self._getBody(maze, solution),
                xmlns="http://www.w3.org/2000/svg", # Official svg namespace, informs how to interpret the tags
                stroke_linejoin="round",
                width=width,
                height=height,
                viewBox=f"0 0 {width} {height}",
            )
        )
    
    def _transform(self, square: Square, extraOffset: int = 0) -> Point:
        return Point(
            x=square.coordinate[1] * self.squareSize,
            y=square.coordinate[0] * self.squareSize,
        ).translate(
            x=self.offset + extraOffset,
            y=self.offset + extraOffset
        )
    
    def _drawSquare(self, square: Square) -> str:
        topLeft: Point = self._transform(square)
        tags = []
        if square.role is Role.EXTERIOR:
            tags.append(exterior(topLeft, self.squareSize, self.lineWidth))
        elif square.role is Role.WALL:
            tags.append(wall(topLeft, self.squareSize, self.lineWidth))
        elif emoji := ROLEEMOJI.get(square.role):
            tags.append(label(emoji, topLeft, self.squareSize // 2)) 
        tags.append(self._drawBorder(square, topLeft))
        return "".join(tags)
    
    def _drawBorder(self, square: Square, topLeft: Point) -> str:
        return decompose(square.border, topLeft, self.squareSize).draw(
            stroke_width=self.lineWidth,
            stroke="black",
            fill="none"
        )
    
    def _drawSolution(self, solution: Solution) -> str:
        return Polyline(
            [
                self._transform(point, self.squareSize // 2) for point in solution
            ]
        ).draw(
            stroke_width = self.lineWidth // 2,
            stroke_opacity = "50%",
            stroke = "red",
            fill = "none",
            marker_end = "url(#arrow)",
        )
    
def exterior(topLeft: Point, size: int, lineWidth: int) -> str:
    return Rect(topLeft).draw(
        width=size,
        height=size,
        strokeWidth=lineWidth,
        stroke="none",
        fill="white"
    )

def wall(topLeft: Point, size: int, lineWidth: int) -> str:
    return Rect(topLeft).draw(
        width=size,
        height=size,
        strokeWidth=lineWidth,
        stroke="none",
        fill="lightgray"
    )

def label(emoji: str, topLeft: Point, offset: int) -> str:
    return Text(emoji, topLeft.translate(x=offset, y=offset)).draw(
        font_size=f"{offset}px",
        text_anchor="middle",
        dominant_baseline="middle",
    )
    
# Arrowhead
def arrowMarker() -> str:
    return tag(
        "defs",
        tag(
            "marker", 
            tag(
                "path",
                d="M 0,0 L 10,5 L 0,10 2,5 z",
                fill="red",
                fill_opacity="50%"
            ),
            id="arrow",
            viewBox="0 0 20 20",
            refX="2",
            refY="5",
            markerUnits="strokeWidth",
            markerWidth="10",
            markerHeight="10",
            orient="auto"
        )
    )

# Background
def background() -> str:
    return Rect().draw(width="100%", height="100%", fill="white")