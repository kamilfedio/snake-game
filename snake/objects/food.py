from random import randint


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