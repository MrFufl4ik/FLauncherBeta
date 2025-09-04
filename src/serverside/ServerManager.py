from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox

from src.utils.LogManager import LogManager
from src.serverside.FTPManager import FTPManager, ERROR_MESSAGES, FTPStatus, FTPOperationObject, FTPOperationThread, \
    FTPCheckConnectionOperationObject
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

    def ftp_initialize(self):
        self._logger.send_info_log("Start ftp check connection")
        FTPManager().setting_up_ftp_config()
        check_connection_object = FTPCheckConnectionOperationObject()
        check_connection_object.on_finished.connect(self.on_ftp_init_finished_handle)
        self._check_connection_thread = FTPOperationThread(check_connection_object)
        self._check_connection_thread.start()

    def on_ftp_init_finished_handle(self, result: bool):
        self._main_window.show()
        self._server_loading_window.close()
        WindowManager().distruct_server_loading_window()