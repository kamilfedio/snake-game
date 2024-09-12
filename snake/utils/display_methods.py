from abc import ABC, abstractmethod
import os

from utils.constants import GameObjects
from utils.custom_errors import BoardException


class DisplayStrategy(ABC):
    @abstractmethod
    def display(
        self,
        board: list[list[int]],
        player_cords: tuple[int, int],
        food_cords: tuple[int, int],
        tail_cords: list[tuple[int, int]],
        clear_msg: str,
    ) -> None:
        pass


class CmdDisplayStrategy(DisplayStrategy):
    def display(
        self,
        board: list[list[int]],
        player_cords: tuple[int, int],
        food_cords: tuple[int, int],
        tail_cords: list[tuple[int, int]],
        clear_msg: str,
    ) -> None:
        if not board:
            raise BoardException
        
        x, y = player_cords
        f_x, f_y = food_cords

        board[f_y + 1][f_x + 1] = GameObjects.food
        board[y + 1][x + 1] = GameObjects.head
        for tail in tail_cords:
            board[tail[1] + 1][tail[0] + 1] = GameObjects.tail

        os.system(clear_msg)
        for line in board:
            print("".join(line))
