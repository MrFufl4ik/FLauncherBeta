# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'server_loading.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(380, 60)
        Form.setMinimumSize(QSize(380, 60))
        Form.setMaximumSize(QSize(380, 60))
        Form.setStyleSheet(u"QWidget {\n"
"  background: rgb(255,255,255)\n"
"}")
        self.labelLoading = QLabel(Form)
        self.labelLoading.setObjectName(u"labelLoading")
        self.labelLoading.setGeometry(QRect(80, 15, 301, 31))
        font = QFont()
        font.setFamilies([u"JetBrains Mono SemiBold"])
        font.setPointSize(14)
        font.setBold(True)
        self.labelLoading.setFont(font)
        self.labelLoading.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.picFrog = QLabel(Form)
        self.picFrog.setObjectName(u"picFrog")
        self.picFrog.setGeometry(QRect(10, 0, 64, 64))
        self.picFrog.setStyleSheet(u"\n"
"color: rgba(0,0,0, 0)")
        self.picFrog.setPixmap(QPixmap(u"../assets/loading_frog.png"))
        self.picFrog.setScaledContents(False)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"FLauncher Beta | \u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435", None))
        self.labelLoading.setText(QCoreApplication.translate("Form", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a \u0441\u0435\u0440\u0432\u0435\u0440\u0443...", None))
        self.picFrog.setText("")
    # retranslateUi

