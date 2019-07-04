from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

# Hide pygame import text
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg


class GameOfLife:
    """Conway's Game of Life. Run by instantiating and calling the `run`
    method.

    1. Set up the grid by clicking and dragging over cells.
    2. Start the evolution by pressing space.

    Args:
        window_size: Width and height of the window.
        grid_size: Number of rows and columns of cells in the window.
        evolution_rate: The number of times per second that the system evolves.
        fps: Maximum frame rate.
    """
    BACKGROUND_COLOUR = (147, 147, 147)
    LIVE_CELL_COLOUR = (255, 255, 0)
    GRID_LINE_COLOUR = (180, 180, 180)

    def __init__(self, window_size: int, grid_size: int, evolution_rate: float,
                 fps: float) -> None:
        pg.init()
        pg.display.set_caption("Conway's Game of Life")
        self.window_size = window_size
        self.grid_size = grid_size
        self.cell_size = window_size // grid_size
        self.fps = fps
        self.evolution_rate = evolution_rate
        self.grid_state = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.surface = pg.display.set_mode((window_size, window_size))
        self.clock = pg.time.Clock()

    def run(self) -> None:
        """Set up the grid by clicking and dragging over cells. Start the
        evolution by pressing space."""
        self.set_up_grid()
        self.main_loop()

    def set_up_grid(self) -> None:
        """Set up the initial grid state by selecting live squares with the
        mouse. Exit the set up by pressing space."""
        update_screen = False
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    done = True

                elif event.type == pg.MOUSEMOTION and pg.mouse.get_focused():
                    mouse_x, mouse_y = event.pos
                    hovered_i, hovered_j = self.position_to_cell(mouse_x, mouse_y)

                    # Can also select cells by dragging over them whilst
                    # holding left mouse button.
                    if pg.mouse.get_pressed() == (1, 0, 0):
                        self.grid_state[hovered_i][hovered_j] = True
                    update_screen = True

                elif event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                    self.grid_state[hovered_i][hovered_j] ^= True
                    update_screen = True

            # We don't need to redraw the screen if nothing has changed.
            if update_screen:
                self.surface.fill(self.BACKGROUND_COLOUR)
                self.fill_live_cells()
                if not self.grid_state[hovered_i][hovered_j]:
                    self.fill_cell(hovered_i, hovered_j)
                self.draw_grid_lines()
                pg.display.update()
                update_screen = False

            self.clock.tick(self.fps)

    def position_to_cell(self, x: int, y: int) -> Tuple[int, int]:
        """Return the cell of the grid that contains the position (`x`, `y`).

        Args:
            x: x coordinate of the position.
            y: y coordinate of the position.

        Returns:
            A cell in the grid.
        """
        return y // self.cell_size, x // self.cell_size

    def draw_grid_lines(self) -> None:
        """Draw the grid lines onto the surface."""
        for i in range(self.grid_size):
            start_pos = (i * self.cell_size - 1, 0)
            end_pos = (i * self.cell_size - 1, self.window_size)
            pg.draw.line(self.surface, self.GRID_LINE_COLOUR, start_pos, end_pos, 2)
        for j in range(self.grid_size):
            start_pos = (0, j * self.cell_size - 1)
            end_pos = (self.window_size, j * self.cell_size - 1)
            pg.draw.line(self.surface, self.GRID_LINE_COLOUR, start_pos, end_pos, 2)

    def fill_live_cells(self) -> None:
        """Draw the live cells in the grid to the surface."""
        for i, row in enumerate(self.grid_state):
            for j, cell_alive in enumerate(row):
                if cell_alive:
                    self.fill_cell(i, j)

    def fill_cell(self, i: int, j: int) -> None:
        """Draw a live cell at position (`i`, `j`).

        Arg:
            i: Row of the cell.
            j: Column of the cell.
        """
        left, top = j * self.cell_size, i * self.cell_size
        rect = [left, top, self.cell_size, self.cell_size]
        pg.draw.rect(self.surface, self.LIVE_CELL_COLOUR, rect)

    def main_loop(self) -> None:
        """Evolve and draw the grid indefinitely until the the window is
        closed or escape is pressed."""
        time_since_last_update = 0
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

            if time_since_last_update > (1 / self.evolution_rate):
                time_since_last_update = 0
                self.evolve_grid()
                self.surface.fill(self.BACKGROUND_COLOUR)
                self.fill_live_cells()
                self.draw_grid_lines()
                pg.display.update()

            time_since_last_update += self.clock.tick(self.fps) / 1000

    def evolve_grid(self) -> None:
        """Evolve the grid by one step.

        Rules for evolution:
            1. Any live cell with fewer than two live neighbours dies, as if by
               underpopulation.
            2. Any live cell with two or three live neighbours lives on to the
               next generation.
            3. Any live cell with more than three live neighbours dies, as if
               by overpopulation.
            4. Any dead cell with exactly three live neighbours becomes a live
               cell, as if by reproduction.
        """
        new_grid_state = []
        for i, row in enumerate(self.grid_state):
            new_row = []
            for j, cell_state in enumerate(row):
                alive = self.live_neighbours(i, j)
                new_state = False
                if (cell_state and 2 <= alive <= 3) or alive == 3:
                    new_state = True
                new_row.append(new_state)
            new_grid_state.append(new_row)

        self.grid_state = new_grid_state

    def live_neighbours(self, i: int, j: int) -> int:
        """Return the number of live cells neighbouring the cell (`i`, `j`)
        in the grid.

        Args:
            i: Row of cell.
            j: Column of cell.

        Returns:
            Number of live neighbours.
        """
        neighbours = self.neighbouring_cells(i, j)
        return sum(self.grid_state[l][m] for l, m in neighbours)

    def neighbouring_cells(self, i: int, j: int) -> List[Tuple[int, int]]:
        """Return the grid positions of the cells neighbouring
        (above/below/diagonal) the cell (`i`, `j`).

        Args:
            i: Row of cell.
            j: Column of cell.

        Returns:
            List of neighbouring cells.
        """
        return [
            (l, m)
            for l in range(i - 1, i + 2) for m in range(j - 1, j + 2)
            if l in range(self.grid_size) and m in range(self.grid_size)
            and (l, m) != (i, j)
        ]


parser = argparse.ArgumentParser(
    description="Conway's Game of Life."
    " Set up the grid by clicking and dragging over cells."
    " Start the evolution by pressing space.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-w', '--window-size', type=int, default=800, metavar='',
                    help='Width and height of the window.')
parser.add_argument('-g', '--grid-size', type=int, default=40, metavar='',
                    help='Number of rows and columns of cells in the grid.')
parser.add_argument('-e', '--evo-rate', type=float, default=8, metavar='',
                    help='Number of times per second that the system evolves.')
parser.add_argument('-f', '--fps', type=float, default=60, metavar='',
                    help='Maximum frame rate.')

if __name__ == '__main__':
    args = parser.parse_args()
    GameOfLife(args.window_size, args.grid_size, args.evo_rate, args.fps).run()
