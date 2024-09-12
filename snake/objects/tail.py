class Tail:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.last_x: int = x
        self.last_y: int = y

    def move(self, new_coords: tuple[int, int]) -> None:
        self.last_x, self.last_y = self.x, self.y
        self.x, self.y = new_coords
