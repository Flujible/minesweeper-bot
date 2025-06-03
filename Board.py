import random
from typing import List
import pyautogui # Added for screenshot capability
from Cell import CaptureRegion, Cell
from constants import DEBUG, LEFT_GUTTER, TOP_GUTTER
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

        for i in range(self.rows):
            row_cells: List[Cell] = []
            for j in range(self.cols):
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

    def evaluate_board(self):
        """
        Takes a screenshot of the entire board and evaluates the state of each cell
        based on that single screenshot.
        """
        print("Evaluating board...")
        board_screenshot = pyautogui.screenshot(region=self.capture_region)
        if DEBUG:
            board_screenshot.save("full_board_evaluation_screenshot.png")

        for i, row_of_cells in enumerate(self.board_array):
            for j, cell in enumerate(row_of_cells):
                # The cell's evaluate_state method uses its board-relative coordinates
                # to find its color within the provided board_screenshot.
                new_state = cell.evaluate_state(board_screenshot)
                cell.state = new_state
                if DEBUG:
                    print(f"Evaluated Cell ({i},{j}): State set to {new_state}")
        print("Board evaluation complete.")
