import os
import sys

from PySide2.QtWidgets import QApplication, QColorDialog, QMainWindow

sys.path.append(os.path.abspath('./src'))
from widgets.waitingSpinner import WaitingSpinner                  # noqa: E402
from demoApps.waitingSpinner.demoAppUi import Ui_DemoApp           # noqa: E402


class DemoApp(QMainWindow, Ui_DemoApp):
    def __init__(self) -> None:
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Set up the spinner
        self.spinner = WaitingSpinner(self.spinnerBox)
        self.spinnerBox.layout().addWidget(self.spinner)
        self.spinner.start()

        # Set up signals and slots
        self.startBtn.clicked.connect(self._startSpinner)
        self.stopBtn.clicked.connect(self._stopSpinner)
        self.colorPickerBtn.clicked.connect(self._pickColor)
        self.roundnessSb.valueChanged.connect(self._setRoundness)
        self.minOpacitySb.valueChanged.connect(self._setMinOpacity)
        self.fadePctSb.valueChanged.connect(self._setFadePct)
        self.lineCntSb.valueChanged.connect(self._setLineCount)
        self.lineLengthSb.valueChanged.connect(self._setLineLength)
        self.lineWidthSb.valueChanged.connect(self._setLineWidth)
        self.innerRadiusSb.valueChanged.connect(self._setInnerRadius)
        self.revsPerSecondSb.valueChanged.connect(self._setRevsPerSecond)

    def _startSpinner(self) -> None:
        self.spinner.start()

    def _stopSpinner(self) -> None:
        self.spinner.stop()

    def _pickColor(self) -> None:
        self.spinner.setColor(QColorDialog.getColor())

    def _setRoundness(self, roundness: float) -> None:
        self.spinner.setRoundness(roundness)

    def _setMinOpacity(self, opacity: float) -> None:
        self.spinner.setMinTrailOpacity(opacity)

    def _setFadePct(self, fadePct: float) -> None:
        self.spinner.setTrailFadePct(fadePct)

    def _setLineCount(self, count: int) -> None:
        self.spinner.setLineCount(count)

    def _setLineLength(self, length: float) -> None:
        self.spinner.setLineLength(length)

    def _setLineWidth(self, width: float) -> None:
        self.spinner.setLineWidth(width)

    def _setInnerRadius(self, radius: float) -> None:
        self.spinner.setInnerRadius(radius)

    def _setRevsPerSecond(self, revs: float) -> None:
        self.spinner.setRevsPerSecond(revs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DemoApp()
    form.show()
    sys.exit(app.exec_())
