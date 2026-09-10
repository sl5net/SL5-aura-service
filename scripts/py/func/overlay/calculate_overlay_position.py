from typing import Tuple


def calculate_overlay_position(
    mon_x: int,
    mon_y: int,
    mon_w: int,
    mon_h: int,
    size: int,
    position_code: str = "tr",
    margin: int = 16,
) -> Tuple[int, int]:
    code = position_code.lower()
    if code == "bl":
        return mon_x + margin, mon_y + mon_h - size - margin
    return mon_x + mon_w - size - margin, mon_y + margin
