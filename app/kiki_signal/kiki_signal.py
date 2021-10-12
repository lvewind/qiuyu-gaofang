from PyQt5.QtCore import QObject, pyqtSignal


class SignalMainUI(QObject):
    refresh_text_browser = pyqtSignal(str)


signal_main_ui = SignalMainUI()
