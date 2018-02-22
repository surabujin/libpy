# -*- coding:utf-8 -*-

import collections

from . import exc
from .root import AbstractDescriptor


_LazyDescriptor = collections.namedtuple('_LazyDescriptor', ('attr', 'name'))


class LazyAttr(AbstractDescriptor):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        target = _LazyDescriptor(self, self._resolve_name(owner))
        result = instance.lazy_attr(target)
        self._save(target.name, instance, result)

        return result

    @staticmethod
    def _save(name, instance, result):
        setattr(instance, name, result)


class LazyMixin(object):
    def lazy_attr(self, target):
        raise exc.UnresolvedLazyAttr(self, target)
