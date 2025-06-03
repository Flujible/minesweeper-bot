from enum import Enum


class CellState(Enum):
    UNKNOWN = 0
    UNCLICKED = 1
    EMPTY = 2
    FLAGGED = 3 # Not used in current logic but good to have
    ONE = 4
    TWO = 5
    THREE = 6
    # Add more numbers if your game has them (FOUR, FIVE, etc.)

class Numbers(Enum):
    # Storing as RGB tuples
    ONE = (49, 49, 231)
    TWO = (69, 129, 50)
    THREE = (223, 85, 73)
    # Add more numbers with their RGB values if needed
