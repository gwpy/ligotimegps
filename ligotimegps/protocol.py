# Copyright (c) 2025 Cardiff University
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

"""Generic protocol defining what any `LIGOTimeGPS` should look like."""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class LIGOTimeGPSLike(Protocol):
    """Protocol for LIGOTimeGPS-like objects.

    This protocol defines the interface that any LIGOTimeGPS-like object
    should implement, allowing for structural subtyping across different
    implementations.
    """

    gpsSeconds: int  # noqa: N815
    gpsNanoSeconds: int  # noqa: N815
