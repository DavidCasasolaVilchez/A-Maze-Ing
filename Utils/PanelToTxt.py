from Model import Panel
from Model import Cell

with open("result.txt", "w", encoding="utf-8"):
    pass

def PanelToTxt(panel: Panel) -> None:
    for line in range(panel.size[0]):
        for row in range(panel.size[1]):
            with open("result.txt", "a", encoding="utf-8") as text:
                text.write(ParsePanel(panel.map[line][row]))
        with open("result.txt", "a", encoding="utf-8") as text:
            text.write("\n")

def ParsePanel(cell: Cell) -> str:
    north: int = 0 if cell.state.north else 0b0001
    east: int = 0 if cell.state.east else 0b0010
    south: int = 0 if cell.state.south else 0b0100
    west: int = 0 if cell.state.west else 0b1000
    result: int = north | east | south | west
    return (format(result, ))