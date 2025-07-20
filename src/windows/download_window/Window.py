# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_window.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(320, 100)
        Form.setMinimumSize(QSize(320, 100))
        Form.setMaximumSize(QSize(320, 100))
        Form.setStyleSheet(u"QWidget {\n"
"  background: rgb(255,255,255)\n"
"}")
        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 70, 300, 20))
        font = QFont()
        font.setFamilies([u"JetBrains Mono Medium"])
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid #333;\n"
"    border-radius: 6px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #444;\n"
"    border-radius: 5px; /* \u0427\u0443\u0442\u044c \u043c\u0435\u043d\u044c\u0448\u0435, \u0447\u0435\u043c \u0443 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0433\u043e \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441-\u0431\u0430\u0440\u0430 */\n"
"    border: 1px solid #555;\n"
"}\n"
"\n"
"QProgressBar:disabled {\n"
"    background-color: #333;\n"
"    color: #999;\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"QProgressBar::chunk:disabled {\n"
"    background-color: #555;\n"
"    border: 1px solid #666;\n"
"}")
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(40)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(Qt.Orientation.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QProgressBar.Direction.TopToBottom)
        self.labelMain = QLabel(Form)
        self.labelMain.setObjectName(u"labelMain")
        self.labelMain.setGeometry(QRect(10, 10, 301, 31))
        font1 = QFont()
        font1.setFamilies([u"JetBrains Mono SemiBold"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.labelMain.setFont(font1)
        self.labelMain.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.labelStatus = QLabel(Form)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setGeometry(QRect(10, 46, 301, 20))
        font2 = QFont()
        font2.setFamilies([u"JetBrains Mono SemiBold"])
        font2.setPointSize(9)
        font2.setBold(True)
        self.labelStatus.setFont(font2)
        self.labelStatus.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"FLauncher Beta | \u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430", None))
        self.progressBar.setFormat(QCoreApplication.translate("Form", u"%p%", None))
        self.labelMain.setText(QCoreApplication.translate("Form", u"Winrar.7z", None))
        self.labelStatus.setText(QCoreApplication.translate("Form", u"10/1024 MB", None))
    # retranslateUi

