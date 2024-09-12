from copy import deepcopy
import os
from utils.display_methods import DisplayStrategy, CmdDisplayStrategy
from utils.custom_errors import DisplayException
from utils.constants import DisplayType


class Board:
    def __init__(self, size: int = 10) -> None:
        self.size: int = size
        self.board: None | list[list[int | str]] = None
        self.clear_msg: str = "cls" if os.name == "nt" else "clear"
        self.display_strategy: DisplayStrategy | None = None

    def create(self, display_type: DisplayType = DisplayType.CMD) -> None:
        if self.board:
            print("Board already exists")
        board: list[list[str]] = [
            ["|"] + ["   "] * (self.size) + ["|"] for _ in range(self.size)
        ]
        board.insert(0, [" - "] * (self.size + 1))
        board.append([" - "] * (self.size + 1))

        self.board = board.copy()
        match display_type:
            case DisplayType.CMD:
                self.display_strategy = CmdDisplayStrategy()

    def display(
        self,
        player_cords: tuple[int, int],
        food_cords: tuple[int, int],
        tail_cords: list[tuple[int, int]],
    ) -> None:
        if not self.display_strategy:
            raise DisplayException("Display type was not initialized")
        self.display_strategy.display(
            deepcopy(self.board), player_cords, food_cords, tail_cords, self.clear_msg
        )
