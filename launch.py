from app.main import Kiki
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    kiki = Kiki()
    kiki.show()
    sys.exit(app.exec_())
