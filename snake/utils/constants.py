from dataclasses import dataclass
from enum import Enum, auto


class Directions(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class DisplayType(Enum):
    CMD = auto()


@dataclass
class GameObjects:
    head: str = " x "
    tail: str = " # "
    food: str = " o "
