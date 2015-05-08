# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import mock
import pytest

import libpy
import libpy.cache


class Subject(object):
    @libpy.lazy_property
    def attr0(self):
        return 'dummy'


@pytest.fixture
def factory():
    return mock.Mock(return_value='test')


@pytest.fixture
def obj(monkeypatch, factory):
    monkeypatch.setattr(Subject.attr0, '_factory', factory)
    return Subject()


class TestLazyProperty(object):
    def test_generic(self, obj, factory):
        assert isinstance(Subject.attr0, libpy.cache.LazyProperty)
        assert 'attr0' not in vars(obj)

        # evaluate property on first call
        assert 'test' == obj.attr0
        # property should not be called on second request
        assert 'test' == obj.attr0

        factory.assert_called_once_with(obj)

    def test_manual_fill(self, obj, factory):
        obj.attr0 = 'test1'

        assert obj.attr0 == 'test1'
        assert not factory.called

    def test_clear(self, obj):
        with pytest.raises(AttributeError):
            del obj.attr0

        assert obj.attr0 == 'test'
        del obj.attr0
        assert 'attr0' not in vars(obj)

    def test_recalculate(self, obj, factory):
        assert obj.attr0 == 'test'
        assert factory.call_count == 1

        del obj.attr0
        assert obj.attr0 == 'test'
        assert factory.call_count == 2


class TestProxy(object):
    def test(self):
        proxy = libpy.cache.Proxy(ProxyTarget())

        assert isinstance(proxy, libpy.cache.Proxy)
        assert proxy.a == mock.sentinel.proxy_target_a
        assert proxy.b == mock.sentinel.proxy_target_b

        with pytest.raises(AttributeError):
            _ = proxy.X

        with pytest.raises(AttributeError):
            _ = proxy._c

    def test_keep_value(self):
        target = ProxyTarget()
        proxy = libpy.cache.Proxy(target)

        assert proxy.b == mock.sentinel.proxy_target_b

        delattr(target, 'b')
        assert not hasattr(target, 'b')

        assert proxy.b == mock.sentinel.proxy_target_b

        delattr(proxy, 'b')
        with pytest.raises(AttributeError):
            _ = proxy.b

    def test_update(self):
        target = ProxyTarget()
        proxy = libpy.cache.Proxy(target)

        assert proxy.a == mock.sentinel.proxy_target_a
        target.a = 'new_value_for_a'
        assert proxy.a == mock.sentinel.proxy_target_a

        delattr(proxy, 'a')
        assert proxy.a == 'new_value_for_a'

    def test_override(self):
        proxy = libpy.cache.Proxy(ProxyTarget(), a='override_a')

        assert proxy.a == 'override_a'
        assert proxy.b == mock.sentinel.proxy_target_b
        proxy.b = 'dynamic_override_b'
        assert proxy.b == 'dynamic_override_b'


class ProxyTarget(object):
    a = mock.sentinel.proxy_target_a

    def __init__(self):
        self.b = mock.sentinel.proxy_target_b
        self._c = mock.sentinel.proxy_target_c
