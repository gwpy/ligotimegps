# Copyright (c) 2010-2016 Kipp Cannon
#               2017-2025 Cardiff University
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

"""A pure-python version of the |lal.LIGOTimeGPS|_ object.

`~ligotimegps.LIGOTimeGPS` is used to represent GPS times
(number of seconds elapsed since the GPS epoch) with nanosecond precision.

The code provided here is much slower than the C-implementation provided
by LAL, so if you really care about performance, don't use this module.
"""

from .ligotimegps import LIGOTimeGPS
from .protocol import LIGOTimeGPSLike

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # pragma: no cover
    __version__ = ""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"
