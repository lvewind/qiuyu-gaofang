from app.ui.main import Ui_MainWindow
from PySide6 import QtWidgets
from app.web_control.web_control import KikiDriver
from app.kiki_signal.kiki_signal import signal_main_ui
from threading import Thread


class Kiki(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Kiki, self).__init__()
        self.setupUi(self)
        self.excel_input_path = ""
        self.bind_func()
        self.kiki = KikiDriver()

    def bind_func(self):
        self.pushButton_select_excel.clicked.connect(self.select_excel)
        self.pushButton_start.clicked.connect(self.start_get)
        self.pushButton_stop.clicked.connect(self.stop_get)
        self.pushButton_pause.clicked.connect(self.pause_get)
        self.pushButton_continue.clicked.connect(self.continue_get)
        self.pushButton_confirm.clicked.connect(self.set_login_true)
        signal_main_ui.refresh_text_browser.connect(self.display_info)

    def select_excel(self):
        openfile_name, openfile_type = QtWidgets.QFileDialog.getOpenFileName(self, caption='选择excel数据表', filter="Excel Files (*.xls), (*.xlsx)")
        if openfile_name:
            self.lineEdit_input_excel.setText(openfile_name)
            self.excel_input_path = openfile_name
        return openfile_name

    def get_sales_volume_low(self):
        return self.spinBox_sales_volume_low.value()

    def get_sales_volume_high(self):
        return self.spinBox_sales_volume_high.value()

    def get_platform(self):
        if self.radioButton_platform_tb.isChecked():
            return "tb"
        elif self.radioButton_platform_jd.isChecked():
            return "jd"
        elif self.radioButton_platform_pdd.isChecked():
            return "pdd"
        elif self.radioButton_platform_am.isChecked():
            return "am"
        elif self.radioButton_platform_wd.isChecked():
            return "wd"

    def start_get(self):
        if self.excel_input_path:
            platform = self.get_platform()
            target_count = self.spinBox_sales_count.value()
            Thread(target=self.kiki.run_get, args=(self.excel_input_path, platform, target_count)).start()

        else:
            self.display_info("未选择\'.xlsx\'数据源文件")

    def stop_get(self):
        self.kiki.stop = True

    def pause_get(self):
        self.kiki.pause = True

    def continue_get(self):
        self.kiki.pause = False

    def set_login_true(self):
        self.kiki.is_pdd_login = True
        self.kiki.is_am_login = True

    def display_info(self, info):
        self.textBrowser.append(info)
