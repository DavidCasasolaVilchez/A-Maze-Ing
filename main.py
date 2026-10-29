from Utils.Colors import GREEN, RESET, RED, CLEAR, colors
from Utils.PanelToTxt import PanelToTxt
from Utils.ArgsParser import ArgsParser
from Model.Panel import Panel
import time


def menu() -> None:
    args: ArgsParser = ArgsParser("config.txt")
    options: list[tuple[int, str]] = [
        (1, "1. Re-generate a new maze"),
        (2, "2. Show / Hide the shortest path"),
        (3, "3. Select maze colors"),
        (4, "4. Quit")
    ]

    p: Panel = Panel.create_base(
        (args.height, args.width),
        args.perfect,
        args.entry,
        args.exit,
        args.seed,
        args.display_mode,
        0
    )
    path: bool = True
    retry: bool = True
    selection: int = 0
    while selection != 4:
        try:
            if retry:
                retry = False
                p.make_maze()
                PanelToTxt(p, p.solution)
            p.display_ascii(-1)
            if path:
                for step in range(p.path_cell_count + 1):
                    print(f"{CLEAR}", end="")
                    p.display_ascii(step)
                    time.sleep(0.08)
            print("=== A-Maze-ing ===")
            for i in range(len(options)):
                print(options[i][1])
            selection = int(input(f"{GREEN}Choice? (1/4): {RESET}"))
            match selection:
                case 1:
                    p = Panel.create_base(
                        (args.height, args.width),
                        args.perfect,
                        args.entry,
                        args.exit,
                        args.seed,
                        args.display_mode,
                        0
                    )
                    path = True
                    retry = True
                    print(f"{CLEAR}", end="")
                case 2:
                    path = not path
                    print(f"{CLEAR}", end="")
                case 3:
                    p.displayer.change_color_border()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_border_42()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_cell_42()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_empty()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_entry()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_exit()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_path()
                    print(f"{CLEAR}", end="")
                case 4:
                    print(f"{CLEAR}", end="")
                    break
                case _:
                    print(f"{CLEAR}", end="")
                    print(
                        f"{RED}The number selected must be between"
                        f" 1 and {len(colors)}{RESET}")
        except ValueError:
            print(f"{CLEAR}", end="")
            print(f"{RED}The selection has to be a number{RESET}")


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
