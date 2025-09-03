from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from src.utils.LogManager import LogManager
from src.serverside.FTPManager import FTPManager, ERROR_MESSAGES, FTPStatus
from src.windows.WindowManager import WindowManager
from src.windows.main_window.FLauncherBetaMainWindow import FLauncherBetaMainWindow
from src.windows.loading_window.FLauncherBetaServerLoadingWindow import FLauncherBetaServerLoadingWindow


class ServerManager:
    _instance = None
    _logger = LogManager()

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True
        self._check_connection_thread = None
        self._server_loading_window = None
        self._main_window = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def servers_initialize(self):
        self._logger.send_info_log("Started servers init process")
        self._main_window: FLauncherBetaMainWindow = WindowManager().create_main_window()
        self._server_loading_window: FLauncherBetaServerLoadingWindow = WindowManager().create_server_loading_window()
        self._server_loading_window.show()

        self.ftp_initialize()

    def ftp_print_error_message(self, result: int) -> None:
        if result in ERROR_MESSAGES:
            title, message, error_code = ERROR_MESSAGES[result]

            self._logger.send_error_log(
                f"FTP connection failed with error {error_code}: {title} - {message}"
            )

            QMessageBox.critical(
                None,
                f"{title} | FLauncher Beta",
                f"{message}\nЛаунчер не может продолжить работу!\n\nКод ошибки: {error_code}"
            )

    def ftp_initialize(self):
        self._logger.send_info_log("Start ftp check connection")
        FTPManager().setting_up_ftp()
        self._check_connection_thread = FTPCheckConnectionThread()
        self._check_connection_thread.on_finished.connect(self.on_ftp_init_finished_handle)
        self._check_connection_thread.on_error.connect(self.on_ftp_error_handle)
        self._check_connection_thread.start()

    def on_ftp_init_finished_handle(self):
        self._main_window.show()
        self._server_loading_window.close()
        WindowManager().distruct_server_loading_window()

    def on_ftp_error_handle(self, result: int):
        self._logger.send_info_log("An error has been detected, starting print")
        WindowManager().get_server_loading_window().close()
        self.ftp_print_error_message(result)
        from src.Application import Application
        Application().exit(result)

class FTPCheckConnectionThread(QThread):
    on_finished = Signal()
    on_error = Signal(int)
    _logger = LogManager()

    def __init__(self):
        super().__init__()
        self._logger.send_info_log("FTP connection checker thread initialized")

    def run(self):
        self._logger.send_info_log("Starting FTP connection check thread")
        ftp_manager = FTPManager()
        result = ftp_manager.setting_up_ftp()
        if result != FTPStatus.SUCCESS:
            self.on_error.emit(result)
            return
        result = ftp_manager.check_connection()
        if result != FTPStatus.SUCCESS:
            self.on_error.emit(result)
            return
        self.on_finished.emit()