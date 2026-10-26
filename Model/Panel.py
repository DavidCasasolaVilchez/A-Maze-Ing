from Model.Enums import Cardinal, TypeCell
from Model.Exceptions import OffTheMap
from Model import Cell
from Utils.Colors import RED, RESET, CYAN, BLUE, GREEN


class Panel():
    def __init__(
            self,
            map: list[list[Cell]],
            size: tuple[int, int],
            is_perfect: bool,
            start_cell: Cell,
            end_cell: Cell,
            seed: int,
            ):
        self.is_perfect: bool = is_perfect
        self.start_cell: Cell = start_cell
        self.size: tuple[int, int] = size
        self.map: list[list[Cell]] = map
        self.end_cell: Cell = end_cell
        self.seed: int = seed

    @staticmethod
    def create_base(
        size: tuple[int, int],
        is_perfect: bool,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int
    ) -> "Panel":
        map: list[list[Cell]] = list()
        for y in range(0, size[0]):
            map.append(list())
            for x in range(0, size[1]):
                map[y].append(Cell.create_base_cell((y, x), Panel))
        map[entry[0]][entry[1]].change_type(TypeCell.START)
        map[exit[0]][exit[1]].change_type(TypeCell.END)
        return Panel(
            map,
            size,
            is_perfect,
            map[entry[0]][entry[1]],
            map[exit[0]][exit[1]],
            seed
        )

    def get_cell(self, direction: Cardinal, actual: tuple[int, int]) -> Cell:
        if direction == Cardinal.N:
            if (actual[0] + 1) <= self.size[0]:
                return map[actual[0] + 1][actual[1]]
            else:
                raise OffTheMap()
        elif direction == Cardinal.E:
            if (actual[1] + 1) >= self.size[1]:
                return map[actual[0]][actual[1] + 1]
            else:
                raise OffTheMap()
        elif direction == Cardinal.S:
            if (actual[0] - 1) >= self.size[0]:
                return map[actual[0] - 1][actual[1]]
            else:
                raise OffTheMap()
        elif direction == Cardinal.W:
            if (actual[1] - 1) >= self.size[1]:
                return map[actual[0]][actual[1] - 1]
            else:
                raise OffTheMap()

    def generate42(self):
        middle: tuple[int, int] = (
            int(self.size[0] / 2), int(self.size[1] / 2))
        self.map[middle[0]][middle[1] + 1].type = TypeCell.CLOSED42
        self.map[middle[0]][middle[1] + 2].type = TypeCell.CLOSED42
        self.map[middle[0]][middle[1] + 3].type = TypeCell.CLOSED42
        self.map[middle[0]][middle[1] - 1].type = TypeCell.CLOSED42
        self.map[middle[0]][middle[1] - 2].type = TypeCell.CLOSED42
        self.map[middle[0]][middle[1] - 3].type = TypeCell.CLOSED42

        self.map[middle[0] + 1][middle[1] + 1].type = TypeCell.CLOSED42
        self.map[middle[0] + 1][middle[1] - 1].type = TypeCell.CLOSED42

        self.map[middle[0] + 2][middle[1] + 1].type = TypeCell.CLOSED42
        self.map[middle[0] + 2][middle[1] + 2].type = TypeCell.CLOSED42
        self.map[middle[0] + 2][middle[1] + 3].type = TypeCell.CLOSED42
        self.map[middle[0] + 2][middle[1] - 1].type = TypeCell.CLOSED42

        self.map[middle[0] - 1][middle[1] + 3].type = TypeCell.CLOSED42
        self.map[middle[0] - 1][middle[1] - 3].type = TypeCell.CLOSED42

        self.map[middle[0] - 2][middle[1] + 1].type = TypeCell.CLOSED42
        self.map[middle[0] - 2][middle[1] + 2].type = TypeCell.CLOSED42
        self.map[middle[0] - 2][middle[1] + 3].type = TypeCell.CLOSED42
        self.map[middle[0] - 2][middle[1] - 3].type = TypeCell.CLOSED42

    def display_ascii(self):
        for line in self.map:
            for cell in line:
                if cell.type.value == 3:
                    print(f"{BLUE}{cell.type.value}{RESET}",
                          end="", flush=True)
                elif cell.type.value == 2:
                    print(f"{RED}{cell.type.value}{RESET}",
                          end="", flush=True)
                elif cell.type.value == 1:
                    print(f"{GREEN}{cell.type.value}{RESET}",
                          end="", flush=True)
                elif cell.type.value == 1:
                    print(f"{CYAN}{cell.type.value}{RESET}",
                          end="", flush=True)
                elif cell.type.value == 0:
                    print(f"{cell.type.value}",
                          end="", flush=True)
            print("")
