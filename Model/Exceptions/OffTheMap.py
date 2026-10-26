class OffTheMap(Exception):
    def __init__(self, message: str = "The cell selected is off the map"):
        super().__init__(message)
