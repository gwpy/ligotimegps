#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2017)
#
# This file is part of ligotimegps.
#
# ligotimegps is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ligotimegps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ligotimegps.  If not, see <http://www.gnu.org/licenses/>.

"""Setup the ligotimegps package
"""

import os.path
import sys

from setuptools import (setup, Extension)

from Cython.Build import cythonize

import versioneer

__version__ = versioneer.get_version()

# setup dependencies
setup_requires = [
    'setuptools',
    'Cython',
]
if set(('pytest', 'test', 'prt')).intersection(sys.argv):
    setup_requires.append('pytest_runner')

# runtime dependencies
install_requires = [
    'six',
    'Cython',
]

# test dependencies
tests_require = ['pytest>=2.8']

# read long description
with open('README.md', 'rb') as f:
    longdesc = f.read().decode().strip()

# build extensions
extensions = [
    Extension('ligotimegps._ligotimegps',
              sources=[os.path.join('ligotimegps', '_ligotimegps.pyx')])
]

# run setup
setup(name='ligotimegps',
      version=__version__,
      packages=['ligotimegps'],
      description="A pure-python version of lal.LIGOTimeGPS",
      long_description=longdesc,
      long_description_content_type='text/markdown',
      author='Duncan Macleod',
      author_email='duncan.macleod@ligo.org',
      keywords="gravitational-waves ligo lal",
      url="https://github.com/gwpy/ligotimegps",
      license='GPLv3',
      cmdclass=versioneer.get_cmdclass(),
      setup_requires=setup_requires,
      install_requires=install_requires,
      tests_require=tests_require,
      ext_modules=cythonize(extensions),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
)
