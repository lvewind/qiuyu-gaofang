from PySide6.QtCore import QObject, Signal


class SignalMainUI(QObject):
    refresh_text_browser = Signal(str)


signal_main_ui = SignalMainUI()
