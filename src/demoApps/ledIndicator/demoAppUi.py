from PySide2.QtWidgets import QButtonGroup, QGridLayout, QMainWindow, \
    QPushButton, QWidget


class Ui_DemoApp(object):
    def setupUi(self, DemoApp: QMainWindow, ledCnt: int) -> None:
        # Set up the DemoApp window
        DemoApp.setObjectName('DemoApp')
        DemoApp.setWindowTitle('LedIndicator Demo App')

        # Set up central widget
        self.centralWidget = QWidget(DemoApp)
        self.centralWidget.setObjectName('centralWidget')
        DemoApp.setCentralWidget(self.centralWidget)

        # Set up layout
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName('demoAppLayout')

        # Set up the buttons
        self.buttonGroup = QButtonGroup(self)
        for idx in range(ledCnt):
            button = QPushButton(self.centralWidget)
            self.buttonGroup.addButton(button, idx)
            button.setObjectName(f"button{idx}")
            button.setText('Click Me')
            self.gridLayout.addWidget(button, 0, idx)
