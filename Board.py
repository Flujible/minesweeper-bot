import random
from Cell import Cell
from constants import LEFT_GUTTER, TOP_GUTTER
from enums import CellState

class Board:
    square_width = 16
    square_height = 16


    def __init__(self, rows, cols): # Removed gutters from here, they are global
        self.rows = rows
        self.cols = cols
        self.board_array = [] # Renamed to avoid confusion with 'board' instance name

        # Logical width and height of the game board area
        self.logical_width = cols * self.square_width
        self.logical_height = rows * self.square_height

        # The region on the screen where the game board is located
        self.capture_region = (LEFT_GUTTER, TOP_GUTTER, self.logical_width, self.logical_height)

        for i in range(rows):
            row_cells = []
            for j in range(cols):
                row_cells.append(
                    Cell(
                        x_on_board=j * self.square_width,
                        y_on_board=i * self.square_height,
                        width=self.square_width,
                        height=self.square_height,
                        initial_state=CellState.UNCLICKED,
                    )
                )
            self.board_array.append(row_cells)

    def click_random_cell(self):
        self.board_array[random.randint(0, self.rows - 1)][random.randint(0, self.cols - 1)].click(self.capture_region)
