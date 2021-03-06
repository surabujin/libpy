# -*- coding:utf-8 -*-

import weakref


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


class Alias(AbstractDescriptor):
    def __init__(self, path, *tail):
        super().__init__()

        self.path = [path]
        self.path.extend(tail)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.resolve(instance)[-1]

    def __set__(self, instance, value):
        trace = self.resolve(instance, exclude_last=True)
        trace.insert(0, instance)
        trace.reverse()
        steps = reversed(self.path)

        for adapter, current in zip(steps, trace):
            value = adapter.write(current, value)
            if value is current:
                break
        else:
            # need to replace root item
            raise AttributeError(
                'Invalid alias setup - trying to write outside of aliased '
                'scope.')

    def resolve(self, instance, exclude_last=False):
        trace = []

        target, idx = instance, 0
        path = self.path
        if exclude_last:
            path = path[:-1]

        try:
            for idx, adapter in enumerate(path):
                target = adapter.read(target)
                trace.append(target)
        except AliasAdapterError:
            raise AttributeError(
                'Unresolvable alias {!r}. Lookup failed at {!r}.{}'.format(
                    self._resolve_name(type(instance)), instance,
                    ''.join(self.path[:idx])))

        return trace


class AliasAdapter(object):
    def __init__(self, name):
        self.name = name

    def read(self, target):
        raise NotImplementedError

    def write(self, target, value):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class AttrAdapter(AliasAdapter):
    def read(self, target):
        try:
            value = getattr(target, self.name)
        except AttributeError:
            raise AliasAdapterError
        return value

    def write(self, target, value):
        setattr(target, self.name, value)
        return target

    def __str__(self):
        return '.{}'.format(self.name)


class ItemAdapter(AliasAdapter):
    def read(self, target):
        try:
            value = target[self.name]
        except (KeyError, IndexError):
            raise AliasAdapterError
        return value

    def write(self, target, value):
        target[self.name] = value
        return target

    def __str__(self):
        return '[{!r}]'.format(self.name)


class AliasAdapterError(Exception):
    pass
