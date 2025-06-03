import time
from typing import Tuple
import pyautogui
from constants import DEBUG, EMPTY_CELL_COLOR_RGB, LEFT_GUTTER, TOP_GUTTER
from enums import CellState, Numbers
from screenshot_utils import RGBColour, colors_match_with_tolerance
from PIL.Image import Image


CaptureRegion = Tuple[int, int, int, int]

class Cell:
    def __init__(self, x_on_board: int, y_on_board: int, width: int, height: int, initial_state: CellState):
        self.x_on_board = x_on_board  # X position relative to the board's top-left
        self.y_on_board = y_on_board  # Y position relative to the board's top-left

        # Screen coordinates of the cell's top-left
        self.screen_x = LEFT_GUTTER + x_on_board
        self.screen_y = TOP_GUTTER + y_on_board

        self.width = width
        self.height = height
        self.state = initial_state

        # Screen coordinates of the cell's center (for clicking)
        self.screen_centre_coords = (
            self.screen_x + width / 2,
            self.screen_y + height / 2,
        )
        # Offset within the cell to check for its color/number (logical pixels)
        self.colour_check_offset = (11, 12) # Specific offset for color checking

    def click(self, board_capture_region: CaptureRegion) -> None:
        """
        Performs a click on the cell, then captures a screenshot of the board
        and evaluates the cell's new state.
        `board_capture_region` should be (x, y, width, height) for the game board.
        """
        if self.state == CellState.UNCLICKED:
            pyautogui.moveTo(self.screen_centre_coords[0], self.screen_centre_coords[1])
            pyautogui.click(self.screen_centre_coords[0], self.screen_centre_coords[1])

            time.sleep(0.15) # Crucial: Give the game UI time to update after the click

            # Capture a screenshot of the specified board region
            board_screenshot = pyautogui.screenshot(region=board_capture_region)

            if DEBUG:
                board_screenshot.save("./images/board_screenshot.png")

            self.state = self.evaluate_state(board_screenshot)
            print(f"State of cell ({self.x_on_board / self.width}, {self.y_on_board / self.height}) set to: {self.state}")
        else:
            if DEBUG:
                print(f"Cell at board ({self.x_on_board},{self.y_on_board}) already processed. State: {self.state}")

    def evaluate_state(self, board_screenshot: Image) -> CellState:
        """
        Evaluates the cell's state based on a screenshot of the game board.
        `board_screenshot` is a Pillow Image object.
        """
        # Logical coordinates of the color check spot relative to the board's top-left
        colour_pixel_x = self.x_on_board + self.colour_check_offset[0]
        colour_pixel_y = self.y_on_board + self.colour_check_offset[1]

        # Convert to physical pixel coordinates for the screenshot
        # This doesn't appear to be needed, keeping in case something changes
        # colour_pixel_x = int(self.x_on_board * SCALING_FACTOR + self.colour_check_offset[0])
        # colour_pixel_y = int(self.y_on_board * SCALING_FACTOR + self.colour_check_offset[1])

        try:
            pixel_color_tuple = board_screenshot.getpixel((colour_pixel_x, colour_pixel_y))
        except IndexError:
            print(f"Error: Failed to get pixel at physical ({colour_pixel_x}, {colour_pixel_y}) "
                  f"from screenshot of size ({board_screenshot.width}, {board_screenshot.height}).")
            return CellState.UNKNOWN

        if type(pixel_color_tuple) == tuple:
            actual_rgb: RGBColour = (pixel_color_tuple[0], pixel_color_tuple[1], pixel_color_tuple[2]) # Ensure we only use RGB, dont use : operator as it gives indeterminate length
        else:
            raise Exception(f"Expected tuple from `getpixel` call but got: {type(pixel_color_tuple)}")

        if DEBUG:
            print(f"Cell ({self.x_on_board},{self.y_on_board}): Logical check in board ({colour_pixel_x},{colour_pixel_y}), "
                  f"Physical on screenshot ({colour_pixel_x},{colour_pixel_y}), Color: {actual_rgb}")
            # For detailed debugging, save a crop around the pixel:
            crop_radius = 5 # Number of logical pixels around the center point
            # TODO: The crop is SLIGHTLY wrong. This could be due to the gutters on the game board
            s_crop = board_screenshot.crop((colour_pixel_x - crop_radius, colour_pixel_y - crop_radius,
                                            colour_pixel_x + crop_radius, colour_pixel_y + crop_radius))
            s_crop.save(f"./images/debug_crop_cell_board_{self.y_on_board}_{self.x_on_board}_logical_{colour_pixel_y}_{colour_pixel_x}_physical_{colour_pixel_y}_{colour_pixel_x}.png")


        # Check for numbers
        for number_enum in Numbers:
            expected_rgb = number_enum.value # This is already (R,G,B)
            if colors_match_with_tolerance(actual_rgb, expected_rgb): # Adjusted tolerance
                try:
                    if DEBUG: print(f"  => State set to: {self.state}")
                    return CellState[number_enum.name]
                except KeyError:
                    print(f"Warning: No corresponding CellState found for Numbers.{number_enum.name}")
                    return CellState.UNKNOWN

        # Check for empty cell
        if colors_match_with_tolerance(actual_rgb, EMPTY_CELL_COLOR_RGB):
            if DEBUG: print(f"  => Found state: {CellState.EMPTY} (Empty)")
            return CellState.EMPTY

        # We have not identified the state
        return CellState.UNKNOWN
