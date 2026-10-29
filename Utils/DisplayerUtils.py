from Utils.Colors import RESET, CYAN, YELLOW, RED, WHITE, BLACK, MAGENTA, BLUE
from Model.Enums.DisplayMode import DisplayMode
from Utils.Colors import colors, CLEAR


class DisplayerUtils():
    def __init__(self,
                 path: str,
                 floor42: str,
                 corner42: str,
                 wall42: str,
                 corner: str,
                 floor: str,
                 wall: str,
                 efloor: str,
                 ewall: str,
                 entry: str,
                 exit: str,
                 c42: str):
        self.color_path: str = BLUE
        self.color_border_42: str = MAGENTA
        self.color_cell_42: str = CYAN
        self.color_border: str = BLACK
        self.color_empty: str = WHITE
        self.color_entry: str = YELLOW
        self.color_exit: str = RED
        self.path: str = path
        self.floor42: str = floor42
        self.wall42: str = wall42
        self.corner42: str = corner42
        self.corner: str = corner
        self.floor: str = floor
        self.wall: str = wall
        self.empty_floor: str = efloor
        self.empty_wall: str = ewall
        self.entry: str = entry
        self.exit: str = exit
        self.c42: str = c42

    @staticmethod
    def create_display(mode: DisplayMode) -> "DisplayerUtils":
        path: str
        floor42: str
        wall42: str
        corner42: str
        corner: str
        floor: str
        wall: str
        empty_floor: str
        empty_wall: str
        entry: str
        exit: str
        c42: str
        if mode == DisplayMode.COMPLETE:
            path = "██"
            floor42 = "██"
            wall42 = "██"
            corner42 = "██"
            corner = "██"
            floor = "██"
            wall = "██"
            empty_floor = "██"
            empty_wall = "██"
            entry = "██"
            exit = "██"
            c42 = "▒▒"
        else:
            path = " ■ "
            floor42 = "---"
            wall42 = "|"
            corner42 = "+"
            corner = "+"
            floor = "---"
            wall = "|"
            empty_floor = "   "
            empty_wall = " "
            entry = " ■ "
            exit = " ■ "
            c42 = " ■ "
        return DisplayerUtils(
            path, floor42, corner42, wall42, corner, floor, wall, empty_floor,
            empty_wall, entry, exit, c42)

    @staticmethod
    def _display_color_selector(obj: str) -> str:
        selection: int
        while True:
            try:
                print("Select color:")
                for i, color in enumerate(colors):
                    print(f"{i + 1}.-{color} ■ {RESET}")
                selection = int(input(
                    f"Introduce the number of the selected color for {obj}:"))
                return colors[selection - 1]
            except IndexError:
                print(f"{CLEAR}", end="")
                print(
                    f"{RED}The number selected must be between"
                    f" 1 and {len(colors)}{RESET}")
            except ValueError:
                print(f"{CLEAR}", end="")
                print(f"{RED}The selection has to be a number{RESET}")

    def change_color_path(self) -> None:
        self.color_path = DisplayerUtils._display_color_selector("path")

    def change_color_border_42(self) -> None:
        self.color_border_42 = DisplayerUtils._display_color_selector(
            "border 42")

    def change_color_cell_42(self) -> None:
        self.color_cell_42 = DisplayerUtils._display_color_selector("cell 42")

    def change_color_border(self) -> None:
        self.color_border = DisplayerUtils._display_color_selector("border")

    def change_color_empty(self) -> None:
        self.color_empty = DisplayerUtils._display_color_selector("empty")

    def change_color_entry(self) -> None:
        self.color_entry = DisplayerUtils._display_color_selector("entry")

    def change_color_exit(self) -> None:
        self.color_exit = DisplayerUtils._display_color_selector("exit")
