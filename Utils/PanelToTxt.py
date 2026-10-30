from Model.Panel import Panel
from Model.Cell import Cell


def PanelToTxt(panel: Panel, steps: str, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8"):
        pass
    for line in range(panel.size[0]):
        for row in range(panel.size[1]):
            with open(file_name, "a", encoding="utf-8") as text:
                text.write(ParsePanel(panel.map[line][row]))
        with open(file_name, "a", encoding="utf-8") as text:
            text.write("\n")
    with open(file_name, "a", encoding="utf-8") as text:
        entry: tuple[int, int] = panel.start_cell.position
        exit: tuple[int, int] = panel.end_cell.position
        text.write("\n")
        text.write(f"{entry[0]},{entry[1]}\n")
        text.write(f"{exit[0]},{exit[1]}\n")
        text.write(f"{steps}\n")


def ParsePanel(cell: Cell) -> str:
    north: int = 0 if not cell.state.north else 0b0001
    east: int = 0 if not cell.state.east else 0b0010
    south: int = 0 if not cell.state.south else 0b0100
    west: int = 0 if not cell.state.west else 0b1000
    result: int = north | east | south | west
    return (format(result, "x"))
