# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpinBox, QStatusBar, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(401, 725)
        MainWindow.setMinimumSize(QSize(401, 725))
        MainWindow.setMaximumSize(QSize(491, 725))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 20, 361, 71))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        self.groupBox.setFont(font)
        self.lineEdit_input_excel = QLineEdit(self.groupBox)
        self.lineEdit_input_excel.setObjectName(u"lineEdit_input_excel")
        self.lineEdit_input_excel.setGeometry(QRect(10, 30, 271, 31))
        self.lineEdit_input_excel.setFont(font)
        self.pushButton_select_excel = QPushButton(self.groupBox)
        self.pushButton_select_excel.setObjectName(u"pushButton_select_excel")
        self.pushButton_select_excel.setGeometry(QRect(280, 30, 75, 31))
        self.pushButton_select_excel.setFont(font)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 180, 361, 61))
        self.groupBox_3.setFont(font)
        self.radioButton_platform_tb = QRadioButton(self.groupBox_3)
        self.radioButton_platform_tb.setObjectName(u"radioButton_platform_tb")
        self.radioButton_platform_tb.setGeometry(QRect(10, 30, 51, 16))
        self.radioButton_platform_tb.setFont(font)
        self.radioButton_platform_tb.setChecked(True)
        self.radioButton_platform_jd = QRadioButton(self.groupBox_3)
        self.radioButton_platform_jd.setObjectName(u"radioButton_platform_jd")
        self.radioButton_platform_jd.setGeometry(QRect(70, 30, 51, 16))
        self.radioButton_platform_jd.setFont(font)
        self.radioButton_platform_pdd = QRadioButton(self.groupBox_3)
        self.radioButton_platform_pdd.setObjectName(u"radioButton_platform_pdd")
        self.radioButton_platform_pdd.setEnabled(True)
        self.radioButton_platform_pdd.setGeometry(QRect(130, 30, 61, 16))
        self.radioButton_platform_pdd.setFont(font)
        self.radioButton_platform_am = QRadioButton(self.groupBox_3)
        self.radioButton_platform_am.setObjectName(u"radioButton_platform_am")
        self.radioButton_platform_am.setEnabled(True)
        self.radioButton_platform_am.setGeometry(QRect(200, 30, 61, 16))
        self.radioButton_platform_am.setFont(font)
        self.radioButton_platform_wd = QRadioButton(self.groupBox_3)
        self.radioButton_platform_wd.setObjectName(u"radioButton_platform_wd")
        self.radioButton_platform_wd.setEnabled(False)
        self.radioButton_platform_wd.setGeometry(QRect(280, 30, 51, 16))
        self.radioButton_platform_wd.setFont(font)
        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setGeometry(QRect(20, 250, 61, 31))
        self.pushButton_start.setFont(font)
        self.pushButton_pause = QPushButton(self.centralwidget)
        self.pushButton_pause.setObjectName(u"pushButton_pause")
        self.pushButton_pause.setGeometry(QRect(90, 250, 61, 31))
        self.pushButton_pause.setFont(font)
        self.pushButton_stop = QPushButton(self.centralwidget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setGeometry(QRect(230, 250, 61, 31))
        self.pushButton_stop.setFont(font)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 290, 361, 411))
        self.textBrowser.setFont(font)
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(20, 100, 361, 71))
        self.groupBox_4.setFont(font)
        self.spinBox_sales_count = QSpinBox(self.groupBox_4)
        self.spinBox_sales_count.setObjectName(u"spinBox_sales_count")
        self.spinBox_sales_count.setGeometry(QRect(70, 30, 101, 31))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(12)
        self.spinBox_sales_count.setFont(font1)
        self.spinBox_sales_count.setMaximum(9999)
        self.spinBox_sales_count.setValue(384)
        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 30, 54, 31))
        self.label_5.setFont(font)
        self.pushButton_continue = QPushButton(self.centralwidget)
        self.pushButton_continue.setObjectName(u"pushButton_continue")
        self.pushButton_continue.setGeometry(QRect(160, 250, 61, 31))
        self.pushButton_continue.setFont(font)
        self.pushButton_confirm = QPushButton(self.centralwidget)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setGeometry(QRect(320, 250, 61, 31))
        self.pushButton_confirm.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"kiki\u70f9\u5c0f\u9c9c", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u4ea7\u54c1\u5217\u8868EXCEL", None))
        self.pushButton_select_excel.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5e73\u53f0\u9009\u62e9", None))
        self.radioButton_platform_tb.setText(QCoreApplication.translate("MainWindow", u"\u6dd8\u5b9d", None))
        self.radioButton_platform_jd.setText(QCoreApplication.translate("MainWindow", u"\u4eac\u4e1c", None))
        self.radioButton_platform_pdd.setText(QCoreApplication.translate("MainWindow", u"\u62fc\u591a\u591a", None))
        self.radioButton_platform_am.setText(QCoreApplication.translate("MainWindow", u"\u4e9a\u9a6c\u900a", None))
        self.radioButton_platform_wd.setText(QCoreApplication.translate("MainWindow", u"\u5fae\u5e97", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.pushButton_pause.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u8981\u91c7\u96c6\u7684\u6837\u672c\u6570\u91cf(\u6837\u672c\u6570\u91cf\u8d8a\u5927\uff0c\u82b1\u8d39\u65f6\u95f4\u8d8a\u591a)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u6837\u672c\u6570\u91cf", None))
        self.pushButton_continue.setText(QCoreApplication.translate("MainWindow", u"\u7ee7\u7eed", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4", None))
    # retranslateUi

