import os

from src.utils import JsonManager


class ClientVersion:
    def __init__(self, version_str):
        if not isinstance(version_str, str):
            raise TypeError("Version must be a string")

        parts = version_str.split('.')
        if not parts:
            raise ValueError("Version string cannot be empty")

        self.version = []
        for part in parts:
            if not part.isdigit():
                raise ValueError(f"Version part '{part}' is not a number")
            self.version.append(int(part))

        self.version = tuple(self.version)
        self.version_str = version_str  # сохраняем исходную строку

    def __gt__(self, other):
        if not isinstance(other, ClientVersion):
            raise TypeError(f"Cannot compare Version with {type(other)}")
        return self.version > other.version

    def __lt__(self, other):
        if not isinstance(other, ClientVersion):
            raise TypeError(f"Cannot compare Version with {type(other)}")
        return self.version < other.version

    def __eq__(self, other):
        if not isinstance(other, ClientVersion):
            raise TypeError(f"Cannot compare Version with {type(other)}")
        return self.version == other.version

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.version_str

    def __repr__(self):
        return f"Version('{self.version_str}')"

class ClientManager:
    _instance = None

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_or_get_client_absolute_path(self) -> str:
        client_path = f"{os.getcwd()}/client"
        if not os.path.exists(client_path): os.makedirs(client_path)
        return client_path

    def is_client_install(self) -> bool:
        client_path = self.create_or_get_client_absolute_path()
        return JsonManager.readJson(f"{client_path}/client.json") is not None

    def get_client_version(self) -> ClientVersion | None:
        client_path = self.create_or_get_client_absolute_path()
        if not self.is_client_install(): return ClientVersion("0")
        json = JsonManager.readJson(f"{client_path}/client.json")
        if "version" in json and json["version"] is str: return ClientVersion(json["version"])
        else: return ClientVersion("0")