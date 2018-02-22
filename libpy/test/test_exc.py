# -*- coding:utf-8 -*-

from libpy import exc


class TestExc(object):
    def test_defaults(self):
        a = ExcSubject()
        assert a.args == ('first', 'second')

        b = ExcSubject('AAA')
        assert b.args == ('AAA', 'second')

        c = ExcSubject('AAA', 'BBB')
        assert c.args == ('AAA', 'BBB')

        d = ExcSubject('AAA', 'BBB', 'CCC')
        assert d.args == ('AAA', 'BBB', 'CCC')

    def test_atr_alias(self):
        a = ExcSubject()

        assert a.first == 'first'
        assert a.second == 'second'
        assert a.third is None

    def test_atr_alias_write(self):
        a = ExcSubject()

        a.first = 'AAA'
        assert a.first == 'AAA'
        assert a.args == ('AAA', 'second')

        a.third = 'CCC'
        assert a.third == 'CCC'
        assert a.args == ('AAA', 'second', 'CCC')


class ExcSubject(exc.AbstractException):
    defaults = ('first', 'second')
    first = exc.make_arg_alias(0)
    second = exc.make_arg_alias(1)
    third = exc.make_arg_alias(2)
