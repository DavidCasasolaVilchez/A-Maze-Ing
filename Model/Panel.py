from Model.Exceptions.CreationFailed import CreationFailed
from Model.Exceptions.OffTheMap import OffTheMap
from Utils.DisplayerUtils import DisplayerUtils
from Model.Enums.DisplayMode import DisplayMode
from Utils.ConquerCell import conquer_cell
from Model.Enums.Cardinal import Cardinal
from Model.Enums.TypeCell import TypeCell
from Model.Movement import Movement
from Utils.GoBack import go_back
from Utils.Colors import (
    BLACK, BLUE, BRIGHT_MAGENTA, BRIGHT_RED, CYAN, GREEN, MAGENTA, RED,
    RESET, WHITE, YELLOW
)
from Model.Cell import Cell
from random import Random
import curses
import re


class Panel():
    _ANSI_COLOR_CODES: dict[str, int] = {
        BLACK: curses.COLOR_BLACK,
        RED: curses.COLOR_RED,
        GREEN: curses.COLOR_GREEN,
        YELLOW: curses.COLOR_YELLOW,
        BLUE: curses.COLOR_BLUE,
        MAGENTA: curses.COLOR_MAGENTA,
        CYAN: curses.COLOR_CYAN,
        WHITE: curses.COLOR_WHITE,
    }

    def __init__(
            self,
            map: list[list[Cell]],
            size: tuple[int, int],
            is_perfect: bool,
            start_cell: Cell,
            end_cell: Cell,
            seed: int,
            mode: DisplayMode,
            path_cell_count: int
            ):
        self.is_perfect: bool = is_perfect
        self.start_cell: Cell = start_cell
        self.size: tuple[int, int] = size
        self.map: list[list[Cell]] = map
        self.end_cell: Cell = end_cell
        self.seed: int = seed
        self.solution: str = ""
        self.displayer: DisplayerUtils = DisplayerUtils.create_display(mode)
        self.path_cell_count: int = path_cell_count
        self.rnd: Random = Random(seed)
        self.refill_map()

    @staticmethod
    def create_base(
        size: tuple[int, int],
        is_perfect: bool,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int,
        mode: DisplayMode,
        path_cell_count: int
    ) -> "Panel":
        map: list[list[Cell]] = list()
        for y in range(0, size[0]):
            map.append(list())
            for x in range(0, size[1]):
                map[y].append(Cell.create_base_cell((y, x), None))
        map[entry[0]][entry[1]].change_type(TypeCell.START)
        map[exit[0]][exit[1]].change_type(TypeCell.END)
        path_cell_count = 0
        return Panel(
            map,
            size,
            is_perfect,
            map[entry[0]][entry[1]],
            map[exit[0]][exit[1]],
            seed,
            mode,
            path_cell_count
        )

    def make_maze(self) -> None:
        for row in self.map:
            for cell in row:
                if cell.type == TypeCell.PATH:
                    cell.type = TypeCell.BASE
        self.generate42()
        self.convert_to_base()
        if not self.is_perfect:
            self.convert_imperfect()
        self.solve()

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

    def convert_imperfect(self) -> None:
        for line in self.map:
            for cell in line:
                if cell.type != TypeCell.CLOSED42:
                    value: int = 0
                    if cell.state.east:
                        value += 1
                    if cell.state.south:
                        value += 1
                    if cell.state.north:
                        value += 1
                    if cell.state.west:
                        value += 1
                    if value > 2:
                        cell.break_random_valid_wall(self.rnd)

    def get_ascii(self, path_until: int) -> str:
        complete_line: str = ""
        for y, line in enumerate(self.map):
            top_line = ""
            middle_line = ""
            for cell in line:
                try:
                    if (cell.type == TypeCell.CLOSED42 or
                        self.get_cell(Cardinal.N, cell.position).type
                        == TypeCell.CLOSED42 or
                        self.get_cell(Cardinal.W, cell.position).type
                        == TypeCell.CLOSED42 or
                        self.get_cell(Cardinal.W, self.get_cell(
                            Cardinal.N, cell.position).position).type
                            == TypeCell.CLOSED42):
                        top_line += (f"{self.displayer.color_border_42}"
                                     f"{self.displayer.corner42}{RESET}")
                    else:
                        top_line += (f"{self.displayer.color_border}"
                                     f"{self.displayer.corner}{RESET}")
                except (OffTheMap):
                    top_line += (f"{self.displayer.color_border}"
                                 f"{self.displayer.corner}{RESET}")
                if cell.state.north:
                    try:
                        if (cell.type == TypeCell.CLOSED42 or
                            self.get_cell(Cardinal.N, cell.position).type
                                == TypeCell.CLOSED42):
                            top_line += (f"{self.displayer.color_border_42}"
                                         f"{self.displayer.floor}{RESET}")
                        else:
                            top_line += (f"{self.displayer.color_border}"
                                         f"{self.displayer.floor}{RESET}")
                    except (OffTheMap):
                        top_line += (f"{self.displayer.color_border}"
                                     f"{self.displayer.floor}{RESET}")
                else:
                    top_line += (f"{self.displayer.color_empty}"
                                 f"{self.displayer.empty_floor}{RESET}")
            try:
                if (cell.type == TypeCell.CLOSED42 or
                    self.get_cell(Cardinal.N, cell.position).type
                    == TypeCell.CLOSED42 or
                    self.get_cell(Cardinal.W, cell.position).type
                        == TypeCell.CLOSED42):
                    top_line += (f"{self.displayer.color_border_42}"
                                 f"{self.displayer.corner42}{RESET}")
                else:
                    top_line += (f"{self.displayer.color_border}"
                                 f"{self.displayer.corner}{RESET}")
            except (OffTheMap):
                top_line += (f"{self.displayer.color_border}"
                             f"{self.displayer.corner}{RESET}")
            for x, cell in enumerate(line):
                if cell.state.west:
                    try:
                        if (cell.type == TypeCell.CLOSED42 or
                            self.get_cell(Cardinal.W, cell.position).type
                                == TypeCell.CLOSED42):
                            middle_line += (f"{self.displayer.color_border_42}"
                                            f"{self.displayer.wall42}{RESET}")
                        else:
                            middle_line += (f"{self.displayer.color_border}"
                                            f"{self.displayer.wall}{RESET}")
                    except (OffTheMap):
                        middle_line += (f"{self.displayer.color_border}"
                                        f"{self.displayer.wall}{RESET}")
                else:
                    middle_line += (f"{self.displayer.color_empty}"
                                    f"{self.displayer.empty_wall}{RESET}")
                if cell.actual:
                    middle_line += (f"{self.displayer.color_actual}"
                                    f"{self.displayer.actual}{RESET}")
                elif cell == self.start_cell:
                    middle_line += (f"{self.displayer.color_entry}"
                                    f"{self.displayer.entry}{RESET}")
                elif cell.player_path and cell.type != TypeCell.PATH:
                    middle_line += (f"{self.displayer.color_error_path}"
                                    f"{self.displayer.player_path}{RESET}")
                elif cell.player_path:
                    middle_line += (f"{self.displayer.color_player_path}"
                                    f"{self.displayer.player_path}{RESET}")
                elif cell == self.end_cell:
                    middle_line += (f"{self.displayer.color_exit}"
                                    f"{self.displayer.exit}{RESET}")
                elif cell.type == TypeCell.CLOSED42:
                    middle_line += (f"{self.displayer.color_cell_42}"
                                    f"{self.displayer.c42}{RESET}")
                elif (cell.path > 0 and cell.path <= path_until):
                    middle_line += (f"{self.displayer.color_path}"
                                    f"{self.displayer.path}{RESET}")
                else:
                    middle_line += (f"{self.displayer.color_empty}"
                                    f"{self.displayer.empty_floor}{RESET}")
            if line[-1].state.east:
                middle_line += (f"{self.displayer.color_border}"
                                f"{self.displayer.wall}{RESET}")
            else:
                middle_line += (f"{self.displayer.color_empty}"
                                f"{self.displayer.empty_wall}{RESET}")
            complete_line += f"{top_line}\n"
            complete_line += f"{middle_line}\n"
        bottom_line = ""
        for cell in self.map[-1]:
            bottom_line += (f"{self.displayer.color_border}"
                            f"{self.displayer.corner}{RESET}")
            if cell.state.south:
                bottom_line += (f"{self.displayer.color_border}"
                                f"{self.displayer.floor}{RESET}")
            else:
                bottom_line += (f"{self.displayer.color_empty}"
                                f"{self.displayer.empty_floor}{RESET}")
        bottom_line += (f"{self.displayer.color_border}"
                        f"{self.displayer.corner}{RESET}")
        complete_line += f"{bottom_line}\n"
        return complete_line

    def display_ascii(self, path_until: int) -> str:
        complete: str = self.get_ascii(path_until)
        print(complete)
        return complete

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

    def solve(self) -> None:
        path: str = self.start_search()
        actual: Cell = self.start_cell
        for i in path:
            if actual.type != TypeCell.START and actual.type != TypeCell.END:
                actual.type = TypeCell.PATH
                self.path_cell_count += 1
            match i:
                case 'N':
                    actual = self.get_cell(Cardinal.N, actual.position)
                case 'S':
                    actual = self.get_cell(Cardinal.S, actual.position)
                case 'E':
                    actual = self.get_cell(Cardinal.E, actual.position)
                case 'W':
                    actual = self.get_cell(Cardinal.W, actual.position)

    def start_search(self) -> str:
        start_steps: list[str] = [""]
        end_steps: list[str] = [""]
        start_cells: list[tuple[Cell, bool]] = [(self.start_cell, False)]
        end_cells: list[tuple[Cell, bool]] = [(self.end_cell, False)]
        common_cells: list[Cell] = []
        current_solution: tuple[str, bool]
        self.solution = ""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.map[i][j].view = False
        while not common_cells:
            for i in range(len(start_steps)):
                if start_cells[i][1]:
                    continue
                self.move_start(start_steps, start_cells, i)
                common_cells = self.exist_equal_cells(start_cells, end_cells)
                if common_cells:
                    break
            for i in range(len(end_steps)):
                if end_cells[i][1]:
                    continue
                self.move_end(end_steps, end_cells, i)
                common_cells = self.exist_equal_cells(start_cells, end_cells)
                if common_cells:
                    break
        for i in range(len(common_cells)):
            current: str = (
                start_steps[
                    self.cells_only(start_cells).index((common_cells[i]))]
                + self.invert(end_steps[
                    self.cells_only(end_cells).index(common_cells[i])])
            )
            if not self.solution or len(self.solution) > len(current):
                self.solution = current
        current_solution = (self.solution, True)
        while (current_solution[1]):
            current_solution = self.quit_concurrency(current_solution[0])
        self.solution = current_solution[0]
        self.assign_path(self.solution)
        return self.solution

    def assign_path(self, sol: str) -> None:
        current_cell: Cell = self.start_cell
        direction: dict[str, Cardinal] = {
            'N': Cardinal.N,
            'E': Cardinal.E,
            'S': Cardinal.S,
            'W': Cardinal.W
        }
        for i, c in enumerate(sol):
            current_cell = self.get_cell(direction[c], current_cell.position)
            current_cell.path = i + 1

    def quit_concurrency(self, sol: str) -> tuple[str, bool]:
        movement: list[tuple[int, int]] = [(0, 0)]
        index_s: int = -1
        index_e: int = -1
        for i, c in enumerate(sol):
            match c:
                case 'N':
                    movement.append((movement[i][0] - 1, movement[i][1]))
                case 'E':
                    movement.append((movement[i][0], movement[i][1] + 1))
                case 'S':
                    movement.append((movement[i][0] + 1, movement[i][1]))
                case 'W':
                    movement.append((movement[i][0], movement[i][1] - 1))
        for i in range(len(movement)):
            for j in range(i + 1, len(movement)):
                if movement[i] == movement[j]:
                    index_s = i
                    index_e = j
                    break
        if (index_s < 0 or index_e < 0):
            return (sol, False)
        return (sol[:index_s] + sol[index_e:], True)

    def invert(self, s: str) -> str:
        opposite: dict[str, str] = {
            'N': 'S',
            'E': 'W',
            'S': 'N',
            'W': 'E'
        }
        return "".join(opposite[c] for c in reversed(s))

    def move_start(self, steps: list[str],
                   cells: list[tuple[Cell, bool]], index: int) -> bool:
        directions: list[tuple[Cardinal, str, bool]] = [
            (Cardinal.N, "N", cells[index][0].state.north or
                self.get_cell(Cardinal.N, cells[index][0].position).view),
            (Cardinal.E, "E", cells[index][0].state.east or
                self.get_cell(Cardinal.E, cells[index][0].position).view),
            (Cardinal.S, "S", cells[index][0].state.south or
                self.get_cell(Cardinal.S, cells[index][0].position).view),
            (Cardinal.W, "W", cells[index][0].state.west or
                self.get_cell(Cardinal.W, cells[index][0].position).view),
        ]
        available: list[tuple[Cardinal, str]] = [
            (direction, name)
            for direction, name, is_wall in directions if not is_wall
        ]
        if not available or cells[index][1]:
            cells[index] = (cells[index][0], True)
            return False

        branches: list[tuple[str, Cell]] = [
            (steps[index] + name, self.get_cell(direction,
                                                cells[index][0].position))
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

    def move_end(self, steps: list[str],
                 cells: list[tuple[Cell, bool]], index: int) -> bool:
        map = cells[index][0].map
        if map is None:
            return False
        directions: list[tuple[Cardinal, str, bool]] = [
            (Cardinal.N, "N", cells[index][0].state.north or
                map.get_cell(Cardinal.N,
                             cells[index][0].position).view_from_end),
            (Cardinal.E, "E", cells[index][0].state.east or
                map.get_cell(Cardinal.E,
                             cells[index][0].position).view_from_end),
            (Cardinal.S, "S", cells[index][0].state.south or
                map.get_cell(Cardinal.S,
                             cells[index][0].position).view_from_end),
            (Cardinal.W, "W", cells[index][0].state.west or
                map.get_cell(Cardinal.W,
                             cells[index][0].position).view_from_end),
        ]
        available: list[tuple[Cardinal, str]] = [
            (direction, name)
            for direction, name, is_wall in directions if not is_wall
        ]
        if not available or cells[index][1]:
            cells[index] = (cells[index][0], True)
            return False

        branches: list[tuple[str, Cell]] = [
            (steps[index] + name,
             map.get_cell(direction, cells[index][0].position))
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

    def exist_equal_cells(
            self,
            s_cells: list[tuple[Cell, bool]],
            e_cells: list[tuple[Cell, bool]]) -> list[Cell]:
        e_pos: set[tuple[int, int]] = {cell.position for cell, _ in e_cells}
        return [cell for cell, _ in s_cells if cell.position in e_pos]

    def cells_only(self, cells: list[tuple[Cell, bool]]) -> list[Cell]:
        return [cell for cell, _ in cells]

    def try_advance(self, actual: Cell, move: Movement) -> Cell:
        if not actual.is_valid_movement(move):
            raise Exception
        actual.actual = False
        actual = self.get_cell(move.direction, actual.position)
        actual.actual = True
        actual.player_path = True
        return actual

    def try_solve(self) -> bool:
        actual: Cell = self.start_cell
        actual.actual = True
        actual.player_path = True
        self.refill_playable_map()

        stdscr = curses.initscr()

        try:
            curses.start_color()
            curses.use_default_colors()
            stdscr.keypad(True)
            curses.noecho()
            curses.cbreak()
            self.init_curses_colors()

            while actual.type != TypeCell.END:
                self.display_curses(stdscr, 0)
                key = stdscr.getch()
                try:
                    match key:
                        case curses.KEY_UP:
                            move = Movement((-1, 0), Cardinal.N)
                            actual = self.try_advance(actual, move)
                        case curses.KEY_DOWN:
                            move = Movement((1, 0), Cardinal.S)
                            actual = self.try_advance(actual, move)
                        case curses.KEY_LEFT:
                            move = Movement((0, -1), Cardinal.W)
                            actual = self.try_advance(actual, move)
                        case curses.KEY_RIGHT:
                            move = Movement((0, 1), Cardinal.E)
                            actual = self.try_advance(actual, move)
                        case curses.KEY_ENTER | 10 | 13:
                            self.refill_playable_map()
                            return False
                except Exception:
                    self.display_curses(
                        stdscr,
                        0,
                        "Invalid movement"
                    )
            return True
        finally:
            curses.nocbreak()
            curses.echo()
            stdscr.keypad(False)
            curses.endwin()

    def init_curses_colors(self) -> None:
        for pair, curses_color in enumerate(
                self._ANSI_COLOR_CODES.values(), start=1):
            curses.init_pair(pair, curses_color, -1)

    def curses_attribute(self, ansi_color: str) -> int:
        color_pairs: dict[str, int] = {
            color: pair
            for pair, color in enumerate(self._ANSI_COLOR_CODES, start=1)
        }
        bright_colors: dict[str, tuple[str, int]] = {
            BRIGHT_RED: (RED, curses.A_BOLD),
            BRIGHT_MAGENTA: (MAGENTA, curses.A_BOLD),
        }
        if ansi_color == RESET:
            return curses.color_pair(0)
        if ansi_color in bright_colors:
            base_color, attribute = bright_colors[ansi_color]
            return curses.color_pair(color_pairs[base_color]) | attribute
        return curses.color_pair(color_pairs[ansi_color])

    def display_curses(
            self,
            stdsrc: curses.window,
            path_until: int,
            status: str = ""
            ) -> None:
        complete: str = self.get_ascii(path_until)
        lines: list[str] = complete.splitlines()
        stdsrc.clear()
        ansi_pattern = re.compile(r"(\033\[[0-9;]*m)")
        for row, line in enumerate(lines):
            column = 0
            attribute = curses.color_pair(0)
            for part in ansi_pattern.split(line):
                if not part:
                    continue
                if ansi_pattern.fullmatch(part):
                    attribute = self.curses_attribute(part)
                else:
                    stdsrc.addstr(row, column, part, attribute)
                    column += len(part)
        stdsrc.addstr(
            len(lines) + 1,
            0,
            "Move yourself using the arrows ['ENTER' for exit]"
        )
        if status:
            stdsrc.addstr(len(lines) + 2, 0, status)
        stdsrc.refresh()

    def refill_playable_map(self) -> None:
        for y in self.map:
            for x in y:
                x.actual = False
                x.player_path = False
        self.start_cell.actual = True
