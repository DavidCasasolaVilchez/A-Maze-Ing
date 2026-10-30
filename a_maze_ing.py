from Utils.Colors import GREEN, RESET, RED, CLEAR, colors
from Utils.PanelToTxt import PanelToTxt
from Utils.ArgsParser import ArgsParser
from Model.Panel import Panel
import random
import time
import sys


def menu(config_file: str) -> None:
    args: ArgsParser = ArgsParser(config_file)
    assert args.width is not None
    assert args.height is not None
    assert args.entry is not None
    assert args.exit is not None
    assert args.perfect is not None
    assert args.seed is not None
    assert args.display_mode is not None
    assert args.output_file is not None
    options: list[tuple[int, str]] = [
        (1, "1. Re-generate a new maze"),
        (2, "2. Generate maze with random entry and exit"),
        (3, "3. Show / Hide the shortest path"),
        (4, "4. Select maze colors"),
        (5, "5. Try to solve it by yourself"),
        (6, "6. Try to solve a new maze by yourself"),
        (7, "7. Quit")
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
    while selection != 7:
        try:
            if retry:
                retry = False
                p.make_maze()
                PanelToTxt(p, p.solution, args.output_file)
            p.display_ascii(-1)
            if path:
                for step in range(p.path_cell_count + 1):
                    print(f"{CLEAR}", end="")
                    p.display_ascii(step)
                    time.sleep(0.025)
            print("=== A-Maze-ing ===")
            for i in range(len(options)):
                print(options[i][1])
            selection = int(input(f"{GREEN}Choice? (1/7): {RESET}"))
            match selection:
                case 1:
                    p = Panel.create_base(
                        (args.height, args.width),
                        args.perfect,
                        args.entry,
                        args.exit,
                        args.seed * int(time.time()),
                        args.display_mode,
                        0
                    )
                    path = True
                    retry = True
                    print(f"{CLEAR}", end="")
                case 2:
                    p = Panel.create_base(
                        (args.height, args.width),
                        args.perfect,
                        (random.randint(0, p.size[0]),
                         random.randint(0, p.size[1])),
                        (random.randint(0, p.size[0]),
                         random.randint(0, p.size[1])),
                        args.seed * int(time.time()),
                        args.display_mode,
                        0
                    )
                    path = True
                    retry = True
                    print(f"{CLEAR}", end="")
                case 3:
                    path = not path
                    print(f"{CLEAR}", end="")
                case 4:
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
                    p.displayer.change_color_actual()
                    print(f"{CLEAR}", end="")
                    p.displayer.change_color_player_path()
                    print(f"{CLEAR}", end="")
                case 5:
                    if p.try_solve():
                        print(
                            f"{GREEN}Congratulations!"
                            f" You find the exit{RESET}")
                        time.sleep(2)
                    print(f"{CLEAR}", end="")
                case 6:
                    p = Panel.create_base(
                        (args.height, args.width),
                        args.perfect,
                        (random.randint(0, p.size[0]),
                         random.randint(0, p.size[1])),
                        (random.randint(0, p.size[0]),
                         random.randint(0, p.size[1])),
                        args.seed * int(time.time()),
                        args.display_mode,
                        0
                    )
                    p.make_maze()
                    PanelToTxt(p, p.solution, args.output_file)
                    if p.try_solve():
                        print(f"{CLEAR}", end="")
                        print(
                            f"{GREEN}Congratulations!"
                            f" You find the exit{RESET}")
                        time.sleep(2)
                    print(f"{CLEAR}", end="")
                case 7:
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
    if len(sys.argv) == 2:
        menu(sys.argv[1])
    else:
        print("You have to include a valid configuration file in arguments")


if __name__ == "__main__":
    main()
