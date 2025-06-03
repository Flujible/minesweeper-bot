import random
from typing import List
from Cell import CaptureRegion, Cell
from constants import LEFT_GUTTER, TOP_GUTTER
from enums import CellState

class Board:
    square_width: int = 16
    square_height: int = 16


    def __init__(self, rows: int, cols: int):
        self.rows: int = rows
        self.cols: int = cols
        self.board_array: List[List[Cell]] = []

        # Logical width and height of the game board area
        self.logical_width: int = cols * self.square_width
        self.logical_height: int = rows * self.square_height

        # The region on the screen where the game board is located
        self.capture_region: CaptureRegion = (LEFT_GUTTER, TOP_GUTTER, self.logical_width, self.logical_height)

        for i in range(rows):
            row_cells: List[Cell] = []
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

    def click_random_cell(self) -> None:
        self.board_array[random.randint(0, self.rows - 1)][random.randint(0, self.cols - 1)].click(self.capture_region)
