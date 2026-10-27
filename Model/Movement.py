from Model.Enums.Cardinal import Cardinal


class Movement:
    def __init__(self, move: tuple[int, int], direction: Cardinal) -> None:
        self.move: tuple[int, int] = move
        self.direction: Cardinal = direction

    def go_back(self) -> tuple[int, int]:
        return (self.move[0] * - 1, self.move[1] * - 1)
