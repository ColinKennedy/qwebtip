#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Reference: https://dbader.org/blog/python-memoization
def memoize_function(function):
    cache = dict()

    def memoized_function(*args):
        if args in cache:
            return cache[args]

        result = function(*args)
        cache[args] = result

        return result

    return memoized_function
