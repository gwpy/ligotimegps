# -*- coding: utf-8 -*-
# Copyright Kipp Cannon 2010-2016
# Copyright Duncan Macleod 2017
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

from math import (modf, log)
from functools import wraps
from decimal import Decimal

try:
    from functools import total_ordering
except ImportError:  # python 2.6
    from total_ordering import total_ordering

import six

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['LIGOTimeGPS']


@total_ordering
class LIGOTimeGPS(object):
    """An object for storing times with nanosecond resolution

    Internally the time is represented as a signed integer `gpsSeconds` part
    and an unsigned integer `gpsNanoseconds` part.
    The actual time is always constructed by adding the nanoseconds to the
    seconds.
    So -0.5 s is represented by setting seconds = -1, and nanoseconds to
    500000000.

    Parameters
    ----------
    seconds : `int`, `str`
        the count of seconds
    nanoseconds: `int`, `str`, optional
        the count of nanoseconds

    Examples
    --------
    >>> LIGOTimeGPS(100.5)
    LIGOTimeGPS(100, 500000000)
    >>> LIGOTimeGPS("100.5")
    LIGOTimeGPS(100, 500000000)
    >>> LIGOTimeGPS(100, 500000000)
    LIGOTimeGPS(100, 500000000)
    >>> LIGOTimeGPS(0, 100500000000)
    LIGOTimeGPS(100, 500000000)
    >>> LIGOTimeGPS(100.2, 300000000)
    LIGOTimeGPS(100, 500000000)
    >>> LIGOTimeGPS("0.000000001")
    LIGOTimeGPS(0, 1)
    >>> LIGOTimeGPS("0.0000000012")
    LIGOTimeGPS(0, 1)
    >>> LIGOTimeGPS("0.0000000018")
    LIGOTimeGPS(0, 2)
    >>> LIGOTimeGPS("-0.8")
    LIGOTimeGPS(-1, 200000000)
    >>> LIGOTimeGPS("-1.2")
    LIGOTimeGPS(-2, 800000000)
    """
    def __init__(self, seconds, nanoseconds=0):
        """Create a LIGOTimeGPS instance
        """
        if not isinstance(nanoseconds, (float, int)):
            nanoseconds = float(nanoseconds)
        if isinstance(seconds, float):
            ns, seconds = modf(seconds)
            seconds = int(seconds)
            nanoseconds += ns * 1e9
        elif not isinstance(seconds, six.integer_types):
            if isinstance(seconds, (six.binary_type, six.text_type)):
                try:
                    seconds = str(Decimal(seconds))
                except ArithmeticError:
                    raise TypeError("invalid literal for LIGOTimeGPS(): %s"
                                    % seconds)
                sign = -1 if seconds.startswith("-") else +1
                if "." in seconds:
                    seconds, ns = seconds.split(".")
                    ns = sign * int(ns.ljust(9, '0'))
                else:
                    ns = 0
                seconds = int(seconds)
                nanoseconds += ns
            elif (hasattr(seconds, "gpsSeconds") and
                  hasattr(seconds, "gpsNanoSeconds")):  # lal.LIGOTimeGPS
                nanoseconds += seconds.gpsNanoSeconds
                seconds = seconds.gpsSeconds
            else:
                raise TypeError(seconds)
        self._seconds = seconds + int(nanoseconds // 1000000000)
        self._nanoseconds = int(nanoseconds % 1000000000)

    # define read-only properties to access each part
    seconds = gpsSeconds = property(lambda self: self._seconds)
    nanoseconds = gpsNanoSeconds = property(lambda self: self._nanoseconds)

    # -- representations ------------------------

    def __repr__(self):
        return "LIGOTimeGPS(%d, %u)" % (self._seconds, self._nanoseconds)

    def __str__(self):
        """Return an ASCII string representation of a `LIGOTimeGPS`
        """
        if (self._seconds >= 0) or (self._nanoseconds == 0):
            s = "%d.%09u" % (self._seconds, self._nanoseconds)
        elif self._seconds < -1:
            s = "%d.%09u" % (self._seconds + 1, 1000000000 - self._nanoseconds)
        else:
            s = "-0.%09u" % (1000000000 - self._nanoseconds)
        return s.rstrip("0").rstrip(".")

    def __float__(self):
        """Convert a `LIGOTimeGPS` to seconds as a float

        Examples
        --------
        >>> float(LIGOTimeGPS(100.5))
        100.5
        """
        return self._seconds + self._nanoseconds * 1e-9

    def __int__(self):
        """Return the integer part (seconds) of a `LIGOTimeGPS` as an int

        Examples
        --------
        >>> int(LIGOTimeGPS(100.5))
        100
        """
        return self._seconds

    if six.PY2:
        def __long__(self):
            """Return the integer part (seconds) of a `LIGOTimeGPS` as a long

            >>> long(LIGOTimeGPS(100.5))
            100L
            """
            return long(self._seconds)

    def ns(self):
        """Convert a `LIGOTimeGPS` to a count of nanoseconds as an int

        Examples
        --------
        >>> LIGOTimeGPS(100.5).ns()
        100500000000
        """
        return self._seconds * 1000000000 + self._nanoseconds

    # -- comparison -----------------------------

    def __eq__(self, other):
        if not isinstance(other, LIGOTimeGPS):
            other = LIGOTimeGPS(other)
        return (self._seconds == other._seconds and
                self._nanoseconds == other._nanoseconds)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if not isinstance(other, LIGOTimeGPS):
            other = LIGOTimeGPS(other)
        if self._seconds < other._seconds:
            return True
        elif (self._seconds == other._seconds and
              self._nanoseconds < other._nanoseconds):
            return True
        return False

    def __hash__(self):
        return self._seconds ^ self._nanoseconds

    def __nonzero__(self):
        """Return True if the `LIGOTimeGPS` is nonzero

        Examples
        --------
        >>> bool(LIGOTimeGPS(100.5))
        True
        """
        return self._seconds or self._nanoseconds

    # -- arithmetic -----------------------------

    def __round__(self, n=0):
        if n == 0 and self.nanoseconds >= 5e8:
            return type(self)(self._seconds+1)
        elif n == 0:
            return type(self)(self._seconds)
        else:
            return type(self)(self._seconds, round(self._nanoseconds, -9 + n))

    def __add__(self, other):
        """Add a value to a `LIGOTimeGPS`

        If the value being added to the `LIGOTimeGPS` is not also a
        `LIGOTimeGPS`, then an attempt is made to convert it to `LIGOTimeGPS`.

        Examples
        --------
        >>> LIGOTimeGPS(100.5) + LIGOTimeGPS(3)
        LIGOTimeGPS(103, 500000000)
        >>> LIGOTimeGPS(100.5) + 3
        LIGOTimeGPS(103, 500000000)
        >>> LIGOTimeGPS(100.5) + "3"
        LIGOTimeGPS(103, 500000000)
        """
        if not isinstance(other, LIGOTimeGPS):
            other = LIGOTimeGPS(other)
        return LIGOTimeGPS(self._seconds + other._seconds,
                           self._nanoseconds + other._nanoseconds)

    # addition is commutative.
    __radd__ = __add__

    def __sub__(self, other):
        """Subtract a value from a `LIGOTimeGPS`

        If the value being subtracted from the `LIGOTimeGPS` is not also
        a `LIGOTimeGPS`, then an attempt is made to convert it to a
        `LIGOTimeGPS`.

        Examples
        --------
        >>> LIGOTimeGPS(100.5) - LIGOTimeGPS(3)
        LIGOTimeGPS(97, 500000000)
        >>> LIGOTimeGPS(100.5) - 3
        LIGOTimeGPS(97, 500000000)
        >>> LIGOTimeGPS(100.5) - "3"
        LIGOTimeGPS(97, 500000000)
        """
        if not isinstance(other, LIGOTimeGPS):
            other = LIGOTimeGPS(other)
        return LIGOTimeGPS(self._seconds - other._seconds,
                           self._nanoseconds - other._nanoseconds)

    def __rsub__(self, other):
        """Subtract a `LIGOTimeGPS` from a value
        """
        if not isinstance(other, LIGOTimeGPS):
            other = LIGOTimeGPS(other)
        return LIGOTimeGPS(other._seconds - self._seconds,
                           other._nanoseconds - self._nanoseconds)

    def __mul__(self, other):
        """Multiply a `LIGOTimeGPS` by a number

        Examples
        --------
        >>> LIGOTimeGPS(100.5) * 2
        LIGOTimeGPS(201, 0)
        """
        seconds = self._seconds
        nanoseconds = self._nanoseconds

        if seconds < 0 and nanoseconds > 0:
            seconds += 1
            nanoseconds -= 1000000000

        slo = seconds % 131072
        shi = seconds - slo
        olo = other % 2**(int(log(other, 2)) - 26) if other else 0
        ohi = other - olo

        nanoseconds *= float(other)
        seconds = 0.
        for addend in (slo * olo, shi * olo, slo * ohi, shi * ohi):
            n, s = modf(addend)
            seconds += s
            nanoseconds += n * 1e9

        return LIGOTimeGPS(seconds, round(nanoseconds))

    # multiplication is commutative
    __rmul__ = __mul__

    def __truediv__(self, other):
        """Divide a `LIGOTimeGPS` by a number

        Examples
        --------
        >>> LIGOTimeGPS(100.5) / 2
        LIGOTimeGPS(50, 250000000)
        """
        quotient = LIGOTimeGPS(float(self) / float(other))
        for n in range(100):
            residual = float(self - quotient * other) / float(other)
            quotient += residual
            if abs(residual) <= 0.5e-9:
                break
        return quotient

    __div__ = __truediv__

    def __mod__(self, other):
        """Compute the remainder when a `LIGOTimeGPS` is divided by a number

        Examples
        --------
        >>> LIGOTimeGPS(100.5) % 3
        LIGOTimeGPS(1, 500000000)
        """
        quotient = int(self / other)
        return self - quotient * other

    # -- unary arithmetic -----------------------

    def __pos__(self):
        return self

    def __neg__(self):
        return LIGOTimeGPS(0, -self.ns())

    def __abs__(self):
        if self._seconds >= 0:
            return self
        return -self
