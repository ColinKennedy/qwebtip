#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A set of classes for interacting with website URLs."""

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
from six.moves import urllib
from Qt import QtCore


class _BaseSelector(object):
    """Select some part of a URL and move the browser to that location."""

    def __init__(self, url):
        """Store a URL to query later.

        Args:
            url (str): Some addressable website to view.

        """
        super(_BaseSelector, self).__init__()
        self.url = url

    @staticmethod
    def move_to_selector(
        browser, selectors, text, *args
    ):  # pylint: disable=unused-argument
        """Find the location of a selector with `text` and position browser to it.

        This method will find the first matching selector for some `text`.

        Args:
            browser (`QtWebKit.QWebView`):
                The browser whose scroll position will be affected.
            selectors (list[str]):
                Some possible CSS elements that could match `text`.
                Examples: ["a", "h1", "h2", "td"] and more.
            text (str):
                Some text to find.
            args (tuple[bool]):
                Unused values which are passed by `QtWebKit.QWebView.loadFinished`.

        """
        permutations = {text, text.replace("-", " ")}

        for selector in selectors:
            elements = browser.page().mainFrame().findAllElements(selector)

            for index, element in enumerate(elements):
                if element.toPlainText() in permutations:
                    position = elements.at(index).geometry()
                    point = QtCore.QPoint(position.x(), position.y())
                    browser.page().mainFrame().setScrollPosition(point)
                    return

    def get_url(self):
        """str: Get the stored web address."""
        return self.url


class Link(_BaseSelector):
    """A class that scrolls a browser to some clickable location."""

    def setup(self, browser):
        """Add a signal to `browser` which will auto-scroll it to the URL's link.

        If the stored URL has no link location then don't do anything.

        Args:
            browser (`QtWebKit.QWebView`):
                The browser whose scroll position will be affected.

        """
        def load_top_of_page(browser, *args):  # pylint: disable=unused-argument
            """Set the webpage to load from the top of the page."""
            browser.page().mainFrame().setScrollPosition(QtCore.QPoint(0, 0))

        # Note: The URL fragment is expected to of the form wwww.foo.com/whatever#bar
        # where "wwww.foo.com/whatever" is the URL and "bar" is the fragment
        # and the-scroll position on the page to go to
        #
        data = urllib.parse.urlparse(self.get_url())

        if not data.fragment:
            browser.loadFinished.connect(functools.partial(load_top_of_page, browser))
            return

        post_move = functools.partial(
            self.move_to_selector, browser, ("a",), "{data.fragment}".format(data=data)
        )

        browser.loadFinished.connect(post_move)


class UnknownSelector(_BaseSelector):
    """A class that helps scrolls a browser for an undefined CSS selector.

    This class is useful if you expect your documentation to change.
    For example, you may have a header text that you want to scroll to in mind.
    Right now, it is h1 but later it gets changed to h2. This class lets you
    search for the text in h1 first and fallback to h2 if it can't find it.

    """

    def __init__(self, url, text, selectors):
        """Store some text to search for and the CSS element selectors that we expect.

        Note:
            `text` is searched for in each of the CSS `selectors` in the order
            that they are defined,

        Args:
            url (str): Some addressable website to view.
            text (str): Some text to scroll to.
            selectors (list[str]): Some CSS elements that could match `text`.
                                   Examples: ["a", "h1", "h2", "td"] and more.

        """
        super(UnknownSelector, self).__init__(url)
        self.text = text
        self.selectors = selectors

    def setup(self, browser):
        """Add a signal to `browser` which will auto-scroll it to some selector.

        If a selector cannot be found then the browser's scroll value is not found.

        """
        post_move = functools.partial(
            self.move_to_selector, browser, self.selectors, self.text
        )

        browser.loadFinished.connect(post_move)


class UnknownHeaderSelector(UnknownSelector):
    """A class that helps scrolls a browser for an undefined CSS selector.

    This class is useful if you expect your documentation to change.
    For example, you may have a header text that you want to scroll to in mind.
    Right now, it is h1 but later it gets changed to h2. This class lets you
    search for the text in h1 first and fallback to h2 if it can't find it.

    """

    def __init__(self, url, text, selectors=("h1", "h2", "h3", "h4", "h5", "h6")):
        """Store some text to search for and the CSS element selectors that we expect.

        Note:
            `text` is searched for in each of the CSS `selectors` in the order
            that they are defined,

        Args:
            url (str): Some addressable website to view.
            text (str): Some text to scroll to.
            selectors (list[str], optional):
                Some CSS elements that could match `text`.
                Default: ("h1", "h2", "h3", "h4", "h5", "h6").

        """
        super(UnknownHeaderSelector, self).__init__(url, text, selectors)
