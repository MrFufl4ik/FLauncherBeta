from fileinput import close

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from src.serverside.FTPManager import FTPDownloadOperationObject, FTPOperationThread
from src.windows.WindowManager import WindowManager
from src.windows.downloadwindow.Window import Ui_Form


class FLauncherBetaDownloadWindow(QWidget):
    def __init__(self):
        super(FLauncherBetaDownloadWindow, self).__init__()
        self._download_operation_thread = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.isDownloadActivate = False
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.progressBar.setValue(85)
        self.closeable = False

    def closeEvent(self, event):
        if not self.closeable: event.ignore()
        else: close()

    def customClose(self):
        if not self.closeable:
            self.closeable = True
            self.close()

    def downloadFileSetup(self, remote_path: str, local_path: str) -> FTPDownloadOperationObject | None:
        if self.isDownloadActivate: return None
        operation_object = FTPDownloadOperationObject(remote_path, local_path)
        operation_object.finished.connect(self._onDownloadFinished)
        operation_object.progress.connect(self._onProgressUpdate)
        return operation_object

    def downloadFileStart(self, operation_object: FTPDownloadOperationObject):
        if self.isDownloadActivate: return None
        self._download_operation_thread = FTPOperationThread(operation_object)
        self._download_operation_thread.start()
        self.isDownloadActivate = True

    def _onDownloadFinished(self):
        self.isDownloadActivate = False

    def _onProgressUpdate(self, downloaded, file_size):
        self.ui.labelStatus.setText(f"{downloaded}/{file_size} B")

        self.ui.progressBar.setMaximum(file_size)
        self.ui.progressBar.setValue(downloaded)
