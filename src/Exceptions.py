#Client
class ClientVersionError(Exception):
    def __init__(self, message: str): super().__init__(message)
class ClientUpdateCheckForUpdate(Exception):
    def __init__(self, message: str): super().__init__(message)


#Json
class JsonDecoder(Exception):
    def __init__(self, message: str): super().__init__(message)
class JsonEncoder(Exception):
    def __init__(self, message: str): super().__init__(message)
