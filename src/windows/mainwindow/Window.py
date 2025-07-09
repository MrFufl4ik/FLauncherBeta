# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(900, 400)
        MainWindow.setMinimumSize(QSize(900, 400))
        MainWindow.setMaximumSize(QSize(900, 400))
        MainWindow.setStyleSheet(u"")
        MainWindow.setDocumentMode(False)
        MainWindow.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks|QMainWindow.DockOption.AnimatedDocks)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet(u"QWidget {\n"
"  background-color: white;\n"
"}")
        self.btnRunMinecraft = QPushButton(self.centralwidget)
        self.btnRunMinecraft.setObjectName(u"btnRunMinecraft")
        self.btnRunMinecraft.setGeometry(QRect(470, 350, 411, 41))
        font = QFont()
        font.setFamilies([u"JetBrains Mono Medium"])
        font.setPointSize(14)
        self.btnRunMinecraft.setFont(font)
        self.btnRunMinecraft.setStyleSheet(u"QPushButton {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid #333;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #222;\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #111;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #333;\n"
"    color: #999;\n"
"}")
        self.picMain = QLabel(self.centralwidget)
        self.picMain.setObjectName(u"picMain")
        self.picMain.setGeometry(QRect(0, 0, 921, 400))
        self.picMain.setPixmap(QPixmap(u"../assets/background.png"))
        self.labelChangelog = QLabel(self.centralwidget)
        self.labelChangelog.setObjectName(u"labelChangelog")
        self.labelChangelog.setGeometry(QRect(10, 10, 441, 381))
        font1 = QFont()
        font1.setFamilies([u"JetBrains Mono"])
        self.labelChangelog.setFont(font1)
        self.labelChangelog.setAutoFillBackground(False)
        self.labelChangelog.setStyleSheet(u"    QLabel {\n"
"        color: white;\n"
"        background: rgba(0,0,0,191);\n"
"    	border: 1px solid #333;\n"
"        border-radius: 6px;\n"
"        padding: 8px 16px;\n"
"    }")
        self.labelChangelog.setTextFormat(Qt.TextFormat.MarkdownText)
        self.labelChangelog.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.btnRules = QPushButton(self.centralwidget)
        self.btnRules.setObjectName(u"btnRules")
        self.btnRules.setGeometry(QRect(730, 300, 151, 41))
        self.btnRules.setFont(font)
        self.btnRules.setStyleSheet(u"QPushButton {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid #333;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #222;\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #111;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #333;\n"
"    color: #999;\n"
"}")
        self.btnDiscord = QPushButton(self.centralwidget)
        self.btnDiscord.setObjectName(u"btnDiscord")
        self.btnDiscord.setGeometry(QRect(470, 300, 251, 41))
        self.btnDiscord.setFont(font)
        self.btnDiscord.setStyleSheet(u"QPushButton {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid #333;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #222;\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #111;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #333;\n"
"    color: #999;\n"
"}")
        self.picFrog = QLabel(self.centralwidget)
        self.picFrog.setObjectName(u"picFrog")
        self.picFrog.setGeometry(QRect(360, -20, 501, 291))
        self.picFrog.setStyleSheet(u"background: transparent; opacity: 0.5;")
        self.picFrog.setPixmap(QPixmap(u"../assets/mrfufl4ik.png"))
        self.picFrog.setScaledContents(True)
        self.picFrog.setWordWrap(False)
        self.inputPlayerName = QLineEdit(self.centralwidget)
        self.inputPlayerName.setObjectName(u"inputPlayerName")
        self.inputPlayerName.setGeometry(QRect(470, 180, 411, 51))
        self.inputPlayerName.setFont(font)
        self.inputPlayerName.setAutoFillBackground(False)
        self.inputPlayerName.setStyleSheet(u"QLineEdit {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid #333;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"    selection-background-color: #444;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background-color: #333;\n"
"    color: #999;\n"
"    border: 1px solid #444;\n"
"}")
        self.inputPassword = QLineEdit(self.centralwidget)
        self.inputPassword.setObjectName(u"inputPassword")
        self.inputPassword.setGeometry(QRect(470, 240, 411, 51))
        self.inputPassword.setFont(font)
        self.inputPassword.setAutoFillBackground(False)
        self.inputPassword.setStyleSheet(u"QLineEdit {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid #333;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"    selection-background-color: #444;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background-color: #333;\n"
"    color: #999;\n"
"    border: 1px solid #444;\n"
"}")
        self.inputPassword.setEchoMode(QLineEdit.EchoMode.Password)
        MainWindow.setCentralWidget(self.centralwidget)
        self.picMain.raise_()
        self.labelChangelog.raise_()
        self.picFrog.raise_()
        self.btnRunMinecraft.raise_()
        self.btnRules.raise_()
        self.btnDiscord.raise_()
        self.inputPlayerName.raise_()
        self.inputPassword.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FLauncher Beta", None))
        self.btnRunMinecraft.setText(QCoreApplication.translate("MainWindow", u"\u0438\u0433\u0440\u0430\u0442\u044c", None))
        self.picMain.setText("")
        self.labelChangelog.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">...</span></p></body></html>", None))
        self.btnRules.setText(QCoreApplication.translate("MainWindow", u"\u043f\u0440\u0430\u0432\u0438\u043b\u0430", None))
        self.btnDiscord.setText(QCoreApplication.translate("MainWindow", u"\u0434\u0438\u0441\u043a\u043e\u0440\u0434", None))
        self.picFrog.setText("")
        self.inputPlayerName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u043d\u0438\u043a \u0438\u0433\u0440\u043e\u043a\u0430", None))
        self.inputPassword.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u043f\u0430\u0440\u043e\u043b\u044c", None))
    # retranslateUi

