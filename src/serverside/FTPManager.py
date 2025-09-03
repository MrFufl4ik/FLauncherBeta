import os
import socket

from ftplib import FTP, error_perm, error_temp
from pathlib import Path
import aioftp
from PySide6.QtCore import QThread, Signal, QObject

from src.utils.JsonManager import read_json
from src.utils.LogManager import LogManager
from src.utils import ConfigManager, ErrorHelper

class FTPStatus:
    SUCCESS = 0
    CONFIG_ERROR = 1
    VALIDATION_ERROR = 2
    AUTH_ERROR = 3
    SERVER_ERROR = 4
    NETWORK_ERROR = 5
    UNKNOWN_ERROR = 6
    SETUP_ERROR = 7

ERROR_MESSAGES = {
    FTPStatus.VALIDATION_ERROR: (
        "Ошибка валидации JSON.",
        f"Данные из {ConfigManager.getFTPDataJsonFile()} имеют неправильную типизацию.",
        "FTP_CONNECT_VALIDATION_ERROR"
    ),
    FTPStatus.AUTH_ERROR: (
        "Ошибка аутентификации.",
        f"Данные {ConfigManager.getFTPDataJsonFile()} повреждены или изменены.",
        "FTP_CONNECT_AUTH_ERROR"
    ),
    FTPStatus.SERVER_ERROR: (
        "Ошибка сервера.",
        "Не удалось подключиться к серверу.",
        "FTP_CONNECT_SERVER_ERROR"
    ),
    FTPStatus.NETWORK_ERROR: (
        "Ошибка соединения.",
        "Проблемы с сетевым подключением.",
        "FTP_CONNECT_NETWORK_ERROR"
    )
}


class FTPConfig:
    ip: str
    port: int
    username: str
    password: str

    def __init__(self, ip: str, port: int, username: str, password: str):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def is_valid(self):
        return not all(key is None for key in [self.ip, self.port, self.username, self.password])


class FTPManager:
    _instance = None
    _logger = LogManager()

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True
        self.ftp_config: FTPConfig

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_current_ftp_config_valid(self, config: FTPConfig) -> int:
        return config is not None and config.is_valid()

    def setting_up_ftp(self) -> int:
        json: dict = read_json(ConfigManager.getFTPDataJsonFile())
        new_config : FTPConfig = FTPConfig(
            json["ip"],       json["port"],
            json["username"], json["password"]
        )
        if not self.is_current_ftp_config_valid(new_config): return FTPStatus.VALIDATION_ERROR
        self.ftp_config = new_config
        self._logger.send_success_log("FTP configuration loaded successfully")
        return FTPStatus.SUCCESS

    def connect_to_ftp(self) -> tuple[int, FTP | None]:
        try:
            ftp = FTP()
            ftp.connect(host=self.ftp_config.ip, port=self.ftp_config.port, timeout=10)
            ftp.login(self.ftp_config.username, self.ftp_config.password)
            welcome_msg = ftp.getwelcome()
            self._logger.send_success_log(f"Connected to FTP server. Welcome message: {welcome_msg}")
            return FTPStatus.SUCCESS, ftp
        except error_perm as e:
            self._logger.send_error_log(f"FTP authentication error: {str(e)}")
            return FTPStatus.AUTH_ERROR, None
        except error_temp as e:
            self._logger.send_error_log(f"FTP server error: {str(e)}")
            return FTPStatus.SERVER_ERROR, None
        except (socket.timeout, socket.gaierror) as e:
            self._logger.send_error_log(f"Network error: {str(e)}")
            return FTPStatus.NETWORK_ERROR, None
        except Exception as e:
            self._logger.send_error_log(f"Unknown FTP error: {str(e)}")
            return FTPStatus.UNKNOWN_ERROR, None

    async def connect_to_ftp_async(self) -> tuple[int, aioftp.Client | None]:
        try:
            ftp = aioftp.Client()
            await ftp.connect(self.ftp_config.ip, self.ftp_config.port)
            await ftp.login(self.ftp_config.username, self.ftp_config.password)
            self._logger.send_success_log(f"Connected to FTP server.")
            return FTPStatus.SUCCESS, ftp
        except aioftp.errors.StatusCodeError as e:
            if "530" in str(e):
                self._logger.send_error_log(f"FTP authentication error: {str(e)}")
                return FTPStatus.AUTH_ERROR, None
            else:
                self._logger.send_error_log(f"FTP server error: {str(e)}")
                return FTPStatus.SERVER_ERROR, None
        except (TimeoutError, OSError) as e:
            self._logger.send_error_log(f"Network error: {str(e)}")
            return FTPStatus.NETWORK_ERROR, None
        except Exception as e:
            self._logger.send_error_log(f"Unknown FTP error: {str(e)}")
            return FTPStatus.UNKNOWN_ERROR, None

    def check_connection(self) -> int:
        if self.ftp_config is None or not self.ftp_config.is_valid():
            self._logger.send_error_log("FTP is not setup properly")
            return FTPStatus.SETUP_ERROR

        self._logger.send_info_log(
            f"Attempting to first connect to FTP server: {self.ftp_config.ip}:{self.ftp_config.port}")

        status, ftp = self.connect_to_ftp()
        return status

class FTPOperationObject(QObject):
    def run(self): pass

class FTPOperationThread(QThread):
    def __init__(self, operation_object: FTPOperationObject):
        super().__init__()
        self.worker = operation_object
        self.worker.moveToThread(self)
        self._logger = LogManager()

    def run(self):
        self._logger.send_info_log(f"Starting operation thread for {id(self.worker)}: operation object")
        self.worker.run()

class FTPIsDirectoryOperationObject(FTPOperationObject):
    finished = Signal(bool)
    error = Signal(int)
    _logger = LogManager()

    def __init__(self, remote_path: str):
        super().__init__()
        self.remote_path = remote_path
        self._logger.send_info_log(f"Initialized FTP is directory operation object for {remote_path}")

    def run(self):
        status, ftp = FTPManager().connect_to_ftp()
        if ftp is None: self.error.emit(status); return
        try:
            response = ftp.sendcmd(f'MLST {self.remote_path}')
            self.finished.emit('type=dir' in response or 'type=cdir' in response or 'type=pdir' in response)
        except Exception as e:
            self._logger.send_error_log(f"Failed to check remote path of directory: {e}")
            self.finished.emit(False)

class FTPListOperationObject(FTPOperationObject):
    finished: Signal    = Signal(list)
    error: Signal       = Signal(int)
    _logger: LogManager = LogManager()

    def __init__(self, remote_path: Path):
        super().__init__()
        self.remote_path: Path = remote_path
        self._logger.send_info_log(f"Initialized FTP list operation object for {str(remote_path)}")

    def run(self):
        status, ftp = FTPManager().connect_to_ftp()
        if ftp is None: self.error.emit(status); return
        try:
            files = ftp.nlst(str(self.remote_path))
            self.finished.emit(files)
        except Exception as e:
            self._logger.send_error_log(f"Failed to list files in {str(self.remote_path)}: {str(e)}")
            self.error.emit(ErrorHelper.convert_string_to_int(str(e)))

class FTPAsyncListOperationObject(FTPOperationObject):
    finished: Signal    = Signal(list)
    error: Signal       = Signal(int)
    _logger: LogManager = LogManager()

    def __init__(self, remote_path: Path):
        super().__init__()
        self.remote_path: Path = remote_path
        self._logger.send_info_log(f"Initialized FTP list operation object for {str(remote_path)}")

    async def run(self):
        status, ftp = await FTPManager().connect_to_ftp_async()
        if ftp is None: self.error.emit(status); return
        try:
            files = []
            async for entry in ftp.list(str(self.remote_path)):
                entry_full_path: str = entry[0].as_posix()
                entry_metadata: dict[str, str | int] = entry[1]

                if entry_metadata["type"] == "file": files.append(entry_full_path)
                elif entry_metadata["type"] == "dir": files.append(entry_full_path)
            self.finished.emit(files)
        except Exception as e:
            self._logger.send_error_log(f"Failed to list files in {str(self.remote_path)}: {str(e)}")

class FTPDownloadOperationStatus:
    EMPTY_FILE_ERROR = 8
    UNKNOWN_FILE_ERROR = 9

class FTPDownloadOperationObject(FTPOperationObject):
    progress = Signal(int, int)
    finished = Signal()
    error = Signal(int)
    _logger = LogManager()

    def __init__(self, remote_path: Path, local_path: Path):
        super().__init__()
        self._remote_path = str(remote_path)
        self._local_path = str(local_path)
        self._logger.send_info_log(f"Initialized FTP download operation object for {remote_path} to {local_path}")

    def run(self):
        try:
            status, ftp = FTPManager().connect_to_ftp()
            if ftp is None: self.error.emit(status); return
            ftp.sendcmd("TYPE I")

            file_size = ftp.size(self._remote_path)
            if file_size == 0 or file_size is None:
                self._logger.send_error_log(f"Empty or invalid file size for {self._remote_path}")
                self.error.emit(FTPDownloadOperationStatus.EMPTY_FILE_ERROR)
                return

            self._logger.send_info_log(f"Downloading file (size: {file_size} bytes)")

            temp_path = self._local_path + '.part'
            with open(temp_path, 'wb') as f:
                def callback(data):
                    f.write(data)
                    downloaded = f.tell()
                    self.progress.emit(downloaded, file_size)

                ftp.retrbinary(f'RETR {self._remote_path}', callback, blocksize=8192)

            if os.path.exists(self._local_path): os.remove(self._local_path)
            os.rename(temp_path, self._local_path)

            self._logger.send_success_log(f"Successfully downloaded {self._remote_path}")
            self.finished.emit()

        except Exception as e:
            self._logger.send_error_log(f"Failed to download {self._remote_path}: {str(e)}")
            self.error.emit(FTPDownloadOperationStatus.UNKNOWN_FILE_ERROR)