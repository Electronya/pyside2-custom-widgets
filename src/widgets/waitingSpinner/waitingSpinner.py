"""
This is a rework of the port from z3ntu.
The original is licensed under the following:

The MIT License (MIT)
Copyright (c) 2012-2014 Alexander Turkin
Copyright (c) 2014 William Hallatt
Copyright (c) 2015 Jacob Dawid
Copyright (c) 2016 Luca Weiss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math

from PySide2.QtCore import QRect, Qt, QTimer
from PySide2.QtGui import QColor, QPainter, QPaintEvent
from PySide2.QtWidgets import QWidget


class WaitingSpinner(QWidget):
    def __init__(self, parent: QWidget, isCentered: bool = True,
                 isParentDisabled: bool = False,
                 color: Qt.GlobalColor = Qt.black,
                 modality: Qt.WindowModality = Qt.NonModal) -> None:
        """
        Constructor.

        Params:
            parent:             The widget parent.
            isCentered:         The center on parent flag.
            isParentDisabled:   The disable parent when spinning flag.
            color:              The waiting spinner color.
            modality:           The modality mode.
        """
        super().__init__(parent)
        self._initAttributes(isCentered, isParentDisabled, color)
        self._initTimer()
        self._initDisplayState(modality)

    def _initAttributes(self, isCentered: bool, isParentDisabled: bool,
                        color: QColor) -> None:
        """
        Initialize the internal attributes.

        Params:
            isCentered:         The center on parent flag.
            isParentDisabled:   The disable parent when spinning flag.
            color:              The waiting spinner color.
        """
        self._isCentered = isCentered
        self._isParentDisabled = isParentDisabled
        self._color = QColor(color)
        self._roundness = 100.0
        self._minTrailOpacity = 3.14159265358979323846
        self._trailFadePct = 80.0
        self._revsPerSecond = 1.57079632679489661923
        self._lineCount = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._counter = 0
        self._isSpinning = False

    def _updateTimer(self) -> None:
        """
        Update the internal timer.
        """
        timeout = int(1000 / (self._lineCount * self._revsPerSecond))
        self._timer.setInterval(timeout)

    def _initTimer(self) -> None:
        """
        Initialize the internal timer.
        """
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._updateTimer()

    def _updateSize(self) -> None:
        """
        Update the spinner size.
        """
        size = int((self._innerRadius + self._lineLength) * 2)
        self.setFixedSize(size, size)

    def _initDisplayState(self, modality: Qt.WindowModality) -> None:
        """
        Initialize the display state.

        Params:
            modality:           The modality of the spinner.
        """
        self._updateSize()
        self.setWindowModality(modality)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.hide()

    def _rotate(self) -> None:
        """
        Rotate the spinner by incrementing the counter.
        """
        self._counter += 1
        if self._counter >= self._lineCount:
            self._counter = 0
        self.update()

    def _centerInParent(self) -> None:
        """
        Center in parent if the feature is enabled.
        """
        if self.parentWidget() and self._isCentered:
            self.move(int(self.parentWidget().width() / 2 - self.width() / 2),
                      int(self.parentWidget().height() / 2 - self.height() / 2))    # noqa: E501

    def _disableParent(self) -> None:
        """
        Disable the parent if the feature is enabled.
        """
        if self.parentWidget() and self._isParentDisabled:
            self.parentWidget().setEnabled(False)

    def _enableParent(self) -> None:
        """
        Enable the parent if thr feature is enabled.
        """
        if self.parentWidget() and self._isParentDisabled:
            self.parentWidget().setEnabled(True)

    def _calcLineTrailPos(self, lineIdx: int, activeIdx: int,
                          lineCount: int) -> int:
        """
        Calculate the position of the given line in the trail.

        Params:
            lineIdx:            The current line index in the spinner.
            activeIdx:          The index in the spinner of the active line.
            lineCount:          The total line count in the spinner.
        """
        trailPos = activeIdx - lineIdx
        if trailPos < 0:
            trailPos += lineCount
        return trailPos

    def _calcLineAlpha(self, trailPos: int, lineCount: int, fadePct: float,
                       minOpacity: float) -> float:
        """
        Calculate the line alpha value.

        Params:
            trailPos:           The current line trail position.
            lineCount:          The total line count in the spinner.
            trailFadePct:       The trail fade percentage.
            minOpacity:         The minimum opacity.

        Return
            The alpha value for the desired line.
        """
        maxAlpha = 1.0
        if trailPos == 0:
            return maxAlpha
        minAlpha = minOpacity / 100.0
        posThreshold = math.ceil((lineCount - 1) * fadePct / 100)
        if trailPos > posThreshold:
            return minAlpha
        else:
            gradient = (maxAlpha - minAlpha) / (posThreshold + 1)
            lineAlpha = maxAlpha - gradient * trailPos
            return min(maxAlpha, max(minAlpha, lineAlpha))

    def _drawLine(self, painter: QPainter, line: int) -> None:
        """
        Draw the requested line.

        Params:
            painter:            The painter.
            line:               The line ID to draw.
        """
        painter.save()
        painter.translate(self._innerRadius + self._lineLength,
                          self._innerRadius + self._lineLength)
        rotateAngle = 360 * line / self._lineCount
        painter.rotate(rotateAngle)
        painter.translate(self._innerRadius, 0)
        trailPos = self._calcLineTrailPos(line, self._counter, self._lineCount)
        alpha = self._calcLineAlpha(trailPos, self._lineCount,
                                    self._trailFadePct,
                                    self._minTrailOpacity)
        color = QColor(self._color)
        color.setAlphaF(alpha)
        painter.setBrush(color)
        rect = QRect(0, int(-self._lineWidth / 2), self._lineLength,
                     self._lineWidth)
        painter.drawRoundedRect(rect, self._roundness,
                                self._roundness, Qt.RelativeSize)
        painter.restore()

    def getLineCount(self) -> int:
        """
        Get the line count.

        Return
            The spinner line count.
        """
        return self._lineCount

    def setLineCount(self, lineCount: int) -> None:
        """
        Set the line count.

        Params:
            lineCount:          The new line count.
        """
        self._lineCount = lineCount
        self._counter = 0
        self._updateTimer()

    def getLineLength(self) -> int:
        """
        Get the line length.

        Return
            The spinner line length.
        """
        return self._lineLength

    def setLineLength(self, length: int) -> None:
        """
        Set the line length.

        Params:
            length:             The new line length.
        """
        self._lineLength = length
        self._updateSize()

    def getLineWidth(self) -> int:
        """
        Get the line width.

        Return
            The spinner line width,
        """
        return self._lineWidth

    def setLineWidth(self, width: int) -> None:
        """
        Set the line width.

        Params:
            width:              The new line width.
        """
        self._lineWidth = width
        self._updateSize()

    def getRoundness(self) -> float:
        """
        Get the line roundness.

        Return
            The spinner line roundness.
        """
        return self._roundness

    def setRoundness(self, roundness: float) -> None:
        """
        Set the line roundness.

        Params:
            roundness:          The new line roundness.
        """
        self._roundness = max(0.0, min(100.0, roundness))

    def getInnerRadius(self) -> int:
        """
        Get the inner radius.

        Return
            The spinner inner radius.
        """
        return self._innerRadius

    def setInnerRadius(self, radius: int) -> None:
        """
        Set inner radius.

        Params:
            radius:             The new inner radius.
        """
        self._innerRadius = radius
        self._updateSize()

    def getColor(self) -> QColor:
        """
        Get the color.

        Return
            The spinner color.
        """
        return self._color

    def setColor(self, color: Qt.GlobalColor = Qt.black) -> None:
        """
        Set the color.

        Params:
            color:              The new color.
        """
        self._color = QColor(color)

    def getMinTrailOpacity(self) -> float:
        """
        Get the minimum trail opacity.

        Return
            The spinner minimum trail opacity.
        """
        return self._minTrailOpacity

    def setMinTrailOpacity(self, minTrailOpacity: float) -> None:
        """
        Set the minimum trail opacity.

        Params:
            minTrailOpacity:    The new minimum trail opacity.
        """
        self._minTrailOpacity = minTrailOpacity

    def getTrailFadePct(self) -> float:
        """
        Get the trail fade percentage.

        Return
            The spinner trail fade percentage.
        """
        return self._trailFadePct

    def setTrailFadePct(self, fadePct: float) -> None:
        """
        Set the trail fade percentage.

        Params:
            fadePct:            The new trail fade percentage.
        """
        self._trailFadePct = fadePct

    def getRevsPerSecond(self) -> float:
        """
        Get the revolutions per second.

        Return
            The spinner revolutions per second.
        """
        return self._revsPerSecond

    def setRevsPerSecond(self, revsPerSecond: float) -> None:
        """
        Set the revolutions per second.

        Params:
            revsPerSecond:      The new revolutions per second.
        """
        self._revsPerSecond = revsPerSecond
        self._updateTimer()

    def isSpinning(self) -> bool:
        """
        Check if the spinner is spinning.

        Return
            True if the spinner is spinning, false otherwise.
        """
        return self._isSpinning

    def start(self) -> None:
        """
        Start the spinner.
        """
        if not self._isSpinning:
            self._centerInParent()
            self._disableParent()
            self._counter = 0
            self._timer.start()
            self._isSpinning = True
            self.show()

    def stop(self) -> None:
        """
        Stop the spinner.
        """
        if self._isSpinning:
            self._enableParent()
            self._timer.stop()
            self._isSpinning = False
            self.hide()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        for line in range(self._lineCount):
            self._drawLine(painter, line)
