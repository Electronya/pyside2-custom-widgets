from unittest import TestCase
from unittest.mock import call, Mock, patch

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor

import os
import sys

sys.path.append(os.path.abspath('./src'))

from widgets.waitingSpinner import WaitingSpinner               # noqa: E402


class TestWaitingSpinner(TestCase):
    """
    The WaitingSpinner class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self.widgetCls = 'widgets.waitingSpinner.waitingSpinner.QWidget'
        self.timerCls = 'widgets.waitingSpinner.waitingSpinner.QTimer'
        self.painterCls = 'widgets.waitingSpinner.waitingSpinner.QPainter'
        self.colorCls = 'widgets.waitingSpinner.waitingSpinner.QColor'
        self.rectCls = 'widgets.waitingSpinner.waitingSpinner.QRect'
        with patch(f"{self.widgetCls}.__init__"), \
                patch.object(WaitingSpinner, '_initTimer'), \
                patch.object(WaitingSpinner, '_initDisplayState'):
            self.dut = WaitingSpinner(None)
            self.dut._timer = Mock()

    def test_constructorDefault(self) -> None:
        """
        The constructor must initialize the WaitingSpinner instance with
        the default value when no specific parameters are provided.
        """
        testParent = 'test parent'
        with patch(f"{self.widgetCls}.__init__") as mockedBaseClsConst, \
                patch.object(WaitingSpinner, '_initAttributes') \
                as mockedInitAtt, \
                patch.object(WaitingSpinner, '_initTimer') as mockedInitTmr, \
                patch.object(WaitingSpinner, '_initDisplayState') \
                as mockedInitDispState:
            WaitingSpinner(testParent)
            mockedBaseClsConst.assert_called_once_with(testParent)
            mockedInitAtt.assert_called_once_with(True, False, Qt.black)
            mockedInitTmr.assert_called_once()
            mockedInitDispState.assert_called_once_with(Qt.NonModal)

    def test_constructorNonDefault(self) -> None:
        """
        The constructor must initialize the WaitingSpinner instance with
        the passed value when specific parameters are provided.
        """
        testParent = 'test parent'
        testCentered = False
        testDisabled = True
        testColor = Qt.red
        testModality = 'test modality'
        with patch(f"{self.widgetCls}.__init__") as mockedBaseClsConst, \
                patch.object(WaitingSpinner, '_initAttributes') \
                as mockedInitAtt, \
                patch.object(WaitingSpinner, '_initTimer') as mockedInitTmr, \
                patch.object(WaitingSpinner, '_initDisplayState') \
                as mockedInitDispState:
            WaitingSpinner(testParent, isCentered=testCentered,
                           isParentDisabled=testDisabled, color=testColor,
                           modality=testModality)
            mockedBaseClsConst.assert_called_once_with(testParent)
            mockedInitAtt.assert_called_once_with(testCentered, testDisabled,
                                                  testColor)
            mockedInitTmr.assert_called_once()
            mockedInitDispState.assert_called_once_with(testModality)

    def test_updateTimer(self) -> None:
        """
        The _updateTimer method must update the internal timer interval.
        """
        timeout = \
            int(1000 / (self.dut._lineCount * self.dut._revsPerSecond))
        self.dut._updateTimer()
        self.dut._timer.setInterval.assert_called_once_with(timeout)

    def test_initTimer(self) -> None:
        """
        The _initTimer method must create and update the internal timer.
        """
        testTimer = Mock()
        with patch(self.timerCls) as mockedTmrClsConst, \
                patch.object(self.dut, '_updateTimer') as mockedUpdateTmr:
            mockedTmrClsConst.return_value = testTimer
            self.dut._initTimer()
            mockedTmrClsConst.assert_called_once()
            self.assertEqual(self.dut._timer, testTimer, '_initTimer failed '
                             'to create the internal timer.')
            mockedUpdateTmr.assert_called_once()

    def test_updateSize(self) -> None:
        """
        The _updateSize method must update the spinner size.
        """
        size = int((self.dut._innerRadius + self.dut._lineLength) * 2)
        with patch.object(self.dut, 'setFixedSize') as mockedSetFixedSize:
            self.dut._updateSize()
            mockedSetFixedSize.assert_called_once_with(size, size)

    def test_initDisplayState(self) -> None:
        """
        The _initDisplayState method must update the size, set the modality,
        set the background translucent and hide the spinner.
        """
        testModality = Qt.NonModal
        with patch.object(self.dut, '_updateSize') as mockedUpdateSize, \
                patch.object(self.dut, 'setWindowModality') as mockedSetMod, \
                patch.object(self.dut, 'setAttribute') as mockedSetAtt, \
                patch.object(self.dut, 'hide') as mockedHide:
            self.dut._initDisplayState(testModality)
            mockedUpdateSize.assert_called_once()
            mockedSetMod.assert_called_once_with(testModality)
            mockedSetAtt.assert_called_once_with(Qt.WA_TranslucentBackground)
            mockedHide.assert_called_once()

    def test_rotate(self) -> None:
        """
        The _rotate method must increment the counter, reset when a full
        circle have been done and update the widget.
        """
        for expectedCount in range(1, self.dut._lineCount + 1):
            if expectedCount >= self.dut._lineCount:
                expectedCount = 0
            with patch.object(self.dut, 'update') as mockedUpdate:
                self.dut._rotate()
                self.assertEqual(self.dut._counter, expectedCount,
                                 '_rotate failed to increment and reset the '
                                 'counter.')
                mockedUpdate.assert_called_once()

    def test_centerInParent(self) -> None:
        """
        The _centerInParent method must center the spinner if the feature
        is enabled.
        """
        centeredFlags = (False, True)
        spinnerWidth = 2
        spinnerHeight = 2
        parentWidth = 10
        parentHeight = 10
        expectedX = int(parentWidth / 2 - spinnerWidth / 2)
        expectedY = int(parentHeight / 2 - spinnerHeight / 2)
        with patch.object(self.dut, 'parentWidget') as mockedParentWidget, \
                patch.object(self.dut, 'width') as mockedWidth, \
                patch.object(self.dut, 'height') as mockedHeight, \
                patch.object(self.dut, 'move') as mockedMove:
            mockedParentWidget().width.return_value = parentWidth
            mockedParentWidget().height.return_value = parentHeight
            mockedWidth.return_value = spinnerWidth
            mockedHeight.return_value = spinnerHeight
            for centeredFlag in centeredFlags:
                self.dut._isCentered = centeredFlag
                self.dut._centerInParent()
            mockedParentWidget().width.assert_called_once()
            mockedParentWidget().height.assert_called_once()
            mockedMove.assert_called_once_with(expectedX, expectedY)

    def test_disableParent(self) -> None:
        """
        The _disableParent must disable the spinner parent when the feature
        is enabled
        """
        disableFlags = (True, False)
        with patch.object(self.dut, 'parentWidget') as mockedParentWidget:
            for disableFlag in disableFlags:
                mockedParentWidget().return_value = 'test parent'
                self.dut._isParentDisabled = disableFlag
                self.dut._disableParent()
            mockedParentWidget().setEnabled.assert_called_once_with(False)

    def test_enableParent(self) -> None:
        """
        The _enableParent must enable the spinner parent when the feature
        is enabled
        """
        enable = (True, False)
        with patch.object(self.dut, 'parentWidget') as mockedParentWidget:
            for enableFlag in enable:
                mockedParentWidget().return_value = 'test parent'
                self.dut._isParentDisabled = enableFlag
                self.dut._enableParent()
            mockedParentWidget().setEnabled.assert_called_once_with(True)

    def test_calcLineTrailPos(self) -> None:
        """
        The _calcLineTrailPos must calculate the current line position in the
        trail.
        """
        currentLines = (0, 2, 7, 10)
        activeLines = (5, 6, 10, 9)
        lineCounts = (10, 20, 15, 30)
        expectedPositions = (5, 4, 3, 29)
        for idx, line in enumerate(currentLines):
            result = self.dut._calcLineTrailPos(line, activeLines[idx],
                                                lineCounts[idx])
            self.assertEqual(result, expectedPositions[idx],
                             '_calcLineTrailPos failed to calculate the '
                             'current line position in the trail.')

    def test_calcLineAlphaActiveLine(self) -> None:
        """
        The _calcLineAlpha method must calculate and return the current line
        alpha value.
        """
        lines = (0, 3, 5, 8, 10)
        expectedAlphas = (1.0, 0.677138668, 0.46189778, 0.139036448, 0.031416)
        for idx, line in enumerate(lines):
            result = self.dut._calcLineAlpha(line, 10, 80, 3.1416)
            self.assertAlmostEqual(result, expectedAlphas[idx], places=7,
                                   msg='_calcLineAlpha failed to calculate '
                                   'the current line alpha.')

    def test_drawLineSavePainter(self) -> None:
        """
        The _drawLine method must save, transform, set the brush
        and restore the painter.
        """
        mockedPainter = Mock()
        mockedColor = Mock()
        expectedAngles = (0, 18, 36, 54, 72)
        expectedTransCalls = \
            (call(self.dut._innerRadius + self.dut._lineLength,
                  self.dut._innerRadius + self.dut._lineLength),
             call(self.dut._innerRadius, 0))
        for line, angle in enumerate(expectedAngles):
            mockedPainter.reset_mock()
            with patch(self.colorCls) as mockedColorConst, \
                    patch.object(self.dut, '_calcLineTrailPos'), \
                    patch.object(self.dut, '_calcLineAlpha'):
                mockedColorConst.return_value = mockedColor
                self.dut._drawLine(mockedPainter, line)
                mockedPainter.save.assert_called_once()
                mockedPainter.translate.assert_has_calls(expectedTransCalls)
                mockedPainter.rotate.assert_called_once_with(angle)
                mockedPainter.setBrush.assert_called_once_with(mockedColor)
                mockedPainter.restore.assert_called_once()

    def test_drawLineColor(self) -> None:
        """
        The _drawLine method must create the line color based on its position
        in the trail the fade percentage and the minimal opacity.
        """
        mockedPainter = Mock()
        mockedColor = Mock()
        trailPositions = (0, 1, 2, 3, 4)
        alphas = (1.0, 0.8, 0.7, 0.6, 0.5)
        for line, trailPos in enumerate(trailPositions):
            mockedColor.reset_mock()
            with patch(self.colorCls) as mockedColorConst, \
                    patch.object(self.dut, '_calcLineTrailPos') \
                    as mockedCalcLineTrailPos, \
                    patch.object(self.dut, '_calcLineAlpha') \
                    as mockedCalcLineAlpha:
                mockedColorConst.return_value = mockedColor
                mockedCalcLineTrailPos.return_value = trailPos
                mockedCalcLineAlpha.return_value = alphas[line]
                self.dut._drawLine(mockedPainter, line)
                mockedColorConst.assert_called_once_with(self.dut._color)
                mockedCalcLineTrailPos \
                    .assert_called_once_with(line, self.dut._counter,
                                             self.dut._lineCount)
                mockedCalcLineAlpha \
                    .assert_called_once_with(trailPos, self.dut._lineCount,
                                             self.dut._trailFadePct,
                                             self.dut._minTrailOpacity)
                mockedColor.setAlphaF.assert_called_once_with(alphas[line])

    def test_drawLineDrawRect(self) -> None:
        """
        The _drawLine must draw the line.
        """
        mockedPainter = Mock()
        mockedRect = Mock()
        for line in range(5):
            mockedPainter.reset_mock()
            with patch(self.colorCls), \
                    patch(self.rectCls) as mockedRectConst, \
                    patch.object(self.dut, '_calcLineTrailPos'), \
                    patch.object(self.dut, '_calcLineAlpha'):
                mockedRectConst.return_value = mockedRect
                self.dut._drawLine(mockedPainter, line)
                mockedRectConst \
                    .assert_called_once_with(0, int(-self.dut._lineWidth / 2),
                                             self.dut._lineLength,
                                             self.dut._lineWidth)
                mockedPainter.drawRoundedRect \
                    .assert_called_once_with(mockedRect, self.dut._roundness,
                                             self.dut._roundness,
                                             Qt.RelativeSize)

    def test_getLineCount(self) -> None:
        """
        The getLineCount method must return the current spinner line count.
        """
        testLineCount = 15
        self.dut._lineCount = testLineCount
        result = self.dut.getLineCount()
        self.assertEqual(result, testLineCount, 'getLineCount failed to '
                         'return the spinner current line count.')

    def test_setLineCount(self) -> None:
        """
        The setLineCount method must set the current spinner line count and
        update the internal timer.
        """
        testLineCount = 15
        with patch.object(self.dut, '_updateTimer') as mockedUpdateTmr:
            self.dut.setLineCount(testLineCount)
            self.assertEqual(self.dut._lineCount, testLineCount,
                             'setLineCount failed to set the spinner current '
                             'line count.')
            mockedUpdateTmr.assert_called_once()

    def test_getLineLength(self) -> None:
        """
        The getLineLength method must return the current spinner line length.
        """
        testLineLength = 15
        self.dut._lineLength = testLineLength
        result = self.dut.getLineLength()
        self.assertEqual(result, testLineLength, 'getLineLength failed to '
                         'return the spinner current line length.')

    def test_setLineLength(self) -> None:
        """
        The setLineLength method must set the current spinner line length and
        update the spinner size.
        """
        testLineLength = 15
        with patch.object(self.dut, '_updateSize') as mockedUpdateSize:
            self.dut.setLineLength(testLineLength)
            self.assertEqual(self.dut._lineLength, testLineLength,
                             'setLineLength failed to set the spinner '
                             'line length.')
            mockedUpdateSize.assert_called_once()

    def test_getLineWidth(self) -> None:
        """
        The getLineWidth method must return the current spinner line width.
        """
        testLineWidth = 15
        self.dut._lineWidth = testLineWidth
        result = self.dut.getLineWidth()
        self.assertEqual(result, testLineWidth, 'getLineWidth failed to '
                         'return the spinner current line width.')

    def test_setLineWidth(self) -> None:
        """
        The setLineWidth method must set the current spinner line width and
        update the spinner size.
        """
        testLineWidth = 15
        with patch.object(self.dut, '_updateSize') as mockedUpdateSize:
            self.dut.setLineWidth(testLineWidth)
            self.assertEqual(self.dut._lineWidth, testLineWidth,
                             'setLineWidth failed to set the spinner '
                             'line width.')
            mockedUpdateSize.assert_called_once()

    def test_getRoundness(self) -> None:
        """
        The getRoundness method must return the current spinner line roundness.
        """
        testRoundness = 15
        self.dut._roundness = testRoundness
        result = self.dut.getRoundness()
        self.assertEqual(result, testRoundness, 'getRoundness failed to '
                         'return the spinner current line roundness.')

    def test_setRoundness(self) -> None:
        """
        The setRoundness method must set the current spinner line roundness
        while limiting its value.
        """
        testRoundnesses = (-0.1, 0.0, 37.8, 85.4, 100.0, 100.1)
        expectedRoundnesses = (0.0, 0.0, 37.8, 85.4, 100.0, 100.0)
        for idx, testRoundness in enumerate(testRoundnesses):
            self.dut.setRoundness(testRoundness)
            self.assertEqual(self.dut._roundness, expectedRoundnesses[idx],
                             'setRoundness failed to set the spinner '
                             'line roundness.')

    def test_getInnerRadius(self) -> None:
        """
        The getInnerRadius method must return the current spinner inner radius.
        """
        testInnerRadius = 15
        self.dut._innerRadius = testInnerRadius
        result = self.dut.getInnerRadius()
        self.assertEqual(result, testInnerRadius, 'getInnerRadius failed to '
                         'return the spinner current inner radius.')

    def test_setInnerRadius(self) -> None:
        """
        The setInnerRadius method must set the current spinner inner radius and
        update the spinner size.
        """
        testInnerRadius = 15
        with patch.object(self.dut, '_updateSize') as mockedUpdateSize:
            self.dut.setInnerRadius(testInnerRadius)
            self.assertEqual(self.dut._innerRadius, testInnerRadius,
                             'setInnerRadius failed to set the spinner '
                             'inner radius.')
            mockedUpdateSize.assert_called_once()

    def test_getColor(self) -> None:
        """
        The getColor method must return the current spinner color.
        """
        testColor = QColor(Qt.red)
        self.dut._color = testColor
        result = self.dut.getColor()
        self.assertEqual(result, testColor, 'getColor failed to '
                         'return the spinner current color.')

    def test_setColor(self) -> None:
        """
        The setColor method must set the current spinner color.
        """
        testColor = QColor(Qt.green)
        self.dut.setColor(Qt.green)
        self.assertEqual(self.dut._color, testColor,
                         'setColor failed to set the spinner color.')

    def test_getMinTrailOpacity(self) -> None:
        """
        The getMinTrailOpacity method must return the current spinner minimum
        trail opacity.
        """
        testOpacity = 2.1
        self.dut._minTrailOpacity = testOpacity
        result = self.dut.getMinTrailOpacity()
        self.assertEqual(result, testOpacity, 'getMinTrailOpacity failed to '
                         'return the spinner current minimum trail opacity.')

    def test_setMinTrailOpacity(self) -> None:
        """
        The setMinTrailOpacity method must set the current spinner minimum
        trail opacity.
        """
        testOpacity = 2.1
        self.dut.setMinTrailOpacity(testOpacity)
        self.assertEqual(self.dut._minTrailOpacity, testOpacity,
                         'setMinTrailOpacity failed to set the spinner '
                         'minimum opacity.')

    def test_getTrailFadePct(self) -> None:
        """
        The getTrailFadePct method must return the current spinner
        trail fade percentage.
        """
        testFadePct = 2.1
        self.dut._trailFadePct = testFadePct
        result = self.dut.getTrailFadePct()
        self.assertEqual(result, testFadePct, 'getTrailFadePct failed to '
                         'return the spinner current trail fade percentage.')

    def test_setTrailFadePct(self) -> None:
        """
        The setTrailFadePct method must set the current spinner
        trail fade percentage.
        """
        testFadePct = 2.1
        self.dut.setTrailFadePct(testFadePct)
        self.assertEqual(self.dut._trailFadePct, testFadePct,
                         'setTrailFadePct failed to set the spinner '
                         'trail fade percentage.')

    def test_getRevsPerSecond(self) -> None:
        """
        The getRevsPerSecond method must return the current spinner
        revolutions per second.
        """
        testRevsPerSecond = 2.1
        self.dut._revsPerSecond = testRevsPerSecond
        result = self.dut.getRevsPerSecond()
        self.assertEqual(result, testRevsPerSecond, 'getRevsPerSecond failed '
                         'to return the spinner current revolutions per '
                         'second.')

    def test_setRevsPerSecond(self) -> None:
        """
        The setRevsPerSecond method must set the current spinner
        revolutions per second.
        """
        testRevsPerSecond = 2.1
        with patch.object(self.dut, '_updateTimer') as mockedUpdateTmr:
            self.dut.setRevsPerSecond(testRevsPerSecond)
            mockedUpdateTmr.assert_called_once()
            self.assertEqual(self.dut._revsPerSecond, testRevsPerSecond,
                             'setRevsPerSecond failed to set the spinner '
                             'revolutions per second.')

    def test_isSpinning(self) -> None:
        """
        The isSpinning method must return True if the spinner is spinning and
        False otherwise.
        """
        expectedRes = (False, True)
        for expectedResult in expectedRes:
            self.dut._isSpinning = expectedResult
            result = self.dut.isSpinning()
            self.assertEqual(result, expectedResult, 'isSpinning failed '
                             'to return the spinning state of the spinner.')

    def test_startCenterAndDisableParent(self) -> None:
        """
        The start method must center in and disable the spinner parent if
        the spinner is not already spinning.
        """
        spinningFlags = (False, True)
        with patch.object(self.dut, '_centerInParent') as mockedCenter, \
                patch.object(self.dut, '_disableParent') as MockedDisable, \
                patch.object(self.dut, 'show'):
            for spinningFlag in spinningFlags:
                self.dut._isSpinning = spinningFlag
                self.dut.start()
            mockedCenter.assert_called_once()
            MockedDisable.assert_called_once()

    def test_startStartSpinning(self) -> None:
        """
        The start method must start the internal timer, set the spinning flag
        and show the spinner if it's not already spinning.
        """
        spinningFlags = (False, True)
        with patch.object(self.dut, '_centerInParent'), \
                patch.object(self.dut, '_disableParent'), \
                patch.object(self.dut, 'show') as mockedShow:
            for spinningFlag in spinningFlags:
                self.dut._isSpinning = spinningFlag
                self.dut._counter = 10
                self.dut.start()
                if not spinningFlag:
                    self.assertTrue(self.dut._isSpinning, 'start failed to '
                                    'set the spinning flag')
                    self.assertEqual(self.dut._counter, 0, 'start failed to '
                                     'initialize the line counter.')
            self.dut._timer.start.assert_called_once()
            mockedShow.assert_called_once()

    def test_stopStopSpinning(self) -> None:
        """
        The stop method must stop the internal timer, clear the spinning flag
        enable the parent and hide the spinner if it's already spinning.
        """
        spinningFlags = (False, True)
        with patch.object(self.dut, '_centerInParent'), \
                patch.object(self.dut, '_enableParent') as mockedEnable, \
                patch.object(self.dut, 'hide') as mockedHide:
            for spinningFlag in spinningFlags:
                self.dut._isSpinning = spinningFlag
                self.dut._counter = 10
                self.dut.stop()
                if spinningFlag:
                    self.assertFalse(self.dut._isSpinning, 'stop failed to '
                                     'set the spinning flag')
            self.dut._timer.stop.assert_called_once()
            mockedEnable.assert_called_once()
            mockedHide.assert_called_once()

    def test_paintEventInitPainter(self) -> None:
        """
        The paintEvent must initialize the painter.
        """
        mockedPainter = Mock()
        with patch(self.painterCls) as mockedPainterConst, \
                patch.object(self.dut, 'rect') as mockedRect, \
                patch.object(self.dut, '_drawLine'):
            mockedPainterConst.return_value = mockedPainter
            mockedRect.return_value = 10
            self.dut.paintEvent(None)
            mockedPainterConst.assert_called_once_with(self.dut)
            mockedPainter.fillRect.assert_called_once_with(10, Qt.transparent)
            mockedPainter.setRenderHint \
                .assert_called_once_with(mockedPainterConst.Antialiasing, True)
            mockedPainter.setPen.assert_called_once_with(Qt.NoPen)

    def test_paintEventDrawLines(self) -> None:
        """
        The paintEvent must draw all the lines of the spinner.
        """
        mockedPainter = Mock()
        expectedCalls = []
        for line in range(self.dut._lineCount):
            expectedCalls.append(call(mockedPainter, line))
        with patch(self.painterCls) as mockedPainterConst, \
                patch.object(self.dut, 'rect'), \
                patch.object(self.dut, '_drawLine') as mockedDrawLine:
            mockedPainterConst.return_value = mockedPainter
            self.dut.paintEvent(None)
            mockedDrawLine.assert_has_calls(expectedCalls)
