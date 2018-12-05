========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
        | |landscape| |codacy|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/qwebtip/badge/?style=flat
    :target: https://readthedocs.org/projects/qwebtip
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/ColinKennedy/qwebtip.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ColinKennedy/qwebtip

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ColinKennedy/qwebtip?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ColinKennedy/qwebtip

.. |requires| image:: https://requires.io/github/ColinKennedy/qwebtip/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ColinKennedy/qwebtip/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/ColinKennedy/qwebtip/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ColinKennedy/qwebtip

.. |landscape| image:: https://landscape.io/github/ColinKennedy/qwebtip/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ColinKennedy/qwebtip/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/ColinKennedy/qwebtip
    :alt: Codacy Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/qwebtip.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/qwebtip

.. |commits-since| image:: https://img.shields.io/github/commits-since/ColinKennedy/qwebtip/v0.1dev.svg
    :alt: Commits since latest release
    :target: https://github.com/ColinKennedy/qwebtip/compare/v0.1dev...master

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

A Qt package that lets you use web URLs as tooltips in Qt widgets

* Free software: BSD 2-Clause License

Installation
============

::

    pip install qwebtip

Documentation
=============


https://qwebtip.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
