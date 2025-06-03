import time
import pyautogui
from constants import DEBUG, EMPTY_CELL_COLOR_RGB, LEFT_GUTTER, TOP_GUTTER
from enums import CellState, Numbers
from screenshot_utils import colors_match_with_tolerance


class Cell:
    def __init__(self, x_on_board, y_on_board, width, height, initial_state):
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

    def click(self, board_capture_region):
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
                board_screenshot.save("board_screenshot.png")

            self.evaluate_state(board_screenshot)
        else:
            if DEBUG:
                print(f"Cell at board ({self.x_on_board},{self.y_on_board}) already processed. State: {self.state}")

    def evaluate_state(self, board_screenshot):
        """
        Evaluates the cell's state based on a screenshot of the game board.
        `board_screenshot` is a Pillow Image object.
        """
        # Logical coordinates of the color check spot relative to the board's top-left
        colour_pixel_x = self.x_on_board + self.colour_check_offset[0]
        colour_pixel_y = self.y_on_board + self.colour_check_offset[1]

        # Convert to physical pixel coordinates for the screenshot
        # colour_pixel_x = int(self.x_on_board * SCALING_FACTOR + self.colour_check_offset[0])
        # colour_pixel_y = int(self.y_on_board * SCALING_FACTOR + self.colour_check_offset[1])

        try:
            pixel_color_tuple = board_screenshot.getpixel((colour_pixel_x, colour_pixel_y))
        except IndexError:
            print(f"Error: Failed to get pixel at physical ({colour_pixel_x}, {colour_pixel_y}) "
                  f"from screenshot of size ({board_screenshot.width}, {board_screenshot.height}).")
            return

        actual_rgb = pixel_color_tuple[:3] # Ensure we only use RGB

        if DEBUG:
            print(f"Cell ({self.x_on_board},{self.y_on_board}): Logical check in board ({colour_pixel_x},{colour_pixel_y}), "
                  f"Physical on screenshot ({colour_pixel_x},{colour_pixel_y}), Color: {actual_rgb}")
            # For detailed debugging, save a crop around the pixel:
            crop_radius = 5 # Number of logical pixels around the center point
            s_crop = board_screenshot.crop((colour_pixel_x - crop_radius, colour_pixel_y - crop_radius,
                                            colour_pixel_x + crop_radius, colour_pixel_y + crop_radius))
            s_crop.save(f"debug_crop_cell_board_{self.y_on_board}_{self.x_on_board}_logical_{colour_pixel_y}_{colour_pixel_x}_physical_{colour_pixel_y}_{colour_pixel_x}.png")


        # Check for numbers
        for number_enum in Numbers:
            expected_rgb = number_enum.value # This is already (R,G,B)
            if colors_match_with_tolerance(actual_rgb, expected_rgb): # Adjusted tolerance
                try:
                    self.state = CellState[number_enum.name]
                    if DEBUG: print(f"  => State set to: {self.state}")
                    return
                except KeyError:
                    print(f"Warning: No corresponding CellState found for Numbers.{number_enum.name}")

        # Check for empty cell
        if colors_match_with_tolerance(actual_rgb, EMPTY_CELL_COLOR_RGB):
            self.state = CellState.EMPTY
            if DEBUG: print(f"  => State set to: {self.state} (Empty)")
            return

        # If no specific state is identified, it might still be unclicked (e.g. if click failed)
        # or it could be a color we haven't defined (like a bomb, or a different type of empty square).
        # For now, if it's not a number and not the defined empty color, we'll assume it didn't change
        # or needs further classification.
        if self.state == CellState.UNCLICKED: # If it was unclicked and still not identified
             if DEBUG: print(f"  => Cell ({self.x_on_board},{self.y_on_board}) color {actual_rgb} not recognized as number or empty. Remains UNCLICKED (or needs more color definitions).")
        # else:
            # if DEBUG: print(f"  => Cell ({self.x_on_board},{self.y_on_board}) color {actual_rgb} not recognized. Current state: {self.state}")
