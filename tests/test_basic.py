#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A series of tests to make sure our classes and functions work correctly."""

# IMPORT STANDARD LIBRARIES
import unittest
import functools

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from qwebtip import qweburltip


APPLICATION = QtWidgets.QApplication([])


class Behavior(unittest.TestCase):

    """All tests for creating a general browser widget."""

    def setUp(self):
        """Since we make edits to certain classes, store their unbound methods."""
        self.backups = {"QLabel.eventFilter": QtWidgets.QLabel.eventFilter}

    def tearDown(self):
        """Restore any modified classes to their default state."""
        QtWidgets.QLabel.eventFilter = self.backups["QLabel.eventFilter"]

    @staticmethod
    def _make_fake_tooltip_event():
        """`QtGui.QHelpEvent`: Make a fake object to use for a tooltip."""
        fake_relative_position = QtCore.QPoint(40, 10)
        fake_global_position = QtCore.QPoint(400, 100)

        event = QtGui.QHelpEvent(
            QtCore.QEvent.ToolTip, fake_relative_position, fake_global_position
        )

        return event

    def test_apply_to_widget(self):
        """Check that adding our tooltip onto a widget works."""
        widget = QtWidgets.QLabel("some widget")
        url = "http://google.com"
        qweburltip.override_tool_tip(widget, url)
        widget.installEventFilter(widget)
        result = widget.eventFilter(widget, self._make_fake_tooltip_event())

        # This is true if a tooltip was requested
        self.assertTrue(result)

    def test_parent_event_filter(self):
        """Check that the original widget's parent class still calls `eventFilter`."""

        def acknowledgement(self, obj, event, data):  # pylint: disable=unused-argument
            """Check if this function has been run, using `data`."""
            data["ran"] = True
            return False

        data = dict()
        widget = QtWidgets.QLabel("some widget")

        widget.__class__.eventFilter = functools.partial(acknowledgement, data=data)

        url = "http://google.com"
        qweburltip.override_tool_tip(widget, url)
        widget.installEventFilter(widget)
        widget.eventFilter(widget, self._make_fake_tooltip_event())

        # This is true if a tooltip was requested
        self.assertTrue(data.get("ran", False))
