from typing import Tuple


RGBColour = Tuple[int, int, int]

def colors_match_with_tolerance(color1_rgb: RGBColour, color2_rgb: RGBColour, tolerance=50) -> bool:
    """Checks if two RGB colors match within a given tolerance."""
    if not color1_rgb or not color2_rgb or len(color1_rgb) < 3 or len(color2_rgb) < 3:
        return False
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1_rgb[:3], color2_rgb[:3]))
