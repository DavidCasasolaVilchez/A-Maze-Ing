from Model.Exceptions import InvalidCell
from Model.Enums import TypeCell
from Model.Enums import Cardinal
from Model.Walls import Walls
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Model.Panel import Panel


class Cell():
    def __init__(
            self,
            position: tuple[int, int],
            type: TypeCell,
            state: Walls,
            map: "Panel | None",
            view: bool
            ):
        self.position: tuple[int, int] = position
        self.type: TypeCell = type
        self.state: Walls = state
        self.view: bool = view
        self.map: Panel = map

    @staticmethod
    def create_base_cell(position: tuple[int, int],
                         map: "Panel | None") -> "Cell":
        return Cell(
            position,
            TypeCell.BASE,
            Walls.create_full(),
            map,
            False
        )

    def change_type(self, new_type: TypeCell) -> None:
        self.type = new_type

    def break_wall(self, direction: Cardinal) -> None:
        """ This method could raise InvalidCell and OffTheMap Exceptions """
        next: Cell = self.map.get_cell(direction, self.position)
        if next.type == TypeCell.CLOSED42 or self.type == TypeCell.CLOSED42:
            raise InvalidCell()
        self.state.change_state(direction)
        next.state.change_state((direction + 2) % 4)
