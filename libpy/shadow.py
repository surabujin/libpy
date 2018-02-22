# -*- coding:utf-8 -*-

import weakref


class Shadow(object):
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
                self, target, attr))
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
