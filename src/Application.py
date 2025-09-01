import asyncio
import sys
from os import confstr_names
from traceback import format_exception
from types import TracebackType

from PySide6.QtWidgets import QMessageBox
from qasync import QEventLoop, QApplication

from src.utils.LogManager import LogManager
from src.serverside.ServerManager import ServerManager
from src.windows.WindowManager import WindowManager

class Application:
    _instance = None

    def __init__(self):
        if hasattr(self, '_initialized'): return

        self._initialized = True
        self._qt_app = None
        self._qt_loop = None
        self._main_window = None

        LogManager().send_info_log("Initializing application components")
        self._initialize_qt_application()
        self._initialize_main_window()
        self._initialize_servers()
        self._run_application()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            LogManager().send_info_log("Creating new application instance")
        return cls._instance

    def _initialize_qt_application(self):
        LogManager().send_info_log("Creating QApplication instance")
        self._qt_app = QApplication(sys.argv)
        LogManager().send_success_log("QApplication initialized successfully")

    def _initialize_main_window(self):
        LogManager().send_info_log("Initializing main application window")
        self._main_window = WindowManager().create_main_window()
        LogManager().send_success_log("Main window created and ready")

    def _initialize_servers(self):
        LogManager().send_info_log("Starting server initialization")
        ServerManager().servers_initialize()
        LogManager().send_success_log("All servers initialized successfully")

    def _run_application(self):
        LogManager().send_info_log("Starting application main loop")
        self._qt_loop = QEventLoop(self._qt_app)
        asyncio.set_event_loop(self._qt_loop)
        sys.excepthook = self.global_error_handle
        with self._qt_loop:
            exit_code: int = self._qt_loop.run_forever()
            self.exit(exit_code)

    def global_error_handle(self, exception_type: any, exception_value: any, exception_traceback: TracebackType):
        QMessageBox.critical(None, "Error has been handle!", str(exception_type) + " | " + str(exception_value))
        self.exit(-1)

    def exit(self, exit_code: int):
        if exit_code == 0: LogManager().send_info_log("Application shutdown completed successfully")
        else:
            LogManager().send_warn_log(
                f"Application exited with non-zero code: {exit_code}. "
                "There might be some issues during runtime."
            )
        sys.exit(exit_code)