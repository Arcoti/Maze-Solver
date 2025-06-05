from ..model.border import Border
from .primitives import (
    Line, 
    Point, 
    Polygon,
    Polyline,
    Primitive,
    DisjointLines,
    NullPrimitive,
)

def decompose(border: Border, topLeft: Point, squareSize: int) -> Primitive:
    topRight: Point = topLeft.translate(x=squareSize)
    bottomRight: Point = topLeft.translate(squareSize, squareSize)
    bottomLeft: Point = topLeft.translate(y=squareSize)

    top = Line(topLeft, topRight)
    bottom = Line(bottomRight, bottomLeft)
    left = Line(topLeft, bottomLeft)
    right = Line(topRight, bottomRight)

    # Enclosed Square
    if border is Border.NORTH | Border.SOUTH | Border.EAST | Border.WEST:
        return Polygon(
            [
                topLeft,
                topRight, 
                bottomRight,
                bottomLeft
            ]
        )

    # Dead End
    if border is Border.WEST | Border.NORTH | Border.EAST:
        return Polyline(
            [
                bottomLeft,
                topLeft,
                topRight,
                bottomRight,

            ]
        )
    
    if border is Border.NORTH | Border.EAST | Border.SOUTH:
        return Polyline(
            [
                topLeft,
                topRight,
                bottomRight,
                bottomLeft
            ]
        )

    if border is Border.EAST | Border.SOUTH | Border.WEST:
        return Polyline(
            [
                topRight,
                bottomRight,
                bottomLeft,
                topLeft
            ]
        )
    
    if border is Border.SOUTH | Border.WEST | Border.NORTH:
        return Polyline(
            [
                bottomRight,
                bottomLeft,
                topLeft,
                topRight,
            ]
        )
    
    if border is Border.NORTH | Border.EAST:
        return Polyline(
            [
                topLeft,
                topRight,
                bottomRight,
            ]
        )
    
    if border is Border.EAST | Border.SOUTH:
        return Polyline(
            [
                topRight, 
                bottomRight,
                bottomLeft,
            ]
        )
    
    if border is Border.SOUTH | Border.WEST:
        return Polyline(
            [
                bottomRight,
                bottomLeft,
                topLeft,
            ]
        )
    
    if border is Border.WEST | Border.NORTH:
        return Polyline(
            [
                bottomLeft,
                topLeft,
                topRight,
            ]
        )
    
    if border is Border.NORTH | Border.SOUTH:
        return DisjointLines(
            [
                top,
                bottom,
            ]
        )
    
    if border is Border.WEST | Border.EAST:
        return DisjointLines(
            [
                left,
                right,
            ]
        )
    
    if border is Border.NORTH:
        return top
    
    if border is Border.SOUTH:
        return bottom
    
    if border is Border.WEST:
        return left
    
    if border is Border.EAST:
        return right
    
    return NullPrimitive()