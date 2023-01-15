from unittest import TestCase
from unittest.mock import call, Mock, patch

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QColor

import os
import sys

sys.path.append(os.path.abspath('./src'))

from widgets.ledIndicator import LedIndicator, LedIndicatorColor   # noqa: E402


class TestLedIndicator(TestCase):
    """
    The LedIndicator class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self.baseCls = 'widgets.ledIndicator.ledIndicator.QAbstractButton'
        self.painterCls = 'widgets.ledIndicator.ledIndicator.QPainter'
        self.penCls = 'widgets.ledIndicator.ledIndicator.QPen'
        self.gradientCls = 'widgets.ledIndicator.ledIndicator.QRadialGradient'
        self.brushCls = 'widgets.ledIndicator.ledIndicator.QBrush'
        self.colorCls = 'widgets.ledIndicator.ledIndicator.QColor'
        self.mockedColors = (Mock(), Mock(), Mock(), Mock())
        with patch(f"{self.baseCls}.__init__"), \
                patch(f"{self.baseCls}.setMinimumSize"), \
                patch(f"{self.baseCls}.setCheckable"), \
                patch(self.colorCls) as mockedColorConst:
            mockedColorConst.side_effect = self.mockedColors
            self.dut = LedIndicator()

    def test_constructor(self) -> None:
        """
        The constructor must set the widget minimum size and as checkable.
        """
        with patch(f"{self.baseCls}.__init__"), \
                patch(f"{self.baseCls}.setMinimumSize") as mockedMinSize, \
                patch(f"{self.baseCls}.setCheckable") as mockedCheckable:
            LedIndicator()
            mockedMinSize.assert_called_once_with(24, 24)
            mockedCheckable.assert_called_once_with(True)

    def test_constructorInitColor(self) -> None:
        """
        The constructor must initialize the widget color based on the desired
        one.
        """
        testColors = (None, LedIndicatorColor.BLU, LedIndicatorColor.GRN,
                      LedIndicatorColor.RED, LedIndicatorColor.YEL)
        expectedColors = ({'onColor1': QColor(0, 255, 0),
                           'onColor2': QColor(0, 192, 0),
                           'offColor1': QColor(0, 28, 0),
                           'offColor2': QColor(0, 128, 0)},
                          {'onColor1': QColor(0, 0, 255),
                           'onColor2': QColor(0, 0, 192),
                           'offColor1': QColor(0, 0, 28),
                           'offColor2': QColor(0, 0, 128)},
                          {'onColor1': QColor(0, 255, 0),
                           'onColor2': QColor(0, 192, 0),
                           'offColor1': QColor(0, 28, 0),
                           'offColor2': QColor(0, 128, 0)},
                          {'onColor1': QColor(255, 0, 0),
                           'onColor2': QColor(192, 0, 0),
                           'offColor1': QColor(28, 0, 0),
                           'offColor2': QColor(128, 0, 0)},
                          {'onColor1': QColor(0, 255, 255),
                           'onColor2': QColor(0, 192, 192),
                           'offColor1': QColor(0, 28, 28),
                           'offColor2': QColor(0, 128, 128)})
        for idx, testColor in enumerate(testColors):
            with patch(f"{self.baseCls}.__init__"), \
                    patch(f"{self.baseCls}.setMinimumSize"), \
                    patch(f"{self.baseCls}.setCheckable"):
                if testColor is None:
                    dut = LedIndicator()
                else:
                    dut = LedIndicator(color=testColor)
                self.assertEqual(dut._onColor1,
                                 expectedColors[idx]['onColor1'],
                                 'The constructor failed to initialize the '
                                 'led indicator colors.')
                self.assertEqual(dut._onColor2,
                                 expectedColors[idx]['onColor2'],
                                 'The constructor failed to initialize the '
                                 'led indicator colors.')
                self.assertEqual(dut._offColor1,
                                 expectedColors[idx]['offColor1'],
                                 'The constructor failed to initialize the '
                                 'led indicator colors.')
                self.assertEqual(dut._offColor2,
                                 expectedColors[idx]['offColor2'],
                                 'The constructor failed to initialize the '
                                 'led indicator colors.')

    def test_drawBorderExternal(self) -> None:
        """
        The _drawBorder method must draw the external border with the right
        values when ask to drawing the external border.
        """
        mockedPainter = Mock()
        mockedGradient = Mock()
        mockedBrush = Mock()
        setColorAtCalls = (call(0, QColor(224, 224, 224)),
                           call(1, QColor(28, 28, 28)))
        with patch(self.gradientCls) as mockedGradCls, \
                patch(self.brushCls) as mockedBrushCls:
            mockedGradCls.return_value = mockedGradient
            mockedBrushCls.return_value = mockedBrush
            self.dut._drawBorder(mockedPainter, True)
            mockedGradCls.assert_called_once_with(QPointF(-500, -500), 1500,
                                                  QPointF(-500, -500))
            mockedGradient.setColorAt.assert_has_calls(setColorAtCalls)
            mockedBrushCls.assert_called_once_with(mockedGradient)
            mockedPainter.setBrush(mockedBrush)
            mockedPainter.drawEllipse.assert_called_once_with(QPointF(0, 0),
                                                              500, 500)

    def test_drawBorderInternal(self) -> None:
        """
        The _drawBorder method must draw the internal border with the right
        values when ask to drawing the internal border.
        """
        mockedPainter = Mock()
        mockedGradient = Mock()
        mockedBrush = Mock()
        setColorAtCalls = (call(0, QColor(224, 224, 224)),
                           call(1, QColor(28, 28, 28)))
        with patch(self.gradientCls) as mockedGradCls, \
                patch(self.brushCls) as mockedBrushCls:
            mockedGradCls.return_value = mockedGradient
            mockedBrushCls.return_value = mockedBrush
            self.dut._drawBorder(mockedPainter, False)
            mockedGradCls.assert_called_once_with(QPointF(500, 500), 1500,
                                                  QPointF(500, 500))
            mockedGradient.setColorAt.assert_has_calls(setColorAtCalls)
            mockedBrushCls.assert_called_once_with(mockedGradient)
            mockedPainter.setBrush(mockedBrush)
            mockedPainter.drawEllipse.assert_called_once_with(QPointF(0, 0),
                                                              450, 450)

    def test_drawLedOn(self) -> None:
        """
        The _drawLed method must draw the LED with the on color when the
        widget is checked.
        """
        mockedPainter = Mock()
        mockedGradient = Mock()
        setColorAtCalls = (call(0, self.dut._onColor1),
                           call(1, self.dut._onColor2))
        with patch.object(self.dut, 'isChecked') as mockedIsChecked, \
                patch(self.gradientCls) as mockedGradCls:
            mockedIsChecked.return_value = True
            mockedGradCls.return_value = mockedGradient
            self.dut._drawLed(mockedPainter)
            mockedGradCls.assert_called_once_with(QPointF(-500, -500), 1500,
                                                  QPointF(-500, -500))
            mockedGradient.setColorAt.assert_has_calls(setColorAtCalls)
            mockedPainter.setBrush(mockedGradient)
            mockedPainter.drawEllipse.assert_called_once_with(QPointF(0, 0),
                                                              400, 400)

    def test_drawLedOff(self) -> None:
        """
        The _drawLed method must draw the LED with the off color when the
        widget is checked.
        """
        mockedPainter = Mock()
        mockedGradient = Mock()
        setColorAtCalls = (call(0, self.dut._offColor1),
                           call(1, self.dut._offColor2))
        with patch.object(self.dut, 'isChecked') as mockedIsChecked, \
                patch(self.gradientCls) as mockedGradCls:
            mockedIsChecked.return_value = False
            mockedGradCls.return_value = mockedGradient
            self.dut._drawLed(mockedPainter)
            mockedGradCls.assert_called_once_with(QPointF(500, 500), 1500,
                                                  QPointF(500, 500))
            mockedGradient.setColorAt.assert_has_calls(setColorAtCalls)
            mockedPainter.setBrush(mockedGradient)
            mockedPainter.drawEllipse.assert_called_once_with(QPointF(0, 0),
                                                              400, 400)

    def test_resizeEventUpdate(self) -> None:
        """
        The resizeEvent method must update the widget.
        """
        with patch.object(self.dut, 'update') as mockedUpdate:
            self.dut.resizeEvent(None)
            mockedUpdate.assert_called_once()

    def test_paintEventInitPainterAndPen(self) -> None:
        """
        The paintEvent method must initialize the painter and the pen.
        """
        realSize = 10
        mockedPainter = Mock()
        mockedPen = Mock()
        with patch.object(self.dut, 'width') as mockedWidth, \
                patch.object(self.dut, 'height') as mockedHeight, \
                patch(self.painterCls) as mockedPainterCls, \
                patch.object(self.dut, '_drawBorder'), \
                patch.object(self.dut, '_drawLed'), \
                patch(self.penCls) as mockedPenCls:
            mockedWidth.side_effect = (realSize, realSize)
            mockedHeight.side_effect = (realSize, realSize)
            mockedPainterCls.return_value = mockedPainter
            mockedPenCls.return_value = mockedPen
            self.dut.paintEvent(None)
            mockedPainterCls.assert_called_once_with(self.dut)
            mockedPainter.setRenderHint \
                .assert_called_once_with(mockedPainterCls.Antialiasing)
            mockedPainter.translate.assert_called_once_with(realSize / 2,
                                                            realSize / 2)
            mockedPainter.scale.assert_called_once_with(realSize / 1000,
                                                        realSize / 1000)
            mockedPenCls.assert_called_once_with(Qt.black)
            mockedPen.setWidth.assert_called_once_with(1)
            mockedPainter.setPen.assert_called_once_with(mockedPen)

    def test_paintEventDraw(self) -> None:
        """
        The paintEvent method must draw the external and internal borders and
        the LED.
        """
        realSize = 10
        mockedPainter = Mock()
        drawBorderCalls = (call(mockedPainter, True),
                           call(mockedPainter, False))
        with patch.object(self.dut, 'width') as mockedWidth, \
                patch.object(self.dut, 'height') as mockedHeight, \
                patch(self.painterCls) as mockedPainterCls, \
                patch.object(self.dut, '_drawBorder') as mockedDrawBorder, \
                patch.object(self.dut, '_drawLed') as mockedDrawLed, \
                patch(self.penCls):
            mockedWidth.side_effect = (realSize, realSize)
            mockedHeight.side_effect = (realSize, realSize)
            mockedPainterCls.return_value = mockedPainter
            self.dut.paintEvent(None)
            mockedDrawBorder.assert_has_calls(drawBorderCalls)
            mockedDrawLed.assert_called_once_with(mockedPainter)
