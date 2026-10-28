from Utils.Colors import RESET, CYAN, YELLOW, RED, WHITE, BLACK, MAGENTA
from Model.Enums.DisplayMode import DisplayMode


class DisplayerUtils():
    def __init__(self,
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
            floor42 = f"{MAGENTA}██{RESET}"
            wall42 = f"{MAGENTA}██{RESET}"
            corner42 = f"{MAGENTA}██{RESET}"
            corner = f"{BLACK}██{RESET}"
            floor = f"{BLACK}██{RESET}"
            wall = f"{BLACK}██{RESET}"
            empty_floor = f"{WHITE}██{RESET}"
            empty_wall = f"{WHITE}██{RESET}"
            entry = f"{YELLOW}██{RESET}"
            exit = f"{RED}██{RESET}"
            c42 = f"{CYAN}▒▒{RESET}"
        else:
            floor42 = f"{MAGENTA}---{RESET}"
            wall42 = f"{MAGENTA}|{RESET}"
            corner42 = f"{MAGENTA}+{RESET}"
            corner = "+"
            floor = "---"
            wall = "|"
            empty_floor = "   "
            empty_wall = " "
            entry = f"{YELLOW} ■ {RESET}"
            exit = f"{RED} ■ {RESET}"
            c42 = f"{CYAN} ■ {RESET}"
        return DisplayerUtils(
            floor42, corner42, wall42, corner, floor, wall, empty_floor,
            empty_wall, entry, exit, c42)
