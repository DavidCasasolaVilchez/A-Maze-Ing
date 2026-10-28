from Model import Panel
from Model.Cell import Cell
from Model.Enums.Cardinal import Cardinal


def start_search(panel: Panel) -> str:
    start_steps: list[str] = [""]
    end_steps: list[str] = [""]
    start_cells: list[Cell] = [panel.start_cell]
    end_cells: list[Cell] = [panel.end_cell]
    solution: str = "None"

    for i in range(panel.size[0]):
        for j in range(panel.size[1]):
            panel.map[i][j].view = False
    while not exist_equal_cells(start_cells, end_cells):
        for i in range(len(start_steps)):
            move(start_steps, start_cells, i)
        for i in range(len(end_steps)):
            move(end_steps, end_cells, i)
    for i, s_cell in enumerate(start_cells):
        for j, e_cell in enumerate(end_cells):
            if s_cell.position == e_cell.position:
                solution = start_steps[i] + invert(end_steps[j])
    return solution


def invert(s: str) -> str:
    opposite: dict[str, str] = {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E'
    }
    return "".join(opposite[c] for c in reversed(s))


def move(steps: list[str], cells: list[Cell], index: int) -> bool:
    map: Panel = cells[index].map
    directions: list[tuple[Cardinal, str, bool]] = [
        (Cardinal.N, "N", cells[index].state.north
         or not map.get_cell(Cardinal.N, cells[index].position).view), #TODO: add code to take care about the solution is not jumped becouse view says not
        (Cardinal.E, "E", cells[index].state.east
         or not map.get_cell(Cardinal.E, cells[index].position).view),
        (Cardinal.S, "S", cells[index].state.south
         or not map.get_cell(Cardinal.S, cells[index].position).view),
        (Cardinal.W, "W", cells[index].state.west
         or not map.get_cell(Cardinal.W, cells[index].position).view),
    ]
    available: list[tuple[Cardinal, str]] = [
        (direction, name)
        for direction, name, is_wall in directions if not is_wall
    ]
    if not available:
        # steps.pop(index)
        # cells.pop(index)
        return False

    branches: list[tuple[str, Cell]] = [
        (steps[index] + name, map.get_cell(direction, cells[index].position))
        for direction, name in available
    ]
    steps[index] = branches[0][0]
    cells[index] = branches[0][1]
    for branch_steps, branch_cell in branches[1:]:
        steps.append(branch_steps)
        cells.append(branch_cell)
    return True


def exist_equal_cells(s_cells: list[Cell], e_cells: list[Cell]) -> bool:
    for i in range(len(s_cells)):
        for j in range(len(e_cells)):
            if (e_cells[j] == s_cells[i]):
                return True
    for i in range(len(e_cells)):
        for j in range(len(s_cells)):
            if (e_cells[i] == s_cells[j]):
                return True
    return False
