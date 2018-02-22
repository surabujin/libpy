# -*- coding:utf-8 -*-

import mock
import pytest

import libpy
import libpy.shadow


class TestShadow(object):
    def test(self):
        proxy = libpy.shadow.Shadow(ShadowTarget())

        assert isinstance(proxy, libpy.shadow.Shadow)
        assert proxy.a == mock.sentinel.proxy_target_a
        assert proxy.b == mock.sentinel.proxy_target_b

        with pytest.raises(AttributeError):
            _ = proxy.X

        with pytest.raises(AttributeError):
            _ = proxy._c

    def test_keep_value(self):
        target = ShadowTarget()
        proxy = libpy.shadow.Shadow(target)

        assert proxy.b == mock.sentinel.proxy_target_b

        delattr(target, 'b')
        assert not hasattr(target, 'b')

        assert proxy.b == mock.sentinel.proxy_target_b

        delattr(proxy, 'b')
        with pytest.raises(AttributeError):
            _ = proxy.b

    def test_update(self):
        target = ShadowTarget()
        proxy = libpy.shadow.Shadow(target)

        assert proxy.a == mock.sentinel.proxy_target_a
        target.a = 'new_value_for_a'
        assert proxy.a == mock.sentinel.proxy_target_a

        delattr(proxy, 'a')
        assert proxy.a == 'new_value_for_a'

    def test_override(self):
        proxy = libpy.shadow.Shadow(ShadowTarget(), a='override_a')

        assert proxy.a == 'override_a'
        assert proxy.b == mock.sentinel.proxy_target_b
        proxy.b = 'dynamic_override_b'
        assert proxy.b == 'dynamic_override_b'


class ShadowTarget(object):
    a = mock.sentinel.proxy_target_a

    def __init__(self):
        self.b = mock.sentinel.proxy_target_b
        self._c = mock.sentinel.proxy_target_c
