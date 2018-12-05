#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of tests to make sure our classes and functions work correctly.'''

# IMPORT STANDARD LIBRARIES
import functools
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from qwebtip import qweburltip
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui


APPLICATION = QtWidgets.QApplication([])


class URL(unittest.TestCase):
    def setUp(self):
        self.backups = {'QLabel.eventFilter': QtWidgets.QLabel.eventFilter}

    def tearDown(self):
        QtWidgets.QLabel.eventFilter = self.backups['QLabel.eventFilter']

    @staticmethod
    def _make_fake_tooltip_event():

        fake_relative_position = QtCore.QPoint(40, 10)
        fake_global_position = QtCore.QPoint(400, 100)

        event = QtGui.QHelpEvent(
            QtCore.QEvent.ToolTip, fake_relative_position, fake_global_position)

        return event

    def test_apply_to_widget(self):
        widget = QtWidgets.QLabel('some widget')
        url = 'http://google.com'
        qweburltip.override_tool_tip(widget, url)
        widget.installEventFilter(widget)
        result = widget.eventFilter(widget, self._make_fake_tooltip_event())

        # This is true if a tooltip was requested
        self.assertTrue(result)

    def test_parent_event_filter(self):
        def acknowledgement(self, obj, event, data=None):  # pylint: disable=unused-argument
            data['ran'] = True
            return False

        data = dict()
        widget = QtWidgets.QLabel('some widget')

        widget.__class__.eventFilter = functools.partial(acknowledgement, data=data)

        url = 'http://google.com'
        qweburltip.override_tool_tip(widget, url)
        widget.installEventFilter(widget)
        widget.eventFilter(widget, self._make_fake_tooltip_event())

        # This is true if a tooltip was requested
        self.assertTrue(data.get('ran', False))
