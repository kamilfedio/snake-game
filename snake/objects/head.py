from utils.constants import Directions
from objects.tail import Tail


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
