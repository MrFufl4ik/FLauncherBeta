import os
import webbrowser


def is_windows():
    if os.name == "nt": return True
    return False

def is_linux():
    if os.name == "posix": return True
    return False

def open_web_site(url: str): webbrowser.open(url)