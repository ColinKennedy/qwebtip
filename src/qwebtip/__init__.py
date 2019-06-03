#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dynamically bind Qt.py so that QtWebKit can be imported using `six`.

At the time of writing Qt.py does not have bindings for QtWebKit. Probably
because QtWebKit is an optional Qt library.

But we don't want to explicitly import from PySide.QtWebKit, PyQt4.QtWebKit, etc.
because then Qt.py is being forced to use a library.

So instead, we find the library that Qt.py imported (it's `__binding__`) and
grab `QtWebKit` from that, instead.

"""

# IMPORT THIRD-PARTY LIBRARIES
import six
import Qt


try:
    __QT_MODULE = __import__(Qt.__binding__)  # pylint: disable=no-member
except ImportError:
    raise EnvironmentError("You must install some Qt library to use this module")

__MODULE = six.MovedModule(
    "QtWebKit", __QT_MODULE.__name__ + ".QtWebKit", __QT_MODULE.__name__ + ".QtWebKit"
)
six.add_move(__MODULE)

try:
    from six.moves import QtWebKit as __QtWebKit  # pylint: disable=ungrouped-imports

    _ = __QtWebKit.QWebView
except (ImportError, AttributeError):
    raise EnvironmentError(
        'Qt binding "{binding}" does not have QtWebKit included.'.format(
            binding=Qt.__binding__  # pylint: disable=no-member
        )
    )
