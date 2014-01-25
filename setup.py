from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import os

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'python-rtkit'
pkg = __import__('rtkit')

author, email = pkg.__author__.rsplit(' ', 1)
email = email.strip('<>')

version = pkg.__version__
classifiers = pkg.__classifiers__

readme = open(os.path.join(wd, 'README.rst'),'r').readlines()
description = readme[1]
long_description = ''.join(readme)

try:
    reqs = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['rtkit/tests']
        #self.test_args = ['--doctest-modules', '--pep8', 'rtkit', '-v',
        #                  '--cov', 'rtkit', '--cov-report', 'term-missing']
        self.test_suite = True

    def run_tests(self):
        from pkg_resources import _namespace_packages
        import pytest

        def normalize_path(p):
            p = '/'.join([p, self.test_args[0]])
            return p

        if sys.version_info >= (3,) and getattr(self.distribution, 'use_2to3', False):
            module = self.test_args[-1].split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)
            del sys.modules['rtkit']

            ei_cmd = self.get_finalized_command("egg_info")
            self.test_args = [normalize_path(ei_cmd.egg_base)]

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    url='http://z4r.github.com/python-rtkit/',
    maintainer=author,
    maintainer_email=email,
    description=description,
    long_description=long_description,
    classifiers=classifiers,
    use_2to3=True,
    install_requires = reqs,
    packages=find_packages(),
    license = 'Apache License 2.0',
    keywords ='RequestTracker REST',
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
