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

"""A pure-python version of the |lal.LIGOTimeGPS|_ object."""

from __future__ import annotations

from decimal import Decimal
from functools import total_ordering
from math import (
    isinf,
    log2,
    modf,
)
from typing import TYPE_CHECKING

from .protocol import LIGOTimeGPSLike

if TYPE_CHECKING:
    from typing import (
        Self,
        SupportsFloat,
    )

HALF_NANOSECOND = 0.5e-9
HALF_SECOND_IN_NANOSECONDS = 500000000


@total_ordering
class LIGOTimeGPS:
    """An object for storing times with nanosecond resolution.

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

    nanoseconds : `int`, `str`, optional
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

    @staticmethod
    def _from_float(seconds: SupportsFloat) -> tuple[int, float]:
        """Convert a float to (seconds_int, nanoseconds_float).

        Parameters
        ----------
        seconds : float
            The time in seconds as a float.

        Returns
        -------
        seconds_int : int
            The integer seconds part.
        nanoseconds_float : float
            The nanoseconds part as a float.
        """
        ns, sec = modf(seconds)
        return int(sec), ns * 1e9

    @staticmethod
    def _from_str_or_bytes(seconds: str | bytes) -> tuple[int, float]:
        """Convert a string or bytes to (seconds_int, nanoseconds_float).

        Parameters
        ----------
        seconds : str or bytes
            The time as a string or bytes object.

        Returns
        -------
        seconds_int : int
            The integer seconds part.
        nanoseconds_float : float
            The nanoseconds part as a float.

        Raises
        ------
        TypeError
            If the string cannot be parsed as a decimal number.
        """
        try:
            seconds_str = str(
                Decimal(
                    seconds.decode() if isinstance(seconds, bytes) else seconds,
                ),
            )
        except ArithmeticError as exc:
            msg = f"invalid literal for LIGOTimeGPS: {seconds!r}"
            raise TypeError(msg) from exc

        sign = -1 if seconds_str.startswith("-") else +1
        if "." in seconds_str:
            sec_str, ns_str = seconds_str.split(".")
            ns_val = sign * int(ns_str.ljust(9, "0")[:9])
        else:
            sec_str = seconds_str
            ns_val = 0

        return int(sec_str), float(ns_val)

    @staticmethod
    def _from_lal_ligotimegps(seconds: LIGOTimeGPSLike) -> tuple[int, float]:
        """Convert a `LIGOTimeGPS` object to (seconds_int, nanoseconds_float).

        Parameters
        ----------
        seconds : `LIGOTimeGPS`
            An object with gpsSeconds and gpsNanoSeconds attributes.

        Returns
        -------
        seconds_int : int
            The integer seconds part.
        nanoseconds_float : float
            The nanoseconds part as a float.
        """
        return (
            seconds.gpsSeconds,
            seconds.gpsNanoSeconds,
        )

    def __init__(
        self,
        seconds: LIGOTimeGPSLike | SupportsFloat | str | bytes = 0,
        nanoseconds: float = 0,
    ) -> None:
        """Create a LIGOTimeGPS instance."""
        nanoseconds_value = float(nanoseconds)

        seconds_int: int
        if isinstance(seconds, LIGOTimeGPSLike):
            sec_int, ns_float = self._from_lal_ligotimegps(seconds)
            seconds_int = sec_int
            nanoseconds_value += ns_float
        elif isinstance(seconds, int):
            seconds_int = seconds
        elif isinstance(seconds, float):
            sec_int, ns_float = self._from_float(seconds)
            seconds_int = sec_int
            nanoseconds_value += ns_float
        elif isinstance(seconds, (str, bytes)):
            sec_int, ns_float = self._from_str_or_bytes(seconds)
            seconds_int = sec_int
            nanoseconds_value += ns_float
        else:
            msg = (
                f"cannot convert {seconds!r} ({seconds.__class__.__name__})"
                f" to {type(self).__name__}"
            )
            raise TypeError(msg)
        self._seconds = seconds_int + int(nanoseconds_value // 1000000000)
        self._nanoseconds = int(nanoseconds_value % 1000000000)

    # define read-only properties to access each part
    gpsSeconds = property(  # noqa: N815
        fget=lambda self: self._seconds,
        doc="Seconds since 0h UTC 6 Jan 1980",
    )
    gpsNanoSeconds = property(  # noqa: N815
        fget=lambda self: self._nanoseconds,
        doc="residual nanoseconds",
    )

    # -- representations -------------

    def __repr__(self) -> str:
        """Return a representation of the `LIGOTimeGPS`."""
        return f"LIGOTimeGPS({self._seconds:d}, {self._nanoseconds:d})"

    def __str__(self) -> str:
        """Return an ASCII string representation of a `LIGOTimeGPS`."""
        if (self._seconds >= 0) or (self._nanoseconds == 0):
            s = f"{self._seconds:d}.{self._nanoseconds:09d}"
        elif self._seconds < -1:
            s = f"{self._seconds + 1:d}.{1000000000 - self._nanoseconds:09d}"
        else:
            s = f"-0.{1000000000 - self._nanoseconds:09d}"
        return s.rstrip("0").rstrip(".")

    def __float__(self) -> float:
        """Convert a `LIGOTimeGPS` to seconds as a float.

        Examples
        --------
        >>> float(LIGOTimeGPS(100.5))
        100.5
        """
        return self._seconds + self._nanoseconds * 1e-9

    def __int__(self) -> int:
        """Return the integer part (seconds) of a `LIGOTimeGPS` as an int.

        Examples
        --------
        >>> int(LIGOTimeGPS(100.5))
        100
        """
        return self._seconds

    def ns(self) -> int:
        """Convert a `LIGOTimeGPS` to a count of nanoseconds as an int.

        When running python2.7 on Windows this is returned as `numpy.long`
        to guarantee long-ness.

        Examples
        --------
        >>> LIGOTimeGPS(100.5).ns()
        100500000000
        """
        return self._seconds * 1000000000 + self._nanoseconds

    # -- comparison ------------------

    def __eq__(self, other: object) -> bool:
        """Test equality between `LIGOTimeGPS` objects."""
        try:
            if isinf(other):  # type: ignore[arg-type]
                return False
            if not isinstance(other, LIGOTimeGPS):
                other = LIGOTimeGPS(other)  # type: ignore[arg-type]
        except TypeError:
            return False
        return (
            self._seconds == other._seconds
            and self._nanoseconds == other._nanoseconds
        )

    def __ne__(self, other: object) -> bool:
        """Test inequality between `LIGOTimeGPS` objects."""
        return not (self == other)

    def __lt__(self, other: SupportsFloat) -> bool:
        """Test if this `LIGOTimeGPS` is less than another."""
        try:
            # +infinity
            if isinf(other) and other > 0:  # type: ignore[operator]
                return True
            # -infinity
            if isinf(other):
                return False
            if not isinstance(other, LIGOTimeGPS):
                other = LIGOTimeGPS(other)
        except TypeError:
            return NotImplemented
        return (
            self._seconds < other._seconds
            or (
                self._seconds == other._seconds
                and self._nanoseconds < other._nanoseconds
            )
        )

    def __hash__(self) -> int:
        """Return hash of the `LIGOTimeGPS`."""
        return self._seconds ^ self._nanoseconds

    def __bool__(self) -> bool:
        """Return True if the `LIGOTimeGPS` is nonzero.

        Examples
        --------
        >>> bool(LIGOTimeGPS(100.5))
        True
        """
        return bool(self._seconds or self._nanoseconds)

    # -- arithmetic ------------------

    def __round__(self, n: int = 0) -> Self:
        """Round a `LIGOTimeGPS` to the given precision."""
        n = int(n)
        if n == 0 and self.gpsNanoSeconds >= HALF_SECOND_IN_NANOSECONDS:
            return type(self)(self._seconds+1)
        if n == 0:
            return type(self)(self._seconds)
        return type(self)(self._seconds, round(self._nanoseconds, -9 + n))

    def __add__(self, other: LIGOTimeGPSLike | float | str | bytes) -> Self:
        """Add a value to a `LIGOTimeGPS`.

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
        return type(self)(
            self._seconds + other._seconds,
            self._nanoseconds + other._nanoseconds,
        )

    # addition is commutative.
    __radd__ = __add__

    def __sub__(self, other: LIGOTimeGPSLike | float | str | bytes) -> Self:
        """Subtract a value from a `LIGOTimeGPS`.

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
        return type(self)(
            self._seconds - other._seconds,
            self._nanoseconds - other._nanoseconds,
        )

    def __rsub__(self, other: LIGOTimeGPSLike | float | str | bytes) -> Self:
        """Subtract a `LIGOTimeGPS` from a value."""
        if not isinstance(other, LIGOTimeGPS):
            other = LIGOTimeGPS(other)
        return type(self)(
            other._seconds - self._seconds,
            other._nanoseconds - self._nanoseconds,
        )

    def __mul__(self, other: float) -> Self:
        """Multiply a `LIGOTimeGPS` by a number.

        Examples
        --------
        >>> LIGOTimeGPS(100.5) * 2
        LIGOTimeGPS(201, 0)
        """
        seconds = self._seconds
        nanoseconds_float = float(self._nanoseconds)

        if seconds < 0 and self._nanoseconds > 0:
            seconds += 1
            nanoseconds_float -= 1000000000

        slo = seconds % 131072
        shi = seconds - slo
        olo = other % 2**(int(log2(other)) - 26) if other else 0
        ohi = other - olo

        nanoseconds_float *= float(other)
        seconds_float = 0.0
        for addend in (slo * olo, shi * olo, slo * ohi, shi * ohi):
            n, s = modf(addend)
            seconds_float += s
            nanoseconds_float += n * 1e9

        return type(self)(seconds_float, round(nanoseconds_float))

    # multiplication is commutative
    __rmul__ = __mul__

    def __truediv__(self, other: float) -> Self:
        """Divide a `LIGOTimeGPS` by a number.

        Examples
        --------
        >>> LIGOTimeGPS(100.5) / 2
        LIGOTimeGPS(50, 250000000)
        """
        quotient = type(self)(float(self) / float(other))
        for _ in range(100):
            residual = float(self - quotient * other) / float(other)
            quotient += residual
            if abs(residual) <= HALF_NANOSECOND:
                break
        return quotient

    __div__ = __truediv__

    def __mod__(self, other: float) -> Self:
        """Compute the remainder when a `LIGOTimeGPS` is divided by a number.

        Examples
        --------
        >>> LIGOTimeGPS(100.5) % 3
        LIGOTimeGPS(1, 500000000)
        """
        quotient = int(self / other)
        return self - quotient * other

    # -- unary arithmetic ------------

    def __pos__(self) -> Self:
        """Return the positive value of the `LIGOTimeGPS`."""
        return self

    def __neg__(self) -> Self:
        """Return the negation of the `LIGOTimeGPS`."""
        return type(self)(0, -self.ns())

    def __abs__(self) -> Self:
        """Return the absolute value of the `LIGOTimeGPS`."""
        if self._seconds >= 0:
            return self
        return -self
