from typing import TYPE_CHECKING
from Model.Exceptions.InvalidCell import InvalidCell
from Model.Cell import Cell
from Model.Enums.Cardinal import Cardinal
from Model.Enums.TypeCell import TypeCell
from Model.Movement import Movement
from random import choice

if TYPE_CHECKING:
    from Model.Panel import Panel


def conquer_cell(
        panel: "Panel", stack: list[Movement],
        actual: Cell) -> Cell:
    values: list[tuple[tuple[int, int], Cardinal]] = [
        ((-1, 0), Cardinal.N),
        ((0, 1), Cardinal.E),
        ((1, 0), Cardinal.S),
        ((0, -1), Cardinal.W),
    ]

    available: list[tuple[tuple[int, int], Cardinal]] = []
    for aux_mv, direction in values:
        y = actual.position[0] + aux_mv[0]
        x = actual.position[1] + aux_mv[1]
        if not (0 <= y < panel.size[0] and 0 <= x < panel.size[1]):
            continue
        neighbor = panel.map[y][x]
        if neighbor.view or neighbor.type == TypeCell.CLOSED42:
            continue
        available.append((aux_mv, direction))

    if not available:
        return None

    aux_mv, direction = choice(available)
    try:
        actual.break_wall(direction)
    except InvalidCell:
        return None

    stack.append(Movement(aux_mv, direction))
    return panel.map[
        actual.position[0] + aux_mv[0]][actual.position[1] + aux_mv[1]]
