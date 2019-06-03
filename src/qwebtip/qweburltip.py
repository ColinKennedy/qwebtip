#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""An override which can make any `QtWidgets.QWidget` display a web-page as a tooltip.

Example:
    >>> import renderer
    >>> label = QtWidgets.QLabel('I am a test')
    >>> label.installEventFilter(label)
    >>> url = "http://pyqt.sourceforge.net/Docs/PyQt4/qwebframe.html"
    >>> renderer.override_tool_tip(label, url)

"""

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
from six.moves import QtWebKit
from Qt import QtCore
import six

# IMPORT LOCAL LIBRARIES
from . import cache
from . import element_selector

_DEFAULT_WIDTH = 400
_DEFAULT_HEIGHT = 300


class SelfClosingBrowser(QtWebKit.QWebView):  # pylint: disable=too-few-public-methods
    """Create a QWebView that closes itself when the cursor moves away from it."""

    def __init__(self, parent=None):
        """Set up this instance to check for a "Leave" event.

        If the `QtCore.QEvent.Leave` event triggers, close this instance.

        Args:
            parent (`QtCore.QObject`, optional):
                Qt-based associated object. Default is None.

        """
        super(SelfClosingBrowser, self).__init__(parent=parent)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):  # pylint: disable=invalid-name,unused-argument
        """bool: Close this instance if the user moved their cursor off of it."""
        if event.type() == QtCore.QEvent.Leave:
            self.close()

            return True

        return False


@cache.memoize_function
def make_browser(
    descriptor, width=_DEFAULT_WIDTH, height=_DEFAULT_HEIGHT, creator=SelfClosingBrowser
):
    """When a user requests a tooltip, show a browser window instead.

    Important:
        This is meant to be used in-place of an instancemethod.

    Args:
        descriptor (`element_selector._BaseSelector`):
            An object that initializes the browser to a particular start position.
        width (int, optional):
            How wide the created browser will be. Default: 400.
        height (int, optional):
            How tall the created browser will be. Default: 300.
        creator (`element_selector._BaseSelector`):
            The object that controls the starting scroll position of the
            created browser widget, along with any other settings.

    Returns:
        bool: If a tooltip browser was displayed. A bool is required by Qt or
              `eventFilter` will raise exceptions.

    """
    browser = creator()
    browser.setWindowFlags(QtCore.Qt.ToolTip)
    browser.resize(width, height)

    browser.load(QtCore.QUrl(descriptor.get_url()))
    descriptor.setup(browser)

    return browser


def event_filter(descriptor, size, creator, obj, event):
    """When a user requests a tooltip, show a browser window instead.

    Important:
        This is meant to be used in-place of an instancemethod.

    Args:
        descriptor (`element_selector._BaseSelector`):
            An object that initializes the browser to a particular start position.
        size (tuple[int, int]):
            How wide and tall the created browser will be.
        creator (`element_selector._BaseSelector`):
            The object that controls the starting scroll position of the
            created browser widget, along with any other settings.
        obj (`QtWidgets.QWidget`):
            The instance that called this event.
        event (`QtCore.QEvent`):
            An event that is passed when a widget's `eventFilter` method is called.
            It contains the relative position for where our browser should be shown.

    Returns:
        bool: If a tooltip browser was displayed. A bool is required by Qt or
              `eventFilter` will raise exceptions.

    """
    obj.__class__.eventFilter(obj, obj, event)  # Call the base-class `eventFilter`

    if event.type() != QtCore.QEvent.ToolTip:
        return False

    width, height = size
    position = obj.mapToGlobal(event.pos())

    # Move the tooltip just a tiny bit inside of the user's cursor.
    # This is completely optional but it keeps the user from
    # accidentally closing out of the browser window early
    #
    offset = 7
    position.setX(position.x() - offset)
    position.setY(position.y() - offset)

    browser = make_browser(descriptor, width, height, creator)

    browser.move(QtCore.QPoint(position.x(), position.y()))
    browser.show()

    return True


def override_tool_tip(
    widget,
    descriptor,
    width=_DEFAULT_WIDTH,
    height=_DEFAULT_HEIGHT,
    creator=SelfClosingBrowser,
):
    """Change `widget` to display a browser tooltip.

    Important:
        This function will override the `eventFilter` method of `widget`.

    Args:
        widget (`QtWidgets.QWidget`):
            The instance that called this event.
        descriptor (`element_selector._BaseSelector`):
            An object that initializes the browser to a particular start position.
        width (int, optional):
            How wide the created browser will be. Default: 400.
        height (int, optional):
            How tall the created browser will be. Default: 300.
        creator (`element_selector._BaseSelector`):
            The object that controls the starting scroll position of the
            created browser widget, along with any other settings.

    Returns:
        bool: If a tooltip browser was displayed. A bool is required by Qt or
              `eventFilter` will raise exceptions.

    """
    if isinstance(descriptor, six.string_types):
        descriptor = element_selector.Link(descriptor)

    widget.eventFilter = functools.partial(
        event_filter, descriptor, (width, height), creator
    )
