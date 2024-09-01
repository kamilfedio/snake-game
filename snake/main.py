from enum import Enum
import time
from pynput.keyboard import Key, Listener
import os
import threading
from copy import deepcopy
from random import randint

class Directions(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class BoardException(Exception):
    def __init__(self) -> None:
        self.error: str = 'Board was not initialized'
        super().__init__(self.error)

class MoveException(Exception):
    def __init__(self, error: str) -> None:
        super().__init__(error)

class Board:
    def __init__(self, size: int = 10) -> None:
        self.size: int = size
        self.board: None | list[list[int | str]] = None
        self.clear_msg = 'cls' if os.name == 'nt' else 'clear'

    def create(self) -> None:
        if self.board:
            print('Board already exists')
        board: list[list[int | str]] = [['|'] + ['   '] * (self.size) + ['|'] for _ in range(self.size)]
        board.insert(0, [' - '] * (self.size + 1))
        board.append([' - '] * (self.size + 1))
        
        self.board = board.copy()

    def display(self, player_cords: tuple[int, int]) -> None:
        if not self.board:
            raise BoardException
        
        x, y = player_cords

        board = deepcopy(self.board)
        board[y + 1][x + 1] = ' x '

        os.system(self.clear_msg)
        for line in board:
            print(''.join(line))

class Head:
    def __init__(self, x: int = 5, y: int = 5, size: int = 10) -> None:
        self.x: int = x
        self.y: int = y
        self.last_direction: Directions | None = None
        self.colisioned: bool = False
        self.active: bool = True
        self.size: int = 10
        self.points: int = 0

    def check_collision(self) -> bool:
        if self.x >= self.size or self.x < 0 or self.y >= self.size or self.y < 0:
            self.colisioned = True

    def move(self, direction: Directions | None = None) -> None:
        if not direction:
            direction = self.last_direction

        match direction:
            case Directions.LEFT:
                self.x -= 1
            case Directions.RIGHT:
                self.x += 1
            case Directions.UP:
                self.y -= 1
            case Directions.DOWN:
                self.y += 1
            case _:
                raise MoveException('Move didn\'t recognize')
            
        self.last_direction = direction
        self.check_collision()

class Game:
    def __init__(self) -> None:
        self.board: Board = Board()
        self.player: Head = Head()
        self.started: bool = False
        self.stop_time: float = .5

    def show_game(self) -> None:
        while True:
            if self.player.colisioned:
                print('Game ended')
                break

            if self.started:
                time.sleep(self.stop_time)
                if self.player.active:
                    self.player.move()
                self.board.display((self.player.x, self.player.y))
                self.player.active = True

    def run(self) -> None:
        self.board.create()
        listener_thread = threading.Thread(target=self.start_listener)
        game_thread = threading.Thread(target=self.show_game)
        listener_thread.start()
        game_thread.start()

        self.board.display((self.player.x, self.player.y))

    def start_listener(self) -> None:
        with Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def on_key_press(self, key) -> None:
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
    
        if direction and direction != self.player.last_direction:
            if not self.started:
                self.started = True

            self.player.move(direction)
            self.player.active = False


if __name__ == '__main__':
    game = Game()
    game.run()
