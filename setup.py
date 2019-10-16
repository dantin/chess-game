# -*- coding: utf-8 -*-
"""Setup Scripts."""

import io
import re

from setuptools import setup, find_packages


with io.open('README.md', 'rt', encoding='utf8') as f:
    README = f.read()

with io.open('chess/__init__.py', 'rt', encoding='utf8') as f:
    VERSION = re.search(r'__version__ = \'(.*?)\'', f.read()).group()

setup(
    name='chess',
    version=VERSION,
    description='Chess Game utilities',
    long_description=README,
    author='David Ding',
    author_email='chengjie.ding@gmail.com',
    url='https://github.com/dantin/chess-game',
    license='BSD',
    packages=find_packages(exclude=('tests', 'misc', 'htmlcov', '*.egg-info')),
    install_requires=[
        'imageio>=2.6.1',
        'numpy>=1.17.2',
    ],
    extras_require={
        'test': [
            'tox>=3.14.0',
        ],
    },
)
