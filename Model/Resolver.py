from Model import Panel
from Model.Cell import Cell
from Model.Enums.Cardinal import Cardinal


def start_search(panel: Panel) -> str:
    start_steps: list[str] = [""]
    end_steps: list[str] = [""]
    start_cells: list[tuple[Cell, bool]] = [(panel.start_cell, False)]
    end_cells: list[tuple[Cell, bool]] = [(panel.end_cell, False)]
    solution: str = "None"
    common_cells: list[Cell] = []
    
    for i in range(panel.size[0]):
        for j in range(panel.size[1]):
            panel.map[i][j].view = False
    while not common_cells:
        common_cells = exist_equal_cells(start_cells, end_cells)
        for i in range(len(start_steps)):
            if start_cells[i][1]:
                continue
            move_start(start_steps, start_cells, i)
        for i in range(len(end_steps)):
            if end_cells[i][1]:
                continue
            move_end(end_steps, end_cells, i)
    
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


def move_start(steps: list[str],
               cells: list[tuple[Cell, bool]], index: int) -> bool:
    map: Panel = cells[index][0].map
    directions: list[tuple[Cardinal, str, bool]] = [
        (Cardinal.N, "N", cells[index][0].state.north
         or map.get_cell(Cardinal.N, cells[index][0].position).view),
        (Cardinal.E, "E", cells[index][0].state.east
         or map.get_cell(Cardinal.E, cells[index][0].position).view),
        (Cardinal.S, "S", cells[index][0].state.south
         or map.get_cell(Cardinal.S, cells[index][0].position).view),
        (Cardinal.W, "W", cells[index][0].state.west
         or map.get_cell(Cardinal.W, cells[index][0].position).view),
    ]
    available: list[tuple[Cardinal, str]] = [
        (direction, name)
        for direction, name, is_wall in directions if not is_wall
    ]
    if not available or cells[index][1]:
        cells[index] = (cells[index][0], True)
        return False

    branches: list[tuple[str, Cell]] = [
        (steps[index] + name, map.get_cell(direction, cells[index][0].position))
        for direction, name in available
    ]
    steps[index] = branches[0][0]
    cells[index] = (branches[0][1], cells[index][1])
    cells[index][0].view = True
    for branch_steps, branch_cell in branches[1:]:
        steps.append(branch_steps)
        branch_cell.view = True
        cells.append((branch_cell, False))
    return True


def move_end(steps: list[str],
             cells: list[tuple[Cell, bool]], index: int) -> bool:
    map: Panel = cells[index][0].map
    directions: list[tuple[Cardinal, str, bool]] = [
        (Cardinal.N, "N", cells[index][0].state.north
         or map.get_cell(Cardinal.N, cells[index][0].position).view_from_end),
        (Cardinal.E, "E", cells[index][0].state.east
         or map.get_cell(Cardinal.E, cells[index][0].position).view_from_end),
        (Cardinal.S, "S", cells[index][0].state.south
         or map.get_cell(Cardinal.S, cells[index][0].position).view_from_end),
        (Cardinal.W, "W", cells[index][0].state.west
         or map.get_cell(Cardinal.W, cells[index][0].position).view_from_end),
    ]
    available: list[tuple[Cardinal, str]] = [
        (direction, name)
        for direction, name, is_wall in directions if not is_wall
    ]
    if not available or cells[index][1]:
        cells[index] = (cells[index][0], True)
        return False

    branches: list[tuple[str, Cell]] = [
        (steps[index] + name, map.get_cell(direction, cells[index][0].position))
        for direction, name in available
    ]
    steps[index] = branches[0][0]
    cells[index] = (branches[0][1], cells[index][1])
    cells[index][0].view_from_end = True
    for branch_steps, branch_cell in branches[1:]:
        steps.append(branch_steps)
        branch_cell.view_from_end = True
        cells.append((branch_cell, False))
    return True


def exist_equal_cells(s_cells: list[tuple[Cell, bool]],
                      e_cells: list[tuple[Cell, bool]]) -> list[Cell]:
    e_pos: tuple[int, int] = {cell.position for cell, _ in e_cells}
    return [cell for cell, _ in s_cells if cell.position in e_pos]


def display_solution(panel: Panel, steps: str) -> None:
    from Model.Exceptions.OffTheMap import OffTheMap
    from Model.Enums.TypeCell import TypeCell
    from Utils.Colors import CYAN, GREEN, RED, RESET, YELLOW
    import sys
    import time

    direction_info: dict[str, tuple[Cardinal, str]] = {
        "N": (Cardinal.N, "north"),
        "E": (Cardinal.E, "east"),
        "S": (Cardinal.S, "south"),
        "W": (Cardinal.W, "west"),
    }
    if steps == "None":
        raise ValueError("No solution was provided")

    path_positions: list[tuple[int, int]] = [panel.start_cell.position]
    current: Cell = panel.start_cell
    for step_number, step in enumerate(steps, start=1):
        if step not in direction_info:
            raise ValueError(f"Invalid direction at step {step_number}: {step}")
        direction, wall_name = direction_info[step]
        if getattr(current.state, wall_name):
            raise ValueError(f"Step {step_number} crosses a wall")
        try:
            current = panel.get_cell(direction, current.position)
        except OffTheMap as error:
            raise ValueError(f"Step {step_number} leaves the maze") from error
        if current.type == TypeCell.CLOSED42:
            raise ValueError(f"Step {step_number} enters a closed cell")
        path_positions.append(current.position)

    def draw_frame(visited_positions: set[tuple[int, int]]) -> None:
        print("\033[H\033[J", end="")
        for row in panel.map:
            top_line = ""
            middle_line = ""
            for cell in row:
                top_line += "+"
                top_line += "---" if cell.state.north else "   "
            top_line += "+"

            for cell in row:
                middle_line += "|" if cell.state.west else " "
                if cell == panel.start_cell:
                    middle_line += f"{YELLOW} S {RESET}"
                elif cell == panel.end_cell:
                    middle_line += f"{RED} E {RESET}"
                elif cell.type == TypeCell.CLOSED42:
                    middle_line += f"{CYAN} # {RESET}"
                elif cell.position in visited_positions:
                    middle_line += f"{RED} 8 {RESET}"
                elif cell.view:
                    middle_line += f"{GREEN} 0 {RESET}"
                else:
                    middle_line += "   "
            middle_line += "|" if row[-1].state.east else " "
            print(top_line)
            print(middle_line)

        bottom_line = ""
        for cell in panel.map[-1]:
            bottom_line += "+"
            bottom_line += "---" if cell.state.south else "   "
        bottom_line += "+"
        print(bottom_line)
        sys.stdout.flush()

    visited_positions: set[tuple[int, int]] = set()
    for position in path_positions:
        visited_positions.add(position)
        draw_frame(visited_positions)
        time.sleep(0.08)
