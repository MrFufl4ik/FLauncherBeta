#Client
class ClientVersionError(Exception):
    def __init__(self, message: str): super().__init__(message)
class ClientUpdateCheckForUpdate(Exception):
    def __init__(self, message: str): super().__init__(message)


#FTP
class FTPAuthError(Exception):
    def __init__(self): super().__init__()

class FTPServerError(Exception):
    def __init__(self): super().__init__()

class FTPNetworkError(Exception):
    def __init__(self): super().__init__()

class FTPUnknownError(Exception):
    def __init__(self): super().__init__()

class FTPSetupError(Exception):
    def __init__(self): super().__init__()