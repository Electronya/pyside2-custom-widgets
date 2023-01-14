from enum import Enum

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPen, \
    QRadialGradient, QResizeEvent
from PySide2.QtWidgets import QAbstractButton


class LedIndicatorColor(dict, Enum):
    """
    The led indicator colors.
    """
    GRN = {'onColor1': {'r': 0, 'g': 255, 'b': 0},
           'onColor2': {'r': 0, 'g': 192, 'b': 0},
           'offColor1': {'r': 0, 'g': 28, 'b': 0},
           'offColor2': {'r': 0, 'g': 128, 'b': 0}}
    RED = {'onColor1': {'r': 255, 'g': 0, 'b': 0},
           'onColor2': {'r': 192, 'g': 0, 'b': 0},
           'offColor1': {'r': 28, 'g': 0, 'b': 0},
           'offColor2': {'r': 128, 'g': 0, 'b': 0}}
    BLU = {'onColor1': {'r': 0, 'g': 0, 'b': 255},
           'onColor2': {'r': 0, 'g': 0, 'b': 192},
           'offColor1': {'r': 0, 'g': 0, 'b': 28},
           'offColor2': {'r': 0, 'g': 0, 'b': 128}}
    YEL = {'onColor1': {'r': 0, 'g': 255, 'b': 255},
           'onColor2': {'r': 0, 'g': 192, 'b': 192},
           'offColor1': {'r': 0, 'g': 28, 'b': 28},
           'offColor2': {'r': 0, 'g': 128, 'b': 128}}


class LedIndicator(QAbstractButton):
    scaledSize = 1000.0

    def __init__(self, parent=None,
                 color: LedIndicatorColor = LedIndicatorColor.GRN) -> None:
        """
        Constructor.

        Params:
            parent:         The widget parent.
            color:          The indicator color.
        """
        QAbstractButton.__init__(self, parent)

        self.setMinimumSize(24, 24)
        self.setCheckable(True)
        self._onColor1 = QColor(color.value['onColor1']['r'],
                                color.value['onColor1']['g'],
                                color.value['onColor1']['b'])
        self._onColor2 = QColor(color.value['onColor2']['r'],
                                color.value['onColor2']['g'],
                                color.value['onColor2']['b'])
        self._offColor1 = QColor(color.value['offColor1']['r'],
                                 color.value['offColor1']['g'],
                                 color.value['offColor1']['b'])
        self._offColor2 = QColor(color.value['offColor2']['r'],
                                 color.value['offColor2']['g'],
                                 color.value['offColor2']['b'])

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Resize event handler.

        Params:
            event:          The Qt resize event.
        """
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint event handler.

        Params:
            event:          The Qt paint event.
        """
        realSize = min(self.width(), self.height())

        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(1)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(realSize / self.scaledSize, realSize / self.scaledSize)

        gradient = QRadialGradient(QPointF(-500, -500), 1500,
                                   QPointF(-500, -500))
        gradient.setColorAt(0, QColor(224, 224, 224))
        gradient.setColorAt(1, QColor(28, 28, 28))
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), 500, 500)

        gradient = QRadialGradient(QPointF(500, 500), 1500, QPointF(500, 500))
        gradient.setColorAt(0, QColor(224, 224, 224))
        gradient.setColorAt(1, QColor(28, 28, 28))
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(0, 0), 450, 450)

        painter.setPen(pen)
        if self.isChecked():
            gradient = QRadialGradient(QPointF(-500, -500), 1500,
                                       QPointF(-500, -500))
            gradient.setColorAt(0, self._onColor1)
            gradient.setColorAt(1, self._onColor2)
        else:
            gradient = QRadialGradient(QPointF(500, 500), 1500,
                                       QPointF(500, 500))
            gradient.setColorAt(0, self._offColor1)
            gradient.setColorAt(1, self._offColor2)

        painter.setBrush(gradient)
        painter.drawEllipse(QPointF(0, 0), 400, 400)
