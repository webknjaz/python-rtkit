from setuptools import setup, find_packages
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
)
