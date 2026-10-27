from Model.Exceptions.CreationFailed import CreationFailed
from Utils.Colors import RESET, CYAN, YELLOW, RED, GREEN
from Model.Exceptions.OffTheMap import OffTheMap
from Model.Enums.Cardinal import Cardinal
from Model.Enums.TypeCell import TypeCell
from Utils.ConquerCell import conquer_cell
from Model.Movement import Movement
from Utils.GoBack import go_back
from Model.Cell import Cell
import time


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
        self.refill_map()

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
                map[y].append(Cell.create_base_cell((y, x), None))
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
        y, x = actual
        if direction == Cardinal.N:
            y -= 1
        elif direction == Cardinal.E:
            x += 1
        elif direction == Cardinal.S:
            y += 1
        elif direction == Cardinal.W:
            x -= 1
        if not (0 <= y < self.size[0] and 0 <= x < self.size[1]):
            raise OffTheMap()
        return self.map[y][x]

    def generate42(self) -> None:
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

    def refill_map(self) -> None:
        for y in self.map:
            for x in y:
                x.map = self

    def display_ascii_num(self) -> None:
        for line in self.map:
            for cell in line:
                value: int = 0
                if cell.state.east:
                    value += 1
                if cell.state.south:
                    value += 1
                if cell.state.north:
                    value += 1
                if cell.state.west:
                    value += 1
                print(f"{value}", end="", flush=True)
            print("")

    def display_ascii(self) -> None:
        for y, line in enumerate(self.map):
            top_line = ""
            middle_line = ""
            for cell in line:
                top_line += "+"
                if cell.state.north:
                    top_line += "---"
                else:
                    top_line += "   "
            top_line += "+"
            for x, cell in enumerate(line):
                if cell.state.west:
                    middle_line += "|"
                else:
                    middle_line += " "
                if cell == self.start_cell:
                    middle_line += f"{YELLOW} S {RESET}"
                elif cell == self.end_cell:
                    middle_line += f"{RED} E {RESET}"
                elif cell.type == TypeCell.CLOSED42:
                    middle_line += f"{CYAN} # {RESET}"
                elif cell.view:
                    middle_line += f"{GREEN} 0 {RESET}"
                else:
                    middle_line += "   "
            if line[-1].state.east:
                middle_line += "|"
            else:
                middle_line += " "
            print(top_line)
            time.sleep(0.02)
            print(middle_line)
            time.sleep(0.02)
        bottom_line = ""
        for cell in self.map[-1]:
            bottom_line += "+"
            if cell.state.south:
                bottom_line += "---"
            else:
                bottom_line += "   "
        bottom_line += "+"
        print(bottom_line)

    def all_viewed(self) -> bool:
        for row in self.map:
            for cell in row:
                if not cell.view and cell.type != TypeCell.CLOSED42:
                    return False
        return True

    def convert_to_base(self) -> None:
        stack: list[Movement] = list()
        actual: Cell = self.start_cell
        actual.view = True
        while not self.all_viewed():
            if actual.exist_not_viewed_neighbor():
                aux = conquer_cell(self, stack, actual)
                if aux is not None:
                    actual = aux
                    actual.view = True
                    continue

            if not stack:
                raise CreationFailed()

            aux = go_back(self, stack, actual)
            if aux is not None:
                actual = aux
                actual.view = True
