import time
from pynput.keyboard import Key, Listener
import os
import threading

from utils.constants import Directions
from objects.board import Board
from objects.food import Food
from objects.head import Head


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
