# Conway's Game of Life
![Conway's Game of Life](screenshot.png)

**[From Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)**
> _The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970._

> **Rules**

> The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:
> 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
> 2. Any live cell with two or three live neighbours lives on to the next generation.
> 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
> 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


## Prerequisites

Python 3.7+ is required. Check your python version with
```
python --version
```

## Installation

Install pygame with
```
pip install pygame
```

## Usage

Run the Game of Life with
```
python gameoflife.py
```

For some configuration options, check the help with
```
python gameoflife.py --help
```
