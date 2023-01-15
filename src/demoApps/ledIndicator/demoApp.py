import os
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton

sys.path.append(os.path.abspath('./src'))
from widgets.ledIndicator import LedIndicator, LedIndicatorColor   # noqa: E402
from demoApps.ledIndicator.demoAppUi import Ui_DemoApp             # noqa: E402


class DemoApp(QMainWindow, Ui_DemoApp):
    def __init__(self):
        super(self.__class__, self).__init__()

        # LedIndicator creation. Here one of each color is created in a for
        # loop, but they can be individually created by the following:
        # self.led = LedIndicator(self, LedIndicatorColor.YEL)
        self.leds: list[LedIndicator] = []
        for idx, color in enumerate(LedIndicatorColor):
            self.leds.append(LedIndicator(self, color))
            self.leds[idx].setDisabled(True)    # Make the led non clickable.

        self.setupUi(self, len(self.leds))

        # Adding the leds to the layout.
        for idx, led in enumerate(self.leds):
            self.gridLayout.addWidget(led, 1, idx)

        # Connecting button group clicked signal.
        self.buttonGroup.buttonClicked.connect(self.onPressButton)

    def onPressButton(self, button: QPushButton):
        idx = self.buttonGroup.id(button)
        self.leds[idx].setChecked(not self.leds[idx].isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DemoApp()
    form.show()
    sys.exit(app.exec_())
