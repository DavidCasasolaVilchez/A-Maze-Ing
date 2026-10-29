from Model.Panel import Panel
from Model.Cell import Cell


def PanelToTxt(panel: Panel, steps: str, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8"):
        pass
    for line in range(panel.size[0]):
        for row in range(panel.size[1]):
            with open("result.txt", "a", encoding="utf-8") as text:
                text.write(ParsePanel(panel.map[line][row]))
        with open("result.txt", "a", encoding="utf-8") as text:
            text.write("\n")
    with open("result.txt", "a", encoding="utf-8") as text:
        text.write("\n")
        text.write(str(panel.start_cell.position) + "    #entry (x,y)\n")
        text.write(str(panel.end_cell.position) + "    #exit (x,y)\n")
        text.write(steps + "\n")


def ParsePanel(cell: Cell) -> str:
    north: int = 0 if not cell.state.north else 0b0001
    east: int = 0 if not cell.state.east else 0b0010
    south: int = 0 if not cell.state.south else 0b0100
    west: int = 0 if not cell.state.west else 0b1000
    result: int = north | east | south | west
    return (format(result, "x"))
