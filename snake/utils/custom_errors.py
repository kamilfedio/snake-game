class BoardException(Exception):
    def __init__(self) -> None:
        self.error: str = "Board was not initialized"
        super().__init__(self.error)


class DisplayException(Exception):
    def __init__(self, error: str) -> None:
        super().__init__(error)
