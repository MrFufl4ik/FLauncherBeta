import sys

from PySide6.QtWidgets import QApplication
from src.logs.LogManager import LogManager
from src.serverside.ServerManager import ServerManager
from src.windows.WindowManager import WindowManager

class Application:
    """Main application class implementing Singleton pattern"""
    _instance = None

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self._qt_app = None
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
        """Initialize QT application framework"""
        LogManager().send_info_log("Creating QApplication instance")
        self._qt_app = QApplication(sys.argv)
        LogManager().send_info_log("QApplication initialized successfully")

    def _initialize_main_window(self):
        """Create and show main application window"""
        LogManager().send_info_log("Initializing main application window")
        self._main_window = WindowManager().create_main_window()
        LogManager().send_info_log("Main window created and ready")

    def _initialize_servers(self):
        """Initialize all server components"""
        LogManager().send_info_log("Starting server initialization")
        ServerManager().servers_initialize()
        LogManager().send_info_log("All servers initialized successfully")

    def _run_application(self):
        """Start main application event loop"""
        LogManager().send_info_log("Starting application main loop")
        try:
            exit_code = self._qt_app.exec()
            self.exit(exit_code)
        except Exception as e:
            LogManager().send_error_log(f"Critical error in main loop: {str(e)}")
            raise

    def exit(self, exit_code: int):
        """Handle application shutdown with proper logging"""
        if exit_code == 0:
            LogManager().send_info_log("Application shutdown completed successfully")
        else:
            LogManager().send_warn_log(
                f"Application exited with non-zero code: {exit_code}. "
                "There might be some issues during runtime."
            )
        sys.exit(exit_code)