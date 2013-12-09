# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from itertools import repeat


class _ProxyAttr(object):
    def __init__(self, item, attr='args'):
        self.item = item
        self.attr = attr

    def __get__(self, instance, owner):
        if not instance:
            return self

        attr = getattr(instance, self.attr)
        try:
            value = attr[self.item]
        except IndexError:
            name = instance.idx_to_attr(self.item)
            raise AttributeError('\'{}\' object has no attribute \'{}\''.format(owner.__name__, name))
        return value

    def __set__(self, instance, value):
        name = instance.idx_to_attr(self.item)
        instance.update(name, value)


class _ExcMeta(type):
    def __new__(mcs, name, bases, dict_):
        cls = super(_ExcMeta, mcs).__new__(mcs, name, bases, dict_)

        dfl = dict()
        for i, a in enumerate(cls.attr_map):
            assert isinstance(a, (str, unicode))
            get = _ProxyAttr(i)
            try:
                dfl[a] = getattr(cls, a)
            except AttributeError:
                pass
            setattr(cls, a, get)

        cls.merge_defaults(dfl)
        return cls


class CommonException(Exception):
    __metaclass__ = _ExcMeta

    attr_map = tuple()
    _dfl = tuple()

    @classmethod
    def merge_defaults(cls, dfl):
        curr = dict(cls._dfl)
        for k, v in dfl.iteritems():
            curr.setdefault(k, v)
        cls._dfl = tuple(curr.items())

    def __init__(self, *a, **kwa):
        Exception.__init__(self, *a)

        for n, v in self._dfl:
            try:
                if getattr(self, n):
                    continue
            except AttributeError:
                pass
            self.update(n, v)
        for n, v in kwa.iteritems():
            self.update(n, v)

    def update(self, fld, value):
        try:
            idx = self.attr_map.index(fld)
        except ValueError:
            setattr(self, fld, value)
            return

        a = self.args
        a = list(a)
        if len(a) <= idx:
            a.extend(repeat(None, idx - len(a) + 1))
        a[idx] = value

        # noinspection PyPropertyAccess
        self.args = tuple(a)

    def idx_to_attr(self, idx):
        return self.attr_map[idx]


class CommonCtrl(CommonException):
    pass


class CommonError(CommonException):
    attr_map = ('message',)
    message = None
