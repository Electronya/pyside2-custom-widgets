from PySide2.QtWidgets import QDoubleSpinBox, QGridLayout, QGroupBox, \
    QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QWidget


class Ui_DemoApp(object):
    def setupUi(self, demoApp: QMainWindow) -> None:
        # Set up the DemoApp window
        demoApp.setObjectName('DemoApp')
        demoApp.setWindowTitle('WaitingSpinner Demo App')
        self._setupCentralWidget(demoApp)
        self._setupSpinnerBox(demoApp)
        self._setupSettingsBox(demoApp)
        self._setupButtons()

    def _setupCentralWidget(self, demoApp: QMainWindow) -> None:
        # Set up central widget
        self.centralWidget = QWidget(demoApp)
        self.centralWidget.setObjectName('centralWidget')
        demoApp.setCentralWidget(self.centralWidget)

        # Set up layout
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName('demoAppLayout')

    def _setupSpinnerBox(self, demoApp: QMainWindow) -> None:
        # Set up the group box
        self.spinnerBox = QGroupBox(demoApp)
        self.spinnerBox.setTitle('Waiting Spinner')
        self.SpinnerBoxLayout = QHBoxLayout(self.spinnerBox)
        self.gridLayout.addWidget(self.spinnerBox, 0, 0, 1, 3)

    def _setupSettingsBox(self, demoApp: QMainWindow) -> None:
        # Set up the group box
        self.settingsBox = QGroupBox(demoApp)
        self.settingsBox.setTitle('Waiting Spinner')
        self.settingsBoxLayout = QGridLayout(self.settingsBox)
        self.gridLayout.addWidget(self.settingsBox, 0, 4)

        # Set up roundness
        self.roundnessLbl = QLabel(self.settingsBox)
        self.roundnessLbl.setText('Roundness:')
        self.settingsBoxLayout.addWidget(self.roundnessLbl, 0, 0)
        self.roundnessSb = QDoubleSpinBox(self.settingsBox)
        self.roundnessSb.setValue(70)
        self.roundnessSb.setRange(0, 100)
        self.settingsBoxLayout.addWidget(self.roundnessSb, 0, 1)

        # Set up minimum opacity
        self.minOpacityLbl = QLabel(self.settingsBox)
        self.minOpacityLbl.setText('Min. Opacity:')
        self.settingsBoxLayout.addWidget(self.minOpacityLbl, 1, 0)
        self.minOpacitySb = QDoubleSpinBox(self.settingsBox)
        self.minOpacitySb.setValue(15)
        self.minOpacitySb.setRange(0, 100)
        self.settingsBoxLayout.addWidget(self.minOpacitySb, 1, 1)

        # Set up fade percentage
        self.fadePctLbl = QLabel(self.settingsBox)
        self.fadePctLbl.setText('Fade Pct:')
        self.settingsBoxLayout.addWidget(self.fadePctLbl, 2, 0)
        self.fadePctSb = QDoubleSpinBox(self.settingsBox)
        self.fadePctSb.setValue(70)
        self.fadePctSb.setRange(1, 100)
        self.settingsBoxLayout.addWidget(self.fadePctSb, 2, 1)

        # Set up line count
        self.LineCntLbl = QLabel(self.settingsBox)
        self.LineCntLbl.setText('Line Count:')
        self.settingsBoxLayout.addWidget(self.LineCntLbl, 3, 0)
        self.lineCntSb = QSpinBox(self.settingsBox)
        self.lineCntSb.setValue(12)
        self.lineCntSb.setRange(0, 25)
        self.settingsBoxLayout.addWidget(self.lineCntSb, 3, 1)

        # Set up line length
        self.lineLengthLbl = QLabel(self.settingsBox)
        self.lineLengthLbl.setText('Line Length:')
        self.settingsBoxLayout.addWidget(self.lineLengthLbl, 4, 0)
        self.lineLengthSb = QDoubleSpinBox(self.settingsBox)
        self.lineLengthSb.setValue(10)
        self.lineLengthSb.setRange(5, 50)
        self.settingsBoxLayout.addWidget(self.lineLengthSb, 4, 1)

        # Set up line width
        self.lineWidthLbl = QLabel(self.settingsBox)
        self.lineWidthLbl.setText('Line Width:')
        self.settingsBoxLayout.addWidget(self.lineWidthLbl, 5, 0)
        self.linWidthSb = QDoubleSpinBox(self.settingsBox)
        self.linWidthSb.setValue(10)
        self.linWidthSb.setRange(1, 20)
        self.settingsBoxLayout.addWidget(self.linWidthSb, 5, 1)

        # Set up inner radius
        self.innerRadiusLbl = QLabel(self.settingsBox)
        self.innerRadiusLbl.setText('Inner Radius:')
        self.settingsBoxLayout.addWidget(self.innerRadiusLbl, 6, 0)
        self.innerRadiusSb = QDoubleSpinBox(self.settingsBox)
        self.innerRadiusSb.setValue(10)
        self.innerRadiusSb.setRange(5, 50)
        self.settingsBoxLayout.addWidget(self.innerRadiusSb, 6, 1)

        # Set up revolutions per second
        self.revsPerSecondLbl = QLabel(self.settingsBox)
        self.revsPerSecondLbl.setText('Revs/s:')
        self.settingsBoxLayout.addWidget(self.revsPerSecondLbl, 6, 0)
        self.revsPerSecondSb = QDoubleSpinBox(self.settingsBox)
        self.revsPerSecondSb.setValue(1)
        self.revsPerSecondSb.setRange(1, 10)
        self.settingsBoxLayout.addWidget(self.revsPerSecondSb, 6, 1)

    def _setupButtons(self) -> None:
        # Set up start button
        self.startBtn = QPushButton(self.centralWidget)
        self.startBtn.setText('START')
        self.gridLayout.addWidget(self.startBtn, 1, 0)

        # Set up stop button
        self.stopBtn = QPushButton(self.centralWidget)
        self.stopBtn.setText('STOP')
        self.gridLayout.addWidget(self.stopBtn, 1, 1)

        # Set up color picker button
        self.colorPickerBtn = QPushButton(self.centralWidget)
        self.colorPickerBtn.setText('PICK COLOR')
        self.gridLayout.addWidget(self.colorPickerBtn, 1, 2)
