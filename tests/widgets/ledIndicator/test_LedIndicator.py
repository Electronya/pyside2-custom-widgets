from unittest import TestCase
from unittest.mock import call, Mock, mock_open, patch

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
        self.colorCls = 'widgets.ledIndicator.ledIndicator.QColor'
        self.mockedColors = {'onColor1': Mock(), 'onColor2': Mock(),
                             'offColor1': Mock(), 'offColor2': Mock()}

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
