from PySide6.QtWidgets import QWidget

from src.windows.downloadwindow.Window import Ui_Form


class FLauncherBetaDownloadWindow(QWidget):
    def __init__(self):
        super(FLauncherBetaDownloadWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(85)
        self.closeable = False

    def closeEvent(self, event):
        if not self.closeable: event.ignore()

    def onProgressUpdate(self, downloaded, file_size):
        self.ui.labelStatus.setText(f"{downloaded}/{file_size} B")

        self.ui.progressBar.setMaximum(file_size)
        self.ui.progressBar.setValue(downloaded)

    def onDownloadFinished(self):
        self.closeable = True
        self.close()