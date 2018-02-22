# -*- coding:utf-8 -*-

import pytest

from libpy import root


class TestAlias(object):
    def test(self):
        subject = AliasSubject()

        assert subject.attr_alias == subject.attr_target
        assert subject.item_alias == subject.attr_target[1]

        subject.item_alias = 'Z'
        assert subject.item_alias == 'Z'
        assert subject.attr_target == list('AZC')

        subject.attr_alias = 'REWRITE'
        assert subject.attr_alias == 'REWRITE'
        assert subject.item_alias == 'E'
        assert subject.attr_target == 'REWRITE'


class TestDefault(object):
    def test(self):
        a = DefaultSubject()

        assert a.first == 'first'
        assert a.second == 'second'

        # override
        a.first = 'ABC'
        assert a.first == 'ABC'

        b = DefaultSubject(first='AAA')
        assert b.first == 'AAA'

        with pytest.raises(TypeError):
            DefaultSubject(z='ZZZ')


class AliasSubject(object):
    attr_alias = root.Alias(
        root.AttrAdapter('attr_target'))
    item_alias = root.Alias(
        root.AttrAdapter('attr_target'),
        root.ItemAdapter(1))

    attr_target = list('ABC')


class DefaultSubject(root.Abstract):
    first = root.Default('first')  # type: str
    second = root.Default(lambda: 'second', produce=True)  # type: str
