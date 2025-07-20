import os
import webbrowser
from pathlib import Path

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QPixmap, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox

from src.logs.LogManager import LogManager
from src.operatingsystem import ConfigManager
from src.serverside.ClientManager import ClientManager
from src.serverside.ClientUpdateManager import ClientUpdateManager
from src.serverside.FTPManager import FTPManager, FTPListOperationObject, FTPOperationThread
from src.windows.WindowManager import WindowManager
from src.windows.download_window.FLauncherBetaDownloadWindow import FLauncherBetaDownloadWindow
from src.windows.main_window.Window import Ui_MainWindow
from src.operatingsystem.JsonManager import writeJson, readJson

class FLauncherBetaMainWindow(QMainWindow):
    _logger = LogManager()

    def __init__(self):
        super().__init__()
        self._thread = None
        self.ftp_manager = FTPManager()

        # UI setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._qt_setup_ui()
        self._qt_setup_connections()

    def _qt_setup_ui(self):
        self.ui.picMain.setPixmap(QPixmap(f"{os.getcwd()}/assets/background.png"))
        self.ui.picServerTitle.setPixmap(QPixmap(f"{os.getcwd()}/assets/server_title.png"))
        self.ui.inputPlayerName.setValidator(
            QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9-_]+")))
        self._load_player_data()

    def _qt_setup_connections(self):
        self.ui.inputPlayerName.textChanged.connect(self._save_player_data_player_name)
        self.ui.inputPassword.textChanged.connect(self._save_player_password)
        self.ui.btnRunMinecraft.clicked.connect(self._on_run_button_clicked)
        self.ui.btnRules.clicked.connect(self._on_rules_button_clicked)
        self.ui.btnDiscord.clicked.connect(self._on_discord_button_clicked)

    def _load_player_data(self):
        player_data = readJson(ConfigManager.getPlayerDataJsonFile()) or {}
        if "name" in player_data:
            self._logger.send_info_log(f"Loaded player name from {ConfigManager.getPlayerDataJsonFile()}")
            self.ui.inputPlayerName.setText(player_data["name"])
        if "password" in player_data:
            self._logger.send_info_log(f"Loaded password from {ConfigManager.getPlayerDataJsonFile()}")
            self.ui.inputPassword.setText(player_data["password"])

    def _save_player_data_player_name(self):
        self._logger.send_info_log(f"Saving player name to {ConfigManager.getPlayerDataJsonFile()}")
        writeJson(ConfigManager.getPlayerDataJsonFile(),{"name": self.ui.inputPlayerName.text()})

    def _save_player_password(self):
        self._logger.send_info_log(f"Saving player password to {ConfigManager.getPlayerDataJsonFile()}")
        writeJson(ConfigManager.getPlayerDataJsonFile(),{"password": self.ui.inputPassword.text()})

    def _on_rules_button_clicked(self):
        links_data = readJson(ConfigManager.getLinksDataJsonFile()) or {}
        if "rules" in links_data:
            self._logger.send_info_log(f"Open browser with url from {ConfigManager.getLinksDataJsonFile()}")
            webbrowser.open(links_data["rules"])

    def _on_discord_button_clicked(self):
        links_data = readJson(ConfigManager.getLinksDataJsonFile()) or {}
        if "discord" in links_data:
            self._logger.send_info_log(f"Open browser with url from {ConfigManager.getLinksDataJsonFile()}")
            webbrowser.open(links_data["discord"])

    def _on_run_button_clicked(self):
        self.ui.btnRunMinecraft.setEnabled(False)

        remote_update_path = "/modpacks/obscurumresurgam"

        temp_path = f"{os.getcwd()}/temp"
        if not os.path.exists(temp_path): os.makedirs(temp_path)

        operation_object = FTPListOperationObject(remote_update_path)

        def on_list_operation_finished(remote_files_list: list):
            for file in ClientUpdateManager().sort_remote_update_file_list(remote_files_list):
                remote_update_file_path: Path = Path(f"{remote_update_path}/{file}")

                status: bool | None = ClientUpdateManager().check_for_update(remote_update_file_path)
                if status is not None and status:
                    ClientUpdateManager().download_update(remote_update_file_path)

        def on_list_operation_error(error_code: int):
            print(error_code)

        operation_object.finished.connect(on_list_operation_finished)
        operation_object.error.connect(on_list_operation_error)
        self._ftp_list_operation_thread = FTPOperationThread(operation_object)
        self._ftp_list_operation_thread.start()

        os.removedirs(temp_path)