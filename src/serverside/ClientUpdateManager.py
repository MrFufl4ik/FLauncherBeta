import re
from pathlib import Path

from src.serverside.ClientManager import ClientVersion, ClientManager
from src.windows.WindowManager import WindowManager
from src.windows.download_window.FLauncherBetaDownloadWindow import FLauncherBetaDownloadWindow


class ClientUpdateManager:
    _instance = None

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True

    def check_for_update(self, remote_path: Path) -> bool | None:
        if remote_path.suffix == ".zip":
            remote_version = ClientVersion(remote_path.stem)
            client_version = ClientManager().get_client_version()
            if remote_version > client_version:
                return True
            else:
                return False
        return None

    def install_update(self, local_path: Path):
        pass

    def _on_download_update_finished(self):
        WindowManager().distruct_download_window()

    def download_update(self, remote_path: Path):
        print("1")
        window: FLauncherBetaDownloadWindow = WindowManager().create_download_window()
        window.show()
        operation_object = window.downloadFileSetup(remote_path, Path(remote_path.name))
        operation_object.finished.connect(self._on_download_update_finished)
        window.downloadFileStart(operation_object)

    def natural_sort_key(self, s: str):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]

    def sort_remote_update_file_list(self, update_file_list: list) -> list:
        update_file_list.sort(key=self.natural_sort_key)
        return update_file_list

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance