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
