import os

def is_windows():
    if os.name == "nt": return True
    return False

def is_linux():
    if os.name == "posix": return True
    return False
