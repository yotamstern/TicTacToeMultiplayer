import pygame
import os
import logging

# Load images for X and O
letterX = pygame.image.load(os.path.join('res', 'x.webp'))
letterO = pygame.image.load(os.path.join('res', 'elono.png'))

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Grid:
    def __init__(self):
        """
        Initialize the grid for the Tic Tac Toe game.
        Sets up the grid lines, grid data structure, and search directions.
        """
        # Define the grid lines for the board
        self.grid_lines = [((0, 200), (600, 200)),  # first horizontal line
                           ((0, 400), (600, 400)),  # second horizontal line
                           ((200, 0), (200, 600)),  # first vertical line
                           ((400, 0), (400, 600))]  # second vertical line

        # Initialize the grid data structure
        self.grid = [[0 for x in range(3)] for y in range(3)]
        # Search directions for checking win conditions
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1),
                            (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

    def draw(self, surface):
        """
        Draw the grid and the X/O symbols on the surface.

        Args:
            surface: The surface to draw on.
        """
        # Draw the grid lines
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)

        # Draw the X and O symbols
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x * 200, y * 200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x * 200, y * 200))

    def get_cell_value(self, x, y):
        """
        Returns the value of the cell at x,y.

        Args:
            x : The x coordinate of the cell.
            y : The y coordinate of the cell.

        Returns:
            int: The value of the cell.
        """
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        """
        Sets the value of the cell at x,y to value.

        Args:
            x : The x coordinate of the cell.
            y : The y coordinate of the cell.
            value : The value to set (x or o).
        """
        logging.debug(f'Setting cell ({x}, {y}) to {value}')
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        """
        Updates the grid based on the player's mouse click.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            player (str): The current player ('X' or 'O').
        """
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)

    def is_within_bounds(self, x, y):
        """
        Checks if x,y is inside the grid.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            bool: True if within bounds, False otherwise.
        """
        return 0 <= x < 3 and 0 <= y < 3

    def check_grid(self, x, y, player):
        """
        Checks the grid for a win condition starting from (x, y) for the player.

        Args:
            x: The x coordinate of the cell.
            y : The y coordinate of the cell.
            player: The current player (x or o).
        """
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.is_within_bounds(x + dirx, y + diry) and self.get_cell_value(x + dirx, y + diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx + dirx, yy + diry) and self.get_cell_value(xx + dirx, yy + diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    new_dir = self.search_dirs[(index + 4) % 8]
                    if self.is_within_bounds(x + new_dir[0], y + new_dir[1]) \
                            and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            logging.info(f'{player} wins!')
            self.game_over = True
        else:
            self.game_over = self.is_grid_full()

    def is_grid_full(self):
        """
        Check if the grid is full.

        Returns:
            bool: True if the grid is full, False otherwise.
        """
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        logging.info('Grid is full, game over!')
        return True

    def clear_grid(self):
        """
        Clear the grid.
        """
        logging.info('Clearing the grid')
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        """
        Print the grid to the console.
        """
        for row in self.grid:
            logging.debug(row)
