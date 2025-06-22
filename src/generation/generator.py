from numpy import random
from cell import Cell
from direction import Direction

class Generator:

    @staticmethod
    def generateCells(rows: int, cols: int):
        return [Cell((i, j), Direction.NONE) for i in range(rows) for j in range(cols)]
    
    @staticmethod
    def getNeighbouringCells(current: "Cell", rows: int, cols: int, cells: list["Cell"]):
        cordNeighbours = current.neighbouringCoordinates
        qualifiedNeighbours = set([neighbour for neighbour in cordNeighbours if 0 <= neighbour[0] < rows and 0 <= neighbour[1] < cols])
        neighbours = [neighbour for neighbour in cells if neighbour.coordinate in qualifiedNeighbours]
        return neighbours
    
    @staticmethod
    def updateMaze(current: "Cell", maze: set["Cell"], cells: list["Cell"]):
        maze.add(current)
        cells.remove(current)
    
    @staticmethod
    def generateMaze(rows: int, cols: int):
        '''
        Wilson's Algorithm

        1) Generate an empty maze
        2) Randomly select an unvisited cell to be part of the maze
        3) While not all cells are visited
            Randomly select a current cell and add it to path
            
            While path not connected to maze
                Select an adjacent and set it as the new current

                if there is a loop in path
                    erase loop
                else
                    add current cell to path
        '''
        # Generate maze
        maze = set()

        # Create a path
        path = []

        # Generate cells
        cells = Generator.generateCells(rows, cols)

        # Select a random cell and add it to the maze
        selected = random.choice(cells)
        maze.add(selected)
        cells.remove(selected)

        while len(cells) != 0:
            # Select a random cell
            current = random.choice(cells)

            # Add new cell to the path
            path.append(current)

            # Loop Erase Random Walk
            while current not in maze:
                # Randomly select a neighbouring cell
                neighbours = Generator.getNeighbouringCells(current, rows, cols, cells)
                current = random.choice(neighbours)

                # Update cell direction
                ...

                if current in set(path):
                    # Remove the loop
                    index = path.index(current)
                    path = path[:index + 1]
                else:
                    # Add cell to path
                    path.append(current)
        
            # Add the path to the maze
            [Generator.updateMaze(cell, maze, cells) for cell in path]

            # Reset the path
            path = []
    
        return maze