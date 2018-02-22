# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from itertools import repeat

from ._root import Alias
from ._root import AttrAdapter
from ._root import ItemAdapter


class ArgsAdapter(ItemAdapter):
    def __init__(self, name):
        if not isinstance(name, int):
            raise TypeError('{} can use ony number as field name'.format(
                type(self)))
        super().__init__(name)

    def read(self, target):
        try:
            value = target[self.name]
        except IndexError:
            value = None
        return value

    def write(self, target, value):
        args = list(target)
        if len(args) <= self.name:
            args.extend(repeat(None, self.name - len(args) + 1))
        args[self.name] = value

        return tuple(args)


def make_arg_alias(index):
    return Alias(
        AttrAdapter('args'),
        ArgsAdapter(index))


class AbstractException(Exception):
    defaults = ()

    def __init__(self, *a, **kwa):
        args = a
        if len(args) < len(self.defaults):
            args = args + self.defaults[len(args):]
            args = args[:len(self.defaults)]
        super().__init__(*args)

        for attr, value in kwa.items():
            setattr(self, attr, value)


class AbstractCtrl(AbstractException):
    pass


class AbstractError(AbstractException):
    defaults = ('Abstract error being used', )
    message = make_arg_alias(0)


class UnresolvedLazyAttr(AbstractError):
    owner = make_arg_alias(0)
    target = make_arg_alias(1)

    def __init__(self, owner, target):
        super(UnresolvedLazyAttr, self).__init__(owner, target)

    @property
    def message(self):
        return 'Object {!r} have failed to resolve lazy attribute {!r}'.format(
            self.owner, self.target.name)
