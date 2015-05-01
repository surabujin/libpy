import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

deps = []
deps_test = [
    'pytest>=2.7.0',
    'mock>=1.0.1']

entry_points = {}


# TODO: try to find better integration with py.test
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def __init__(self, dist, **kwa):
        TestCommand.__init__(self, dist, **kwa)
        self.pytest_args = []
        self.test_suite = '-dummy-'

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='libpy',
    version='0.2rc0',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    packages=find_packages(),
    entry_points=entry_points,

    install_requires=deps,
    tests_require=deps_test,

    include_package_data=True,
    zip_safe=True,

    cmdclass={
        'test': PyTest},

    # metadata for upload to PyPI
    author='Dmitry Bogun',
    author_email='surabujin@surabujin.org.ua',
    description='A set of tools for common python application',
    #license='',
    keywords='library tooolbox tools',
    url='https://github.com/surabujin/libpy')
