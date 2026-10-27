class CreationFailed(Exception):
    def __init__(self, message: str =
                 "The creation process failed, try again"):
        super().__init__(message)
