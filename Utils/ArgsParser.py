from Model.Exceptions.InvalidArguments import InvalidArguments
from Model.Enums.DisplayMode import DisplayMode
import sys


class ArgsParser():
    def __init__(self, fconfig: str):
        self.width: int | None = None
        self.height: int | None = None
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.output_file: str | None = None
        self.perfect: bool | None = None
        self.seed: int | None = None
        self.display_mode: DisplayMode | None = None
        self.read_file(fconfig)
        self.validator()

    def validator(self) -> None:
        if (self.width is None or self.height is None or
                self.entry is None or self.exit is None or
                self.output_file is None or self.perfect is None or
                self.seed is None or self.display_mode is None):
            raise InvalidArguments(
                            "All the values must be initializated")
        if self.height < 15:
            raise InvalidArguments(
                "The height can't be less than 15")
        if self.width < 20:
            raise InvalidArguments(
                "The width can't be less than 20")
        if (self.entry[0] > self.width or self.entry[0] < 0 or
                self.entry[1] > self.height or self.entry[1] < 0):
            raise InvalidArguments(
                f"Entry must be behind [0-{self.width}] and [0-{self.height}]")
        if (self.exit[0] > self.width or self.exit[0] < 0 or
                self.exit[1] > self.height or self.exit[1] < 0):
            raise InvalidArguments(
                f"Exit must be behind [0-{self.width}] and [0-{self.height}]")

    def evaluate_line(self, line: str) -> bool:
        try:
            if line == "":
                return False
            kv: list[str] = line.split("=", 2)
            if len(kv) == 1:
                raise InvalidArguments("The arg format has to be [KEY=VALUE]")
            kv[1] = kv[1].removesuffix("\n")
            if kv[0].lower() == "width":
                self.width = int(kv[1])
            elif kv[0].lower() == "height":
                self.height = int(kv[1])
            elif kv[0].lower() == "entry":
                tp: list[str] = kv[1].split(",", 2)
                if len(tp) == 1:
                    raise InvalidArguments("The tuple has to use [0,0] format")
                self.entry = (int(tp[1]), int(tp[0]))
            elif kv[0].lower() == "exit":
                tp: list[str] = kv[1].split(",", 2)
                if len(tp) == 1:
                    raise InvalidArguments("The tuple has to use [0,0] format")
                self.exit = (int(tp[1]), int(tp[0]))
            elif kv[0].lower() == "output_file":
                self.output_file = kv[1]
            elif kv[0].lower() == "perfect":
                if kv[1].lower() == "true":
                    self.perfect = True
                elif kv[1].lower() == "false":
                    self.perfect = False
                else:
                    raise InvalidArguments("Perfect has to be True/False")
            elif kv[0].lower() == "seed":
                self.seed = int(kv[1])
            elif kv[0].lower() == "display_mode":
                if kv[1].upper() == "COMPLETE":
                    self.display_mode = DisplayMode.COMPLETE
                elif kv[1].upper() == "ASCIIBASE":
                    self.display_mode = DisplayMode.ASCIIBASE
                else:
                    raise InvalidArguments(
                        "Display_mode has to be COMPLETE/ASCIIBASE")
            else:
                raise InvalidArguments("The arguments are not correct")
            return True
        except ValueError:
            raise InvalidArguments(
                "The value of width, height and seed must be a valid int")

    def read_file(self, config_name: str) -> None:
        try:
            with open(config_name, "r", encoding="utf-8") as file:
                while True:
                    if (not self.evaluate_line(file.readline())):
                        break
        except OSError as error:
            print(f"Cannot read file: {error}")
            sys.exit(1)
