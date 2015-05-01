# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import functools


class LazyProperty(object):
    def __init__(self, factory):
        self._factory = factory

        functools.update_wrapper(self, self._factory)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        try:
            get_factory = self._factory.__get__
        except AttributeError:
            result = self._factory(instance)
        else:
            bound_factory = get_factory(instance, owner)
            result = bound_factory()

        setattr(instance, self.__name__, result)

        return result
