#!/usr/bin/env python
from codecs import open
from os import path
import re

from setuptools import setup, find_packages


RE_VERSION = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-([^$]+))?$')

here = path.abspath(path.dirname(__file__))

# Acquire description from README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Acquire project versionn from CHANGELOG's first line
with open(path.join(here, 'CHANGELOG')) as f:
    for line in f.readlines():
        version_tuple = RE_VERSION.match(line.strip()).groups()
        version_str = '.'.join(version_tuple[:3])
        break

setup(
    name='soda-pylib',
    version=version_str,
    description='Utilities to help projets at SODA Virtual.',
    long_description=long_description,

    # Distributed packages
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # The project's main homepage.
    url='https://gitlab.com/sodavirtual/soda-pylib',

    # Author details
    author='Evandro Myller',
    author_email='emyller@7ws.co',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='deploy fabric',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Fabric3',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },
)
