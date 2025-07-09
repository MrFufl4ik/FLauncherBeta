import os
from ftplib import FTP, error_perm, error_temp
import socket
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
        f"Файл {ConfigManager.getFTPJsonFile()} поврежден или не является JSON.",
        "FTP_CONNECT_CONFIG_ERROR"
    ),
    FTPStatus.VALIDATION_ERROR: (
        "Ошибка валидации JSON.",
        f"Данные из {ConfigManager.getFTPJsonFile()} имеют неправильную типизацию.",
        "FTP_CONNECT_VALIDATION_ERROR"
    ),
    FTPStatus.AUTH_ERROR: (
        "Ошибка аутентификации.",
        f"Данные {ConfigManager.getFTPJsonFile()} повреждены или изменены.",
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

        self._logger.send_success_log("FTP config validation passed")
        return FTPStatus.SUCCESS

    #FTP Setup
    def is_ftp_setup(self) -> bool:
        default_config = {"ip": "127.0.0.1", "port": 21, "username": "username", "password": "123"}
        return self.ftp_config != default_config

    def setup_ftp(self) -> int:
        self._logger.send_info_log("Setting up FTP configuration")

        _json = readJson(ConfigManager.getFTPJsonFile())
        if not _json:
            self._logger.send_error_log(f"Failed to read JSON file: {ConfigManager.getFTPJsonFile()}")
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

    def check_connection(self) -> int:
        if not self.is_ftp_setup():
            self._logger.send_error_log("FTP is not setup properly")
            return FTPStatus.SETUP_ERROR

        self._logger.send_info_log(
            f"Attempting to connect to FTP server: {self.ftp_config['ip']}:{self.ftp_config['port']}")

        try:
            with FTP() as ftp:
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
                return FTPStatus.SUCCESS
        except error_perm as e:
            self._logger.send_error_log(f"FTP authentication error: {str(e)}")
            return FTPStatus.AUTH_ERROR
        except error_temp as e:
            self._logger.send_error_log(f"FTP server error: {str(e)}")
            return FTPStatus.SERVER_ERROR
        except (socket.timeout, socket.gaierror) as e:
            self._logger.send_error_log(f"Network error: {str(e)}")
            return FTPStatus.NETWORK_ERROR
        except Exception as e:
            self._logger.send_error_log(f"Unknown FTP error: {str(e)}")
            return FTPStatus.UNKNOWN_ERROR

    #Main ftp operations
    def list_files(self, remote_path: str) -> Optional[List[str]]:
        """List files in remote FTP directory"""
        self._logger.send_info_log(f"Attempting to list files in: {remote_path}")

        try:
            with FTP() as ftp:
                ftp.connect(
                    host=self.ftp_config["ip"],
                    port=self.ftp_config["port"],
                    timeout=10
                )
                ftp.login(
                    user=self.ftp_config["username"],
                    passwd=self.ftp_config["password"]
                )
                files = ftp.nlst(remote_path)
                self._logger.send_success_log(f"Found {len(files)} files in {remote_path}")
                return files

        except Exception as e:
            self._logger.send_error_log(f"Failed to list files in {remote_path}: {str(e)}")
            return None


class FTPDownloader(QObject):
    """FTP file downloader with progress tracking"""
    progress = Signal(int, int)  # downloaded, total
    finished = Signal()
    error = Signal(str)
    _logger = LogManager()

    def __init__(self, remote_path: str, local_path: str):
        super().__init__()
        self.remote_path = remote_path
        self.local_path = local_path
        self._logger.send_info_log(f"Initialized FTP downloader for {remote_path} -> {local_path}")

    def run(self):
        """Execute the file download"""
        self._logger.send_info_log(f"Starting download of {self.remote_path}")

        try:
            with FTP() as ftp:
                # Connect to FTP server
                ftp.connect(
                    host=FTPManager().ftp_config["ip"],
                    port=FTPManager().ftp_config["port"],
                    timeout=10
                )
                ftp.login(
                    user=FTPManager().ftp_config["username"],
                    passwd=FTPManager().ftp_config["password"]
                )

                # Get file size
                ftp.sendcmd("TYPE I")
                file_size = ftp.size(self.remote_path)

                if file_size == 0 or file_size is None:
                    error_msg = f"Empty or invalid file size for {self.remote_path}"
                    self._logger.send_error_log(error_msg)
                    self.error.emit(error_msg)
                    return

                self._logger.send_info_log(f"Downloading file (size: {file_size} bytes)")

                # Download to temporary file
                temp_path = self.local_path + '.part'
                with open(temp_path, 'wb') as f:
                    def callback(data):
                        f.write(data)
                        downloaded = f.tell()
                        self.progress.emit(downloaded, file_size)

                    ftp.retrbinary(f'RETR {self.remote_path}', callback, blocksize=8192)

                # Rename temporary file to final name
                if os.path.exists(self.local_path):
                    os.remove(self.local_path)
                os.rename(temp_path, self.local_path)

                self._logger.send_success_log(f"Successfully downloaded {self.remote_path}")
                self.finished.emit()

        except Exception as e:
            error_msg = f"Failed to download {self.remote_path}: {str(e)}"
            self._logger.send_error_log(error_msg)
            self.error.emit(error_msg)


class FTPDownloadThread(QThread):
    """Thread wrapper for FTPDownloader"""

    def __init__(self, remote_path: str, local_path: str):
        super().__init__()
        self.worker = FTPDownloader(remote_path, local_path)
        self.worker.moveToThread(self)
        self._logger = LogManager()
        self._logger.send_info_log(f"Created download thread for {remote_path}")

    def run(self):
        self._logger.send_info_log("Starting download thread")
        self.worker.run()
