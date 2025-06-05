# Maze Solver

This project aims to create an automated maze solver. Ideally, it reads in the file describing a maze and then solves the maze using Dijkstra's Algorithm. Finally, it will output the solution in svg file. 

## Installation and Running the Code

Set up the python virtual environment.
```
python -m venv .venv
```

Start the virtual environment.
```
.venv\Scripts\activate
```

Run the code. You may then view the results in `maze.svg` under the `static` folder. 
```
python -m src.main
```

After you are done, you may deactivate your virtual environment. 
```
deactivate
```

## Edit the Code

Follow the instructions under [Installation and Running the Code](#installation-and-running-the-code) but stop before running it. 

Edit the code and install any dependencies you need. Either update pyproject.toml or create or update the requirements.txt.

Then, after you are done, deactivate the python virtual environment. 
```
deactivate
```

## Acknowledgement

I would like to express my thanks to the follownig resources:
- [Build a Maze Solver in Python Using Graphs](https://realpython.com/python-maze-solver/): For providing inspiration and guidance for this project
- [How Dijkstra's Algorithm Works](https://www.youtube.com/watch?v=EFg3u_E6eHU): For helping me to understand Dijkstra's Algorithm
