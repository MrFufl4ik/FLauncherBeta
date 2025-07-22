import os
import re
from pathlib import Path

from qasync import asyncSlot

from src.serverside.ClientManager import ClientVersion, ClientManager
from src.serverside.FTPManager import FTPAsyncListOperationObject
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

    async def update_client(self):

        remote_update_path = "/modpacks/obscurumresurgam"

        temp_path = f"{os.getcwd()}/temp"
        if not os.path.exists(temp_path): os.makedirs(temp_path)

        operation_object = FTPAsyncListOperationObject(Path(remote_update_path))

        @asyncSlot(list)
        async def on_list_operation_finished(remote_files_list: list):
            for file in ClientUpdateManager().sort_remote_update_file_list(remote_files_list):
                remote_update_file_path: Path = Path(f"{remote_update_path}/{file}")

                status: bool | None = ClientUpdateManager().check_for_update(remote_update_file_path)
                if status is not None and status:
                    print(remote_update_file_path, status)
                    # ClientUpdateManager().download_update(remote_update_file_path)

        @asyncSlot(int)
        async def on_list_operation_error(error_code: int):
            print(error_code)

        operation_object.finished.connect(on_list_operation_finished)
        operation_object.error.connect(on_list_operation_error)
        await operation_object.run()

        os.removedirs(temp_path)

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