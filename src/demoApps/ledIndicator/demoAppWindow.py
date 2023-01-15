from PySide2 import QtCore, QtWidgets


class Ui_DemoApp(object):
    def setupUi(self, DemoApp):
        DemoApp.setObjectName("DemoApp")
        DemoApp.resize(150, 100)
        self.centralWidget = QtWidgets.QWidget(DemoApp)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        DemoApp.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(DemoApp)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 150, 22))
        self.menuBar.setObjectName("menuBar")
        DemoApp.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(DemoApp)
        self.mainToolBar.setObjectName("mainToolBar")
        DemoApp.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(DemoApp)
        self.statusBar.setObjectName("statusBar")
        DemoApp.setStatusBar(self.statusBar)

        self.retranslateUi(DemoApp)
        QtCore.QMetaObject.connectSlotsByName(DemoApp)

    def retranslateUi(self, DemoApp):
        _translate = QtCore.QCoreApplication.translate
        DemoApp.setWindowTitle(_translate("DemoApp", "DemoApp"))
        self.pushButton.setText(_translate("DemoApp", "Click Me"))
