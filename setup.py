#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import sys

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'TrainTrack'
DESCRIPTION = 'Track metrics and progress when training deep learning models.'
URL = 'https://github.com/kevinmcguinness/traintrack'
EMAIL = 'kevin.mcguinness@gmail.com'
AUTHOR = 'Kevin McGuinness'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

REQUIRED = [
    'zerorpc',
    'torch',
    'numpy',
    'Pillow',
    'Click',
    'slackclient',
    'loguru',
    'pyyaml'
]

ENTRY_POINTS = """
[console_scripts]
trackserver=trackserver:main
"""

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


PACKAGES = find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"])
print(PACKAGES)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=PACKAGES,
    py_modules=['trackserver'],
    install_requires=REQUIRED,
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    entry_points=ENTRY_POINTS
)
