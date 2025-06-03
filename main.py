import time

from Board import Board
from enums import CellState

DEBUG = False

# --- Configuration Constants ---
# Adjust these based on your game's layout and screen resolution

# SCALING_FACTOR: 2 for Retina/HiDPI displays (e.g., macOS), 1 for standard displays.
# This is used because pyautogui.screenshot() captures physical pixels.

if __name__ == "__main__":
    game_board = Board(rows=9, cols=9)
    print(f"Board initialized. Capture region: {game_board.capture_region}")
    print("Ensure your Minesweeper game window is visible and positioned correctly.")
    print("Pausing for 3 seconds before starting...")
    time.sleep(3)

    # We don't care what cell we start the game on currently
    game_board.click_random_cell()

    print("\nScript finished.")


def debug():
    # Example: Click and evaluate a few cells
    cells_to_test = []

    for r, c in cells_to_test:
        if 0 <= r < game_board.rows and 0 <= c < game_board.cols: # r is row index, c is col index
            cell = game_board.board_array[r][c]
            print(f"\nTesting cell at board coordinates ({r},{c}). Current state: {cell.state}")
            cell.click(game_board.capture_region) # Pass the board's capture region
            print(f"After click & eval, cell ({r},{c}) state: {cell.state}")
            if DEBUG: time.sleep(0.5) # Pause to observe if DEBUG is on
        else:
            print(f"Test coordinates ({r},{c}) are out of board bounds.")

    # To click and evaluate all cells (for testing purposes):
    # print("\n--- Clicking all cells (for testing evaluation logic) ---")
    # for i, row_of_cells in enumerate(game_board.board_array):
    #     for j, cell in enumerate(row_of_cells):
    #         if cell.state == CellState.UNCLICKED: # Only click if not already processed
    #             print(f"\nProcessing cell ({i},{j})")
    #             cell.click(game_board.capture_region)
    #             print(f"Cell ({i},{j}) final state: {cell.state}")
    #         else:
    #             print(f"Skipping already processed cell ({i},{j}), state: {cell.state}")
