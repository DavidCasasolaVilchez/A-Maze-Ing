from Model.Enums import Cardinal


class Walls():
    def __init__(
            self,
            north: bool,
            east: bool,
            west: bool,
            south: bool
            ):
        self.north: bool = north
        self.east: bool = east
        self.west: bool = west
        self.south: bool = south

    @staticmethod
    def create_full() -> "Walls":
        return Walls(True, True, True, True)

    def change_state(self, dir: Cardinal) -> None:
        if dir == Cardinal.N:
            self.north = not self.north
        elif dir == Cardinal.E:
            self.east = not self.east
        elif dir == Cardinal.W:
            self.west = not self.west
        elif dir == Cardinal.S:
            self.south = not self.south
