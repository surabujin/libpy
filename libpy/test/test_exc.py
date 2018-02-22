# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import pytest

from libpy import exc


class Subject(exc.CommonException):
    attr_map = ('attr0', 'attr1')
    attr0 = 'pass'


def test_proxy_access():
    subj = Subject()
    assert isinstance(subj.__class__.attr0, exc._ProxyAttr)


def _validate_subj_attrs(subj, expect):
    attr = ('attr0', 'attr1')
    assert subj.args == expect
    for attr, value in zip(attr, expect):
        assert getattr(subj, attr) == value


@pytest.mark.parametrize(('a', 'kwa', 'expect'), [
    ((),                 {},                  ('pass',)),
    (('ovr',),           {},                  ('ovr',)),
    (('ovr',),           {'attr0': 'kw-ovr'}, ('kw-ovr',)),
    (('ovr1', 'ovr2',),  {},                  ('ovr1', 'ovr2'))
])
def test_attr_dfl(a, kwa, expect):
    subj = Subject(*a, **kwa)
    _validate_subj_attrs(subj, expect)


@pytest.mark.parametrize(('attr', 'value', 'expect'), [
    ('attr0',  'value0', ('value0',)),
    ('attr1',  'value1', ('pass', 'value1')),
    ('custorm', 'extra', ('pass',))
])
def test_attr_set(attr, value, expect):
    subj = Subject()
    setattr(subj, attr, value)
    _validate_subj_attrs(subj, expect)


@pytest.mark.parametrize(('attr', 'value', 'expect'), [
    ('attr0',  'value0', ('value0',)),
    ('attr1',  'value1', ('pass', 'value1')),
    ('custorm', 'extra', ('pass',))
])
def test_update(attr, value, expect):
    subj = Subject()
    subj.update(attr, value)
    _validate_subj_attrs(subj, expect)
