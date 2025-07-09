import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

from src.serverside.loading_window.Window import Ui_Form

class FLauncherBetaServerLoadingWindow(QWidget):
    def __init__(self):
        super(FLauncherBetaServerLoadingWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.picFrog.setPixmap(QPixmap(f"{os.getcwd()}/assets/loading_frog.png"))


