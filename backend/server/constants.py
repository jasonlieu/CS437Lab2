from enum import Enum

class Directions(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    TURN_LEFT = "turnleft"
    TURN_RIGHT = "turnright"
    LEAN_RIGHT = "Lean-R"
    LEAN_LEFT = "Lean-L"

SYMBOLS = [".", "█", "s", "+"]

class Orientation(Enum):
    N = (0, 1)
    S = (0, -1)
    W = (-1, 0)
    E = (1, 0)
    NW = (-1, 1)
    NE = (1, 1)
    SW = (-1, -1)
    SE = (1, -1)

    @staticmethod
    def is_cardinal(direction):
        return direction == Orientation.N.value or direction == Orientation.S.value or direction == Orientation.W.value or direction == Orientation.E.value