# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import pytest

from libpy import cache
from libpy import exc


class TestLazyProperty(object):
    def test(self):
        a = LazyPropertySubject()
        assert a.first == 'FIRST'
        assert a.called == 1
        assert a.first == 'FIRST'
        assert a.called == 1  # value must be cached, so no second call

        with pytest.raises(exc.UnresolvedLazyAttr):
            assert a.second is None

        assert a.called == 2

    def test_override(self):
        a = LazyPropertySubject()
        a.first = 'AAA'
        assert a.first == 'AAA'

        del a.first
        assert a.first == 'FIRST'


class LazyPropertySubject(cache.LazyMixin, object):
    first = cache.LazyAttr()
    second = cache.LazyAttr()

    called = 0

    def lazy_attr(self, target):
        self.called += 1

        if target.attr is type(self).first:
            value = 'FIRST'
        else:
            value = super().lazy_attr(target)
        return value
