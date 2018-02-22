# -*- coding:utf-8 -*-

import weakref

__all__ = [
    'Abstract',
    'AbstractDescriptor',
    'Default']


class AbstractDescriptor(object):
    def __init__(self):
        self._resolve_cache = weakref.WeakKeyDictionary()

    def _resolve_name(self, owner):
        try:
            return self._resolve_cache[owner]
        except KeyError:
            pass

        for name in dir(owner):
            try:
                attr = getattr(owner, name)
            except AttributeError:
                continue
            if attr is not self:
                continue
            break
        else:
            raise RuntimeError(
                '{!r} Unable to resolve bounded name (UNREACHABLE)'.format(
                    self))

        self._resolve_cache[owner] = name
        return name


class Default(AbstractDescriptor):
    def __init__(self, value, produce=False):
        super().__init__()
        self.value = value
        self.produce = produce

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = self.value
        if self.produce:
            value = value()

        setattr(instance, self._resolve_name(owner), value)
        return value

    def is_filled(self, instance):
        name = self._resolve_name(type(instance))
        data = vars(instance)
        return name in data


class Abstract(object):
    def __init__(self, **fields):
        cls = type(self)
        extra = set()
        for name in fields:
            extra.add(name)
            try:
                attr = getattr(cls, name)
            except AttributeError:
                continue
            if not isinstance(attr, Default):
                continue

            extra.remove(name)
            setattr(self, name, fields[name])

        if extra:
            raise TypeError('{!r} got unknown arguments: "{}"'.format(
                self, '", "'.join(sorted(extra))))
