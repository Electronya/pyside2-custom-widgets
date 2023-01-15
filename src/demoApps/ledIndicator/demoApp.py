import os
import sys

from PySide2.QtWidgets import QApplication, QMainWindow

sys.path.append(os.path.abspath('./src'))
from widgets.ledIndicator import LedIndicator, LedIndicatorColor     # noqa: E402 E501
from demoApps.ledIndicator.demoAppWindow import Ui_DemoApp


class DemoApp(QMainWindow, Ui_DemoApp):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Change the color at will from the LedIndicatorColor Enum
        self.led = LedIndicator(self, LedIndicatorColor.YEL)
        self.led.setDisabled(True)  # Make the led non clickable
        self.horizontalLayout.addWidget(self.led)

        self.pushButton.clicked.connect(lambda: self.onPressButton())

    def onPressButton(self):
        self.led.setChecked(not self.led.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DemoApp()
    form.show()
    sys.exit(app.exec_())
