# -*- coding:utf-8 -*-

import collections

import weakref
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
        raise TypeError(
            'Object {!r} have failed to resolve lazy attribute {!r}'.format(
                self, target.name))
 

class Proxy(object):
    def __init__(self, target, **init):
        _update_object_mapping(self, target)
        for attr, val in init.items():
            setattr(self, attr, val)

    def __getattr__(self, attr):
        target = None

        try:
            target = _lookup_object_mapping(self)
            if attr.startswith('_'):
                raise AttributeError
            value = getattr(target, attr)
        except KeyError:
            raise AttributeError(_make_proxy_attr_error_message(
                self,  target, attr))
        except AttributeError:
            raise AttributeError(_make_proxy_attr_error_message(
                self, target, attr))

        setattr(self, attr, value)
        return value


def _make_proxy_attr_error_message(proxy, target, attr):
    proxy = type(proxy)
    if target is None:
        target = '???'
    else:
        target = type(target)
    return '{}=>{} object has no attribute \'{}\''.format(proxy, target, attr)


def _lookup_object_mapping(instance):
    return _object_mapping[instance]


def _update_object_mapping(instance, value):
    _object_mapping[instance] = value


_object_mapping = weakref.WeakKeyDictionary()
