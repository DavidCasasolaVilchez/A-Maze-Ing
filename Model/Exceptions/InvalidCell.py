class InvalidCell(Exception):
    def __init__(self, message: str = "The cell is invalid"):
        super().__init__(message)
