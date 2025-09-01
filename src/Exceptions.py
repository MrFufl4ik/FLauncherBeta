class ClientVersionError(Exception):
    def __init__(self, message: str): super().__init__(message)

class ClientUpdateCheckForUpdate(Exception):
    def __init__(self, message: str): super().__init__(message)