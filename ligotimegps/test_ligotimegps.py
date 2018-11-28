# -*- coding: utf-8 -*-
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

from numbers import Integral

import pytest

from ligotimegps import LIGOTimeGPS


def almost_equal(a, b, places=7):
    if round(abs(a - b), places) == 0:
        return
    raise AssertionError('{} != {} within {} places'.format(a, b, places))


def test_creation():
    # test simple creations
    a = LIGOTimeGPS(1)
    assert isinstance(a, LIGOTimeGPS)
    assert a.seconds == 1
    assert a.gpsSeconds == 1
    assert a.nanoseconds == 0
    assert a.gpsNanoSeconds == 0

    a = LIGOTimeGPS(100, 200)
    assert a.gpsSeconds == 100
    assert a.gpsNanoSeconds == 200

    a = LIGOTimeGPS(1.002)
    assert a.gpsSeconds == 1
    assert a.gpsNanoSeconds == 2000000

    b = LIGOTimeGPS(a)
    assert a == b

    # test string creation
    a = LIGOTimeGPS("1.234")
    assert a.gpsSeconds == 1
    assert a.gpsNanoSeconds == 234000000

    a = LIGOTimeGPS("1", "234")
    assert a.gpsSeconds == 1
    assert a.gpsNanoSeconds == 234

    a = LIGOTimeGPS("1.2345678987654321e9")
    assert a.gpsSeconds == 1234567898
    assert a.gpsNanoSeconds == 765432100


@pytest.mark.parametrize('input_, errstr', [
    ('test', 'invalid literal for LIGOTimeGPS: test'),
    (None, 'cannot convert None (NoneType) to LIGOTimeGPS'),
])
def test_creation_errors(input_, errstr):
    with pytest.raises(TypeError) as err:
        LIGOTimeGPS(input_)
    assert str(err.value) == errstr


def test_str():
    assert str(LIGOTimeGPS(1)) == "1"
    assert str(LIGOTimeGPS(1, 1)) == "1.000000001"
    assert str(LIGOTimeGPS(100, 1)) == "100.000000001"
    assert str(LIGOTimeGPS(100, 100)) == "100.0000001"
    assert str(LIGOTimeGPS(-100, 100)) == "-99.9999999"
    assert str(LIGOTimeGPS(-1, 100)) == "-0.9999999"


def test_repr():
    assert repr(LIGOTimeGPS(1)) == "LIGOTimeGPS(1, 0)"


def test_float():
    f = float(LIGOTimeGPS(1))
    assert isinstance(f, float)
    assert f == 1.0


def test_int():
    i = int(LIGOTimeGPS(1, 100))
    assert isinstance(i, int)
    assert i == 1


def test_ns():
    n = LIGOTimeGPS(12345, 67890).ns()
    assert isinstance(n, Integral)
    assert n == 12345000067890



def test_eq_neq():
    assert LIGOTimeGPS(1) == LIGOTimeGPS(1)
    assert LIGOTimeGPS(1) != LIGOTimeGPS(2)
    assert (
        LIGOTimeGPS(123456789.123456789) ==
        LIGOTimeGPS(123456789.123456789))


def test_lt_gt():
    # less than
    assert LIGOTimeGPS(1) < LIGOTimeGPS(2)
    assert LIGOTimeGPS(1) < 2
    assert LIGOTimeGPS(1, 200) < LIGOTimeGPS(1, 300)

    # greater than
    assert LIGOTimeGPS(2) > LIGOTimeGPS(1)
    assert LIGOTimeGPS(2) > 1

    # less equal
    assert LIGOTimeGPS(1) <= LIGOTimeGPS(2)
    assert LIGOTimeGPS(1) <= 2
    assert 1 <= LIGOTimeGPS(2)
    assert LIGOTimeGPS(2) <= LIGOTimeGPS(2)

    # greater equal
    assert LIGOTimeGPS(2) >= LIGOTimeGPS(1)
    assert LIGOTimeGPS(2) >= 1
    assert 2 >= LIGOTimeGPS(1)
    assert LIGOTimeGPS(2) >= LIGOTimeGPS(2)


def test_hash():
    h = hash(LIGOTimeGPS(123, 456))
    assert isinstance(h, int)
    assert h == 435


def test_bool():
    assert bool(LIGOTimeGPS(0)) is False
    assert bool(LIGOTimeGPS(0, 1234)) is True
    assert bool(LIGOTimeGPS(1)) is True
    assert bool(LIGOTimeGPS(-1, 1234)) is True


def test_round():
    # test round (down) to int
    a = LIGOTimeGPS(12345, 67890)
    b = round(a)
    assert isinstance(b, LIGOTimeGPS)
    assert b == 12345

    # test round up
    assert round(LIGOTimeGPS(12345, 500000000)) == 12346

    # test round with decimal point
    b = round(a, 1)
    assert isinstance(b, LIGOTimeGPS)
    assert b == 12345.0
    assert round(a, 7) == LIGOTimeGPS(12345, 67900)


def test_add():
    a = LIGOTimeGPS(1) + LIGOTimeGPS(2)
    assert isinstance(a, LIGOTimeGPS)
    assert a == 3

    b = LIGOTimeGPS(1) + 2
    assert isinstance(b, LIGOTimeGPS)
    assert a == b

    c = 1 + LIGOTimeGPS(2)
    assert isinstance(c, LIGOTimeGPS)
    assert a == c

    a = 123.456 + LIGOTimeGPS(456, 999000000)
    assert a == 580.455


def test_sub():
    a = LIGOTimeGPS(2) - LIGOTimeGPS(1)
    assert isinstance(a, LIGOTimeGPS)
    assert a == 1

    b = LIGOTimeGPS(2) - 1
    assert isinstance(a, LIGOTimeGPS)
    assert a == 1

    c = 2 - LIGOTimeGPS(1)
    assert isinstance(c, LIGOTimeGPS)
    assert c == 1


def test_mul():
    a = LIGOTimeGPS(2) * LIGOTimeGPS(5)
    assert isinstance(a, LIGOTimeGPS)
    assert a == 10

    b = LIGOTimeGPS(2) * 5
    assert isinstance(b, LIGOTimeGPS)
    assert a == b

    c = 2 * LIGOTimeGPS(5)
    assert isinstance(c, LIGOTimeGPS)
    assert a == c

    d = LIGOTimeGPS(123, 456000000) * LIGOTimeGPS(234, 567000000)
    almost_equal(d, 28958.703552)
    assert LIGOTimeGPS(-123, 456789000) * 2 == -245.086422
    almost_equal(LIGOTimeGPS(123, -456000000) * 4, 490.176)


def test_div():
    a = LIGOTimeGPS(10) / LIGOTimeGPS(5)
    assert isinstance(a, LIGOTimeGPS)
    assert a == 2

    b = LIGOTimeGPS(10) / 5.
    assert isinstance(b, LIGOTimeGPS)
    assert a == b

    # check that we can't do int/LIGOTimeGPS
    with pytest.raises(TypeError):
        10 / LIGOTimeGPS(2)

    # check crazy numbers work (almost)
    d = LIGOTimeGPS(123, 456789012) / 3.14159265
    almost_equal(d, 39.2975165039)


def test_mod():
    assert LIGOTimeGPS(100.5) % 3 == 1.5


def test_pos():
    a = LIGOTimeGPS(1, 234)
    assert a == +a


def test_neg():
    a = LIGOTimeGPS(1, 234)
    assert -a == LIGOTimeGPS(-2, 999999766)


def test_abs():
    a = LIGOTimeGPS(123, 456789)
    assert abs(a) == a
    assert abs(-a) == a


def test_infinity():
    assert LIGOTimeGPS(1) < float('inf')
    assert LIGOTimeGPS(1) > -float('inf')
    assert LIGOTimeGPS(1) != float('inf')
    assert LIGOTimeGPS(1) != -float('inf')
