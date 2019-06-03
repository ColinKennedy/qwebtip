#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that stores computed results so that they can be reused."""

# IMPORT STANDARD LIBRARIES
import os


# Reference: https://dbader.org/blog/python-memoization
def memoize_function(function):
    """Create a cache for the given `function`.

    Important:
        This wrapper does not work with functions that take keywords and each
        arg must be hashable.

    Args:
        function (callable): Some function to store the information of.

    Returns:
        callable: A new function which can create/get cached results.

    """
    cache = dict()

    def memoized_function(*args):
        """Cache the results.

        Args:
            *args (tuple): The objects that were passed by the user to `function`.

        Returns:
            The result of `function(*args)`.

        """
        disable_caching = os.getenv("QWEBTIP_DISABLE_CACHING", "0") == "1"
        if disable_caching:
            return function(*args)

        if args in cache:
            return cache[args]

        result = function(*args)
        cache[args] = result

        return result

    return memoized_function
