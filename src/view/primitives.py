from dataclasses import dataclass
from typing import Protocol, NamedTuple

# Interface
class Primitive(Protocol):
    def draw(self, **attributes) -> str:
        ...

class Point(NamedTuple):
    x: int
    y: int

    def draw(self, **attributes) -> str:
        return f"{self.x},{self.y}"     # Returns a SVG point as a python string
    
    def translate(self, x=0, y=0) -> "Point":
        return Point(self.x + x, self.y + y)

class Line(NamedTuple):
    start: Point
    end: Point

    def draw(self, **attributes) -> str:
        return tag(
            "line",
            x1 = self.start.x,
            y1 = self.start.y,
            x2 = self.end.x,
            y2 = self.end.y,
            **attributes,   # Unpacks the attributes
        )

class Polyline(tuple[Point, ...]):
    def draw(self, **attributes) -> str:
        points = " ".join(point.draw() for point in self)
        return tag("Polyline", points=points, **attributes)
    
class Polygon(tuple[Point, ...]):
    def draw(self, **attributes) -> str:
        points = " ".join(point.draw() for point in self)
        return tag("Polygon", points=points, **attributes)

class DisjointLines(tuple[Line, ...]):
    def draw(self, **attributes) -> str:
        return "".join(line.draw(**attributes) for line in self)

@dataclass(frozen=True)
class Rect:
    topLeft: Point | None = None

    def draw(self, **attributes) -> str:
        if self.topLeft:
            attrs = attributes | {"x": self.topLeft.x, "y": self.topLeft.y} # Union two dictionaries, if attributes have x and y, overwrite with topLeft coordinates
        else:
            attrs = attributes

        return tag("rect", **attrs)

@dataclass(frozen=True)
class Text:
    content: str
    point: Point

    def draw(self, **attributes) -> str:
        return tag(
            "text", 
            self.content, # Passed as positional argument
            x=self.point.x,
            y=self.point.y,
            **attributes
        )   

class NullPrimitive:
    def draw(self, **attributes) -> str:
        return ""

# Render XML tag
def tag(name: str, value: str | None = None, **attributes) -> str:
    attrs = "" if not attributes else " " + " ".join(
        f'{key.replace("_", "-")}="{value}"' for key, value in attributes.items()
    )

    if value is None:
        return f"<{name}{attrs} />"
    return f"<{name}{attrs}>{value}</{name}>"
