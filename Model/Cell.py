from Model.Exceptions.InvalidCell import InvalidCell
from Model.Enums.TypeCell import TypeCell
from Model.Enums.Cardinal import Cardinal
from typing import TYPE_CHECKING
from Model.Walls import Walls
import random

if TYPE_CHECKING:
    from Model.Panel import Panel


class Cell:
    def __init__(
            self,
            position: tuple[int, int],
            type: TypeCell,
            state: Walls,
            map: "Panel",
            view: bool,
            view_from_end: bool
            ):
        self.position: tuple[int, int] = position
        self.type: TypeCell = type
        self.state: Walls = state
        self.view: bool = view
        self.view_from_end: bool = view_from_end
        self.map: "Panel" = map

    @staticmethod
    def create_base_cell(position: tuple[int, int],
                         map: "Panel") -> "Cell":
        return Cell(
            position,
            TypeCell.BASE,
            Walls.create_full(),
            map,
            False,
            False
        )

    def change_type(self, new_type: TypeCell) -> None:
        self.type = new_type

    def break_wall(self, direction: Cardinal) -> None:
        """ This method could raise InvalidCell and OffTheMap Exceptions """
        next: Cell = self.map.get_cell(direction, self.position)
        if next.type == TypeCell.CLOSED42 or self.type == TypeCell.CLOSED42:
            print(f"Next: [{next.position}] Self: [{self.position}]")
            raise InvalidCell()
        self.state.change_state(direction)
        self.map.map[next.position[0]][next.position[1]].state.change_state(
            Cardinal((direction.value + 2) % 4))

    def exist_not_viewed_neighbor(self) -> bool:
        if ((
            (self.position[0] + 1) < self.map.size[0] and
            not self.map.map[self.position[0] + 1][self.position[1]].view and
            not self.map.map[self.position[0] + 1][self.position[1]].type ==
            TypeCell.CLOSED42
        ) or (
            (self.position[0] - 1) >= 0 and
            not self.map.map[self.position[0] - 1][self.position[1]].view and
            not self.map.map[self.position[0] - 1][self.position[1]].type ==
            TypeCell.CLOSED42
        ) or (
            (self.position[1] + 1) < self.map.size[1] and
            not self.map.map[self.position[0]][self.position[1] + 1].view and
            not self.map.map[self.position[0]][self.position[1] + 1].type ==
            TypeCell.CLOSED42
        ) or (
            (self.position[1] - 1) >= 0 and
            not self.map.map[self.position[0]][self.position[1] - 1].view and
            not self.map.map[self.position[0]][self.position[1] - 1].type ==
            TypeCell.CLOSED42
        )):
            return True
        return False

    def return_valid_movements(self) -> list[Cardinal]:
        valid_movements: list[Cardinal] = list()
        if (
            (self.position[0] + 1) < self.map.size[0] and
            not self.map.map[self.position[0] + 1][self.position[1]].type ==
            TypeCell.CLOSED42 and
            self.map.map[self.position[0] + 1][self.position[1]].state.north
        ):
            valid_movements.append(Cardinal.S)
        if (
            (self.position[0] - 1) >= 0 and
            not self.map.map[self.position[0] - 1][self.position[1]].type ==
            TypeCell.CLOSED42 and
            self.map.map[self.position[0] - 1][self.position[1]].state.south
        ):
            valid_movements.append(Cardinal.N)
        if (
            (self.position[1] + 1) < self.map.size[1] and
            not self.map.map[self.position[0]][self.position[1] + 1].type ==
            TypeCell.CLOSED42 and
            self.map.map[self.position[0]][self.position[1] + 1].state.west
        ):
            valid_movements.append(Cardinal.E)
        if (
            (self.position[1] - 1) >= 0 and
            not self.map.map[self.position[0]][self.position[1] - 1].type ==
            TypeCell.CLOSED42 and
            self.map.map[self.position[0]][self.position[1] - 1].state.east
        ):
            valid_movements.append(Cardinal.W)
        return valid_movements

    def break_random_valid_wall(self, seed: str):
        valid_movements: list[Cardinal] = self.return_valid_movements()
        if len(valid_movements) > 0:
            dir: Cardinal = random.Random(seed).choice(valid_movements)
            self.break_wall(dir)
