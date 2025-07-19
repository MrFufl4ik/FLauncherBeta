import os
import socket
from ftplib import FTP, error_perm, error_temp

from typing import TypedDict, Optional, List
from PySide6.QtCore import QThread, Signal, QObject

from src.logs.LogManager import LogManager
from src.operatingsystem import ConfigManager
from src.operatingsystem.JsonManager import readJson

# FTP Status Codes
class FTPStatus:
    SUCCESS = 0
    CONFIG_ERROR = 1
    VALIDATION_ERROR = 2
    AUTH_ERROR = 3
    SERVER_ERROR = 4
    NETWORK_ERROR = 5
    UNKNOWN_ERROR = 6
    SETUP_ERROR = 7

# Error messages mapping
ERROR_MESSAGES = {
    FTPStatus.CONFIG_ERROR: (
        "Ошибка чтения JSON.",
        f"Файл {ConfigManager.getFTPDataJsonFile()} поврежден или не является JSON.",
        "FTP_CONNECT_CONFIG_ERROR"
    ),
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


class FTPConfig(TypedDict):
    ip: str
    port: int
    username: str
    password: str


class FTPManager:
    _instance = None
    _logger = LogManager()

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True
        self._server_loading_window = None
        self._check_connection_thread = None
        self.ftp_config = FTPConfig(ip="127.0.0.1", port=21, username="username", password="123")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def validate_ftp_config(self, config: dict) -> int:
        required_keys = {"ip", "port", "username", "password"}
        if not all(key in config for key in required_keys):
            self._logger.send_error_log("Missing required keys in FTP config")
            return FTPStatus.CONFIG_ERROR

        if not (isinstance(config["ip"], str) and
                isinstance(config["port"], int) and
                isinstance(config["username"], str) and
                isinstance(config["password"], str)):
            self._logger.send_error_log("Type validation failed in FTP config")
            return FTPStatus.VALIDATION_ERROR
        return FTPStatus.SUCCESS

    #FTP Setup
    def is_ftp_setup(self) -> bool:
        default_config = {"ip": "127.0.0.1", "port": 21, "username": "username", "password": "123"}
        return self.ftp_config != default_config

    def setup_ftp(self) -> int:
        _json = readJson(ConfigManager.getFTPDataJsonFile())
        if not _json:
            self._logger.send_error_log(f"Failed to read JSON file: {ConfigManager.getFTPDataJsonFile()}")
            return FTPStatus.CONFIG_ERROR
        validation_result = self.validate_ftp_config(_json)
        if validation_result != FTPStatus.SUCCESS:
            return validation_result
        self.ftp_config.update({
            "ip": _json["ip"],
            "port": _json["port"],
            "username": _json["username"],
            "password": _json["password"]
        })
        self._logger.send_success_log("FTP configuration loaded successfully")
        return FTPStatus.SUCCESS

    def connect_to_ftp(self) -> tuple[int, FTP | None]:
        try:
            ftp = FTP()
            ftp.connect(
                host=self.ftp_config["ip"],
                port=self.ftp_config["port"],
                timeout=10
            )
            ftp.login(
                user=self.ftp_config["username"],
                passwd=self.ftp_config["password"]
            )
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

    def check_connection(self) -> int:
        if not self.is_ftp_setup():
            self._logger.send_error_log("FTP is not setup properly")
            return FTPStatus.SETUP_ERROR

        self._logger.send_info_log(
            f"Attempting to first connect to FTP server: {self.ftp_config['ip']}:{self.ftp_config['port']}")

        status, ftp = self.connect_to_ftp()
        return status

    def list_files(self, remote_path: str) -> Optional[List[str]]:
        self._logger.send_info_log(f"Attempting to list files in: {remote_path}")


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
    finished = Signal(list)
    error = Signal(int)
    _logger = LogManager()

    def __init__(self, remote_path: str):
        super().__init__()
        self.remote_path = remote_path
        self._logger.send_info_log(f"Initialized FTP list operation object for {remote_path}")

    def run(self):
        status, ftp = FTPManager().connect_to_ftp()
        if ftp is None: self.error.emit(status); return
        try:
            files = ftp.nlst(self.remote_path)
            self.finished.emit(files)
        except Exception as e:
            self._logger.send_error_log(f"Failed to list files in {self.remote_path}: {str(e)}")

class FTPDownloadOperationStatus:
    EMPTY_FILE_ERROR = 8

class FTPDownloadOperationObject(FTPOperationObject):
    progress = Signal(int, int)
    finished = Signal()
    error = Signal(int)
    _logger = LogManager()

    def __init__(self, remote_path: str, local_path: str):
        super().__init__()
        self.remote_path = remote_path
        self.local_path = local_path
        self._logger.send_info_log(f"Initialized FTP download operation object for {remote_path} to {local_path}")

    def run(self):
        try:
            status, ftp = FTPManager().connect_to_ftp()
            if ftp is None: self.error.emit(status); return
            ftp.sendcmd("TYPE I")

            file_size = ftp.size(self.remote_path)
            if file_size == 0 or file_size is None:
                self._logger.send_error_log(f"Empty or invalid file size for {self.remote_path}")
                self.error.emit(FTPDownloadOperationStatus.EMPTY_FILE_ERROR)
                return

            self._logger.send_info_log(f"Downloading file (size: {file_size} bytes)")

            temp_path = self.local_path + '.part'
            with open(temp_path, 'wb') as f:
                def callback(data):
                    f.write(data)
                    downloaded = f.tell()
                    self.progress.emit(downloaded, file_size)

                ftp.retrbinary(f'RETR {self.remote_path}', callback, blocksize=8192)

            if os.path.exists(self.local_path): os.remove(self.local_path)
            os.rename(temp_path, self.local_path)

            self._logger.send_success_log(f"Successfully downloaded {self.remote_path}")
            self.finished.emit()

        except Exception as e:
            error_msg = f"Failed to download {self.remote_path}: {str(e)}"
            self._logger.send_error_log(error_msg)
            self.error.emit(error_msg)