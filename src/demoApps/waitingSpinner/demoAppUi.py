from PySide2.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, \
    QLabel, QMainWindow, QPushButton, QSpinBox, QWidget


class Ui_DemoApp(object):
    def setupUi(self, demoApp: QMainWindow) -> None:
        # Set up the DemoApp window
        demoApp.setObjectName('DemoApp')
        demoApp.setWindowTitle('WaitingSpinner Demo App')
        self._setupCentralWidget(demoApp)
        self._setupSpinnerBox(demoApp)
        self._setupSettingsBox(demoApp)

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
        self.roundnessSb = QSpinBox(self.settingsBox)
        self.roundnessSb.setValue(70)
        self.roundnessSb.setRange(0, 9999)
        self.settingsBoxLayout.addWidget(self.roundnessSb, 0, 1)

        # Set up minimum opacity
        self.minOpacityLbl = QLabel(self.settingsBox)
        self.minOpacityLbl.setText('Min. Opacity:')
        self.settingsBoxLayout.addWidget(self.minOpacityLbl, 1, 0)
        self.minOpacitySb = QSpinBox(self.settingsBox)
        self.minOpacitySb.setValue(15)
        self.minOpacitySb.setRange(0, 100)
        self.settingsBoxLayout.addWidget(self.minOpacitySb, 1, 1)
