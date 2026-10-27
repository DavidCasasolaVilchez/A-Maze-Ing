from Model.Enums.Cardinal import Cardinal


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
            self.north = False
        elif dir == Cardinal.E:
            self.east = False
        elif dir == Cardinal.W:
            self.west = False
        elif dir == Cardinal.S:
            self.south = False
