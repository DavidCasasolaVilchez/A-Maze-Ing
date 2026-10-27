from typing import TYPE_CHECKING
from Model.Movement import Movement
from Model.Cell import Cell

if TYPE_CHECKING:
    from Model.Panel import Panel


def go_back(panel: "Panel", stack: list[Movement], actual: Cell) -> Cell:
    if len(stack) <= 0:
        return None
    last_move: Movement = stack.pop(len(stack) - 1)
    go_back = last_move.go_back()
    return (
        panel.map[actual.position[0] + go_back[0]]
        [actual.position[1] + go_back[1]]
    )
