from enum import Enum
import time
from typing import Any
from pynput.keyboard import Key, Listener
import os
import threading
from copy import deepcopy
from random import randint


class Directions(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class BoardException(Exception):
    def __init__(self) -> None:
        self.error: str = "Board was not initialized"
        super().__init__(self.error)


class MoveException(Exception):
    def __init__(self, error: str) -> None:
        super().__init__(error)


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


class Food:
    def __init__(self, size: int, blocked_coords: list[tuple[int, int]]) -> None:
        self.blocked_coords: list[tuple[int, int]] = blocked_coords
        self.size: int = size
        self.coords: tuple[int, int] = self.generate_coords()

    def generate_coords(self) -> tuple[int, int]:
        coords: tuple[int, int] = randint(0, self.size - 1), randint(0, self.size - 1)
        while coords in self.blocked_coords:
            coords = randint(0, self.size - 1), randint(0, self.size - 1)
        return coords


class Tail:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.last_x: int = x
        self.last_y: int = y

    def move(self, new_coords: tuple[int, int]) -> None:
        self.last_x, self.last_y = self.x, self.y
        self.x, self.y = new_coords


class Head:
    def __init__(self, x: int = 5, y: int = 5, size: int = 10) -> None:
        self.x: int = x
        self.y: int = y
        self.tail: list[Tail] = [Tail(x=4, y=5)]
        self.last_direction: Directions | None = None
        self.colisioned: bool = False
        self.active: bool = True
        self.size: int = 10
        self.points: int = 0

    def check_collision(self) -> None:
        if self.x >= self.size or self.x < 0 or self.y >= self.size or self.y < 0:
            self.colisioned = True

        if (self.x, self.y) in self.get_tail_coords():
            self.colisioned = True

    def get_tail_coords(self) -> list[tuple[int, int]]:
        coords: list[tuple[int, int]] = []
        for cord in self.tail:
            coords.append((cord.x, cord.y))

        return coords

    def get_tail_long(self) -> int:
        return len(self.tail)

    def add_tail(self) -> None:
        last_tail: Tail = self.tail[-1]
        new_tail: Tail = Tail(last_tail.last_x, last_tail.last_y)
        self.tail.append(new_tail)

    def move(self, direction: Directions | None = None) -> None:
        prev_x, prev_y = self.x, self.y
        if not direction:
            direction: Directions = self.last_direction

        if direction == Directions.LEFT:
            self.x -= 1
        elif direction == Directions.RIGHT:
            self.x += 1
        elif direction == Directions.UP:
            self.y -= 1
        elif direction == Directions.DOWN:
            self.y += 1

        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i].move((self.tail[i - 1].x, self.tail[i - 1].y))

        self.tail[0].move((prev_x, prev_y))

        self.last_direction = direction
        self.check_collision()


class Game:
    def __init__(self) -> None:
        self.board: Board = Board()
        self.player: Head = Head()
        self.food = Food(
            blocked_coords=[(self.player.x, self.player.y)]
            + self.player.get_tail_coords(),
            size=self.board.size,
        )

        self.started: bool = False
        self.stop_time: float = 0.8

    def show_game(self) -> None:
        while True:
            if self.player.colisioned:
                print(f"Player points: {self.player.points}")
                print("Game ended")
                os._exit(0)

            if self.started:
                print(f"Player points: {self.player.points}")
                time.sleep(self.stop_time)
                if self.player.active:
                    self.player.move()

                self.player.active = True

                if (self.player.x, self.player.y) == self.food.coords:
                    self.player.points += 1
                    self.food = Food(
                        blocked_coords=[(self.player.x, self.player.y)]
                        + self.player.get_tail_coords(),
                        size=self.board.size,
                    )

                    score = self.player.points
                    if score <= 4:
                        pass
                    elif score > 4:
                        self.stop_time = 0.6
                    elif score > 10:
                        self.stop_time = 0.5
                    elif score > 15:
                        self.stop_time = 0.4
                    elif score > 20:
                        self.stop_time = 0.3
                    else:
                        self.stop_time = 0.2

                    if self.player.get_tail_long() == 99:
                        print(f"Player points: {self.player.points}")
                        print("Game ended - You won")
                        os._exit(0)

                    self.player.add_tail()

                self.board.display(
                    (self.player.x, self.player.y),
                    self.food.coords,
                    self.player.get_tail_coords(),
                )

    def run(self) -> None:
        self.board.create()
        listener_thread = threading.Thread(target=self.start_listener)
        game_thread = threading.Thread(target=self.show_game)
        listener_thread.start()
        game_thread.start()

        self.board.display(
            (self.player.x, self.player.y),
            self.food.coords,
            self.player.get_tail_coords(),
        )

    def start_listener(self) -> None:
        with Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def on_key_press(self, key) -> None:
        def _check_behind(last_dir: Directions | None, cur_dir: Directions) -> bool:
            if not last_dir:
                return True

            if (
                (last_dir == Directions.LEFT and cur_dir == Directions.RIGHT)
                or (last_dir == Directions.RIGHT and cur_dir == Directions.LEFT)
                or (last_dir == Directions.UP and cur_dir == Directions.DOWN)
                or (last_dir == Directions.DOWN and cur_dir == Directions.UP)
            ):
                return False

            return True

        if not self.player.active:
            return

        direction: None | Directions = None
        match key:
            case Key.left:
                direction = Directions.LEFT
            case Key.right:
                direction = Directions.RIGHT
            case Key.up:
                direction = Directions.UP
            case Key.down:
                direction = Directions.DOWN
            case _:
                pass

        if (
            direction
            and direction != self.player.last_direction
            and _check_behind(self.player.last_direction, direction)
        ):
            if not self.started:
                self.started = True

            self.player.move(direction)
            self.player.active = False


if __name__ == "__main__":
    game = Game()
    game.run()
