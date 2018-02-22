# -*- coding:utf-8 -*-

import pytest

from libpy import root


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


class DefaultSubject(root.Abstract):
    first = root.Default('first')  # type: str
    second = root.Default(lambda: 'second', produce=True)  # type: str
