#!/usr/bin/env python

import os
import sys

from distutils.core import setup

__version__ = "0.1"
__author__ = "Matthew Dietz"

setup(name='retropie_sync',
      version=__version__,
      description='RetroPie ROM syncer',
      author=__author__,
      author_email='matthew.dietz@gmail.com',
      url='',
      license='',
      install_requires=[],
      package_dir={},
      packages=[
      ],
      scripts=[
      ],
      entry_points={
        "console_scripts": ["retropiesync = retropie_sync.cli:main"]})
