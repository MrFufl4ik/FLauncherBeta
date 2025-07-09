import os

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QPixmap, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox

from src.logs.LogManager import LogManager
from src.operatingsystem import ConfigManager
from src.serverside.FTPManager import FTPManager, FTPDownloadThread
from src.windows.downloadwindow.FLauncherBetaDownloadWindow import FLauncherBetaDownloadWindow
from src.windows.mainwindow.Window import Ui_MainWindow
from src.operatingsystem.JsonManager import writeJson, readJson

class FLauncherBetaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server_loading_window = None
        self.download_window = None
        self.ftp_manager = FTPManager()

        # UI setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._qt_setup_ui()
        self._qt_setup_connections()

    def _qt_setup_ui(self):
        """Initialize UI components"""
        self.ui.picMain.setPixmap(QPixmap(f"{os.getcwd()}/assets/background.png"))
        self.ui.inputPlayerName.setValidator(
            QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9-_]+")))
        self._load_player_data()

    def _qt_setup_connections(self):
        """Setup signal-slot connections"""
        self.ui.inputPlayerName.textChanged.connect(self._save_player_data_player_name)
        self.ui.inputPassword.textChanged.connect(self._save_player_password)
        self.ui.btnRunMinecraft.clicked.connect(self._on_run_button_clicked)


    def _load_player_data(self):
        """Load player data from JSON file"""
        player_data = readJson(ConfigManager.getPlayerDataJsonFile()) or {}
        if "name" in player_data:
            LogManager().send_info_log(f"Loaded player name from {ConfigManager.getPlayerDataJsonFile()}")
            self.ui.inputPlayerName.setText(player_data["name"])
        if "password" in player_data:
            LogManager().send_info_log(f"Loaded password from {ConfigManager.getPlayerDataJsonFile()}")
            self.ui.inputPassword.setText(player_data["password"])

    def _save_player_data_player_name(self):
        """Save player name to JSON file"""
        LogManager().send_info_log("Saving player name")
        writeJson(ConfigManager.getPlayerDataJsonFile(),
                  {"name": self.ui.inputPlayerName.text()})

    def _save_player_password(self):
        """Save player password to JSON file"""
        LogManager().send_info_log("Saving player password")
        writeJson(ConfigManager.getPlayerDataJsonFile(),
                  {"password": self.ui.inputPassword.text()})

    def _on_run_button_clicked(self):
        """Handle run button click - start modpack download"""
        if not self.ftp_manager.is_ftp_setup():
            QMessageBox.warning(
                self,
                "Ошибка",
                "FTP соединение не настроено!",
                QMessageBox.StandardButton.Ok
            )
            return

        self.download_window = FLauncherBetaDownloadWindow()
        self.download_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.download_window.show()

        # Start download
        remote_path = "modpacks/vacuumrevival/1.7z"
        local_path = f"{os.getcwd()}/1.7z"

        self.ftp_download_thread = FTPDownloadThread(remote_path, local_path)
        self.ftp_download_thread.worker.progress.connect(self.download_window.onProgressUpdate)
        self.ftp_download_thread.worker.finished.connect(self.download_window.onDownloadFinished)
        self.ftp_download_thread.worker.on_error.connect(self._handle_download_error)
        self.ftp_download_thread.start()

    def _handle_download_error(self, error_msg: str):
        LogManager().send_error_log(f"Download error: {error_msg}")
        if self.download_window:
            self.download_window.close()

        QMessageBox.critical(
            self,
            "Ошибка загрузки",
            f"Не удалось загрузить файлы: {error_msg}",
            QMessageBox.StandardButton.Ok
        )