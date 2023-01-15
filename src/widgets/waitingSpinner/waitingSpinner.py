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
        self._currentCounter = 0
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
        self._timer.timeout.connect(self.rotate)
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
        self._currentCounter = 0
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

    def getInnerRadius(self) -> int:
        """
        Get the inner radius.

        Return
            The spinner inner radius.
        """
        return self._innerRadius

    def setInnerRadius(self, radius: int) -> None:
        self._innerRadius = radius
        self._updateSize()

    def paintEvent(self, event: QPaintEvent):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._lineCount:
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(0, self._lineCount):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength,
                              self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._lineCount)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i,
                                                         self._currentCounter,
                                                         self._lineCount)
            color = self.currentLineColor(distance, self._lineCount,
                                          self._trailFadePct,
                                          self._minTrailOpacity,
                                          self._color)
            painter.setBrush(color)
            rect = QRect(0, int(-self._lineWidth / 2),
                         int(self._lineLength), int(self._lineWidth))
            painter.drawRoundedRect(rect, self._roundness,
                                    self._roundness, Qt.RelativeSize)
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._isParentDisabled:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._isParentDisabled:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimumTrailOpacity(self):
        return self._minTrailOpacity

    def trailFadePercentage(self):
        return self._trailFadePct

    def revolutionsPerSecond(self):
        return self._revsPerSecond

    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=Qt.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePct = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._lineCount:
            self._currentCounter = 0
        self.update()

    def updatePosition(self):
        if self.parentWidget() and self._isCentered:
            self.move(int(self.parentWidget().width() / 2 - self.width() / 2),
                      int(self.parentWidget().height() / 2 - self.height() / 2))    # noqa: E501

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines,
                         trailFadePerc, minOpacity, colorinput):
        color = QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))    # noqa: E501
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color
