from copy import deepcopy
import os
from utils.custom_errors import BoardException


class Board:
    def __init__(self, size: int = 10) -> None:
        self.size: int = size
        self.board: None | list[list[int | str]] = None
        self.clear_msg = "cls" if os.name == "nt" else "clear"

    def create(self) -> None:
        if self.board:
            print("Board already exists")
        board: list[list[str]] = [
            ["|"] + ["   "] * (self.size) + ["|"] for _ in range(self.size)
        ]
        board.insert(0, [" - "] * (self.size + 1))
        board.append([" - "] * (self.size + 1))

        self.board = board.copy()

    def display(
        self,
        player_cords: tuple[int, int],
        food_coords: tuple[int, int],
        tail_coords: list[tuple[int, int]],
    ) -> None:
        if not self.board:
            raise BoardException

        x, y = player_cords
        f_x, f_y = food_coords

        board = deepcopy(self.board)
        board[f_y + 1][f_x + 1] = " o "
        board[y + 1][x + 1] = " x "
        for tail in tail_coords:
            board[tail[1] + 1][tail[0] + 1] = " # "

        os.system(self.clear_msg)
        for line in board:
            print("".join(line))