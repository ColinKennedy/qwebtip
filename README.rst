========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |requires|
        | |codacy|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|


.. |requires| image:: https://requires.io/github/ColinKennedy/qwebtip/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ColinKennedy/qwebtip/requirements/?branch=master

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/7e73dd8eb05349b08006732e8152c22d
    :target: https://app.codacy.com/app/ColinKennedy/qwebtip?utm_source=github.com&utm_medium=referral&utm_content=ColinKennedy/qwebtip&utm_campaign=Badge_Grade_Dashboard
    :alt: Codacy Badge

.. |version| image:: https://img.shields.io/pypi/v/qwebtip.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/qwebtip

.. |commits-since| image:: https://img.shields.io/github/commits-since/ColinKennedy/qwebtip/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ColinKennedy/qwebtip/compare/v0.2.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/qwebtip.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/qwebtip

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/qwebtip.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/qwebtip

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/qwebtip.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/qwebtip


.. end-badges

A Qt package that lets you use web URLs as tooltips in Qt widgets.

* Free software: BSD 2-Clause License


Requires
========

PySide or PyQt4 with QtWebKit included.


Installation
============

::

    pip install qwebtip


How To Use
==========


Import qwebtip's main model, `qweburltip` and set it to override one of
your widget's tooltips with some URL.

The next time you build your application and hover over that widget, a URL box
is displayed with that URL, instead.


.. code:: python

   from qwebtip import qweburltip

   url = 'http://pyqt.sourceforge.net/Docs/PyQt4/qwebframe.html'
   qweburltip.override_tool_tip(QtWidgets.QLabel('Some label'), url)


How To Use - Customizing
========================


Setting a custom tooltip size

.. code:: python

   from qwebtip import qweburltip

   url = 'http://pyqt.sourceforge.net/Docs/PyQt4/qwebframe.html'
   qweburltip.override_tool_tip(
      QtWidgets.QLabel('Some label'),
      url,
      width=100,
      height=400,
   )

Opening the URL at a specific header section


.. code:: python

   url = 'http://pyqt.sourceforge.net/Docs/PyQt4/qwebframe.html'
   qweburltip.override_tool_tip(
      self.line_edit,
      element_selector.UnknownHeaderSelector(
          url,
          'Method Documentation',
      ),
   )


Disabling Caching
=================

Loaded webpages are cached so that successive loads can be kept fast.
To disable caching, set this environment variable.


.. code:: bash

   export QWEBTIP_DISABLE_CACHING=1

This is useful for debugging but is not recommended.
