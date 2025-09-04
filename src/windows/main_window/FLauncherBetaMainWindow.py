import asyncio
import os
import webbrowser

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QPixmap, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow
from qasync import asyncSlot

from src.utils.LogManager import LogManager
from src.utils import ConfigManager
from src.serverside.ClientUpdateManager import ClientUpdateManager
from src.serverside.FTPManager import FTPManager
from src.windows.main_window.Window import Ui_MainWindow
from src.utils.JsonManager import write_json, read_json


class FLauncherBetaMainWindow(QMainWindow):
    _logger = LogManager()

    def __init__(self):
        super().__init__()
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
        self.ui.btnRunMinecraft.clicked.connect(lambda: asyncio.ensure_future(self._on_run_button_clicked()))
        self.ui.btnRules.clicked.connect(self._on_rules_button_clicked)
        self.ui.btnDiscord.clicked.connect(self._on_discord_button_clicked)

    def _load_player_data(self):
        player_data = read_json(ConfigManager.getPlayerDataJsonFile()) or {}
        if "name" in player_data:
            self._logger.send_info_log(f"Loaded player name from {ConfigManager.getPlayerDataJsonFile()}")
            self.ui.inputPlayerName.setText(player_data["name"])
        if "password" in player_data:
            self._logger.send_info_log(f"Loaded password from {ConfigManager.getPlayerDataJsonFile()}")
            self.ui.inputPassword.setText(player_data["password"])

    def _save_player_data_player_name(self):
        self._logger.send_info_log(f"Saving player name to {ConfigManager.getPlayerDataJsonFile()}")
        write_json(ConfigManager.getPlayerDataJsonFile(), {"name": self.ui.inputPlayerName.text()})

    def _save_player_password(self):
        self._logger.send_info_log(f"Saving player password to {ConfigManager.getPlayerDataJsonFile()}")
        write_json(ConfigManager.getPlayerDataJsonFile(), {"password": self.ui.inputPassword.text()})

    def _on_rules_button_clicked(self):
        links_data = read_json(ConfigManager.getLinksDataJsonFile()) or {}
        if "rules" in links_data:
            self._logger.send_info_log(f"Open browser with url from {ConfigManager.getLinksDataJsonFile()}")
            webbrowser.open(links_data["rules"])

    def _on_discord_button_clicked(self):
        links_data = read_json(ConfigManager.getLinksDataJsonFile()) or {}
        if "discord" in links_data:
            self._logger.send_info_log(f"Open browser with url from {ConfigManager.getLinksDataJsonFile()}")
            webbrowser.open(links_data["discord"])

    @asyncSlot()
    async def _on_run_button_clicked(self):
        self.ui.btnRunMinecraft.setEnabled(False)
        await ClientUpdateManager().update_client()
        self.ui.btnRunMinecraft.setEnabled(True)