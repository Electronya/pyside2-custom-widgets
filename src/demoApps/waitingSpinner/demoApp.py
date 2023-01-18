import os
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton

sys.path.append(os.path.abspath('./src'))
from widgets.waitingSpinner import WaitingSpinner                  # noqa: E402
from demoApps.waitingSpinner.demoAppUi import Ui_DemoApp           # noqa: E402


class DemoApp(QMainWindow, Ui_DemoApp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DemoApp()
    form.show()
    sys.exit(app.exec_())
