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


def assert_almost_equal(a, b, places=7):
    if round(abs(a - b), places) == 0:
        return
    raise AssertionError('{} != {} within {} places'.format(a, b, places))


@pytest.mark.parametrize(("value", "sec", "nanosec"), (
    # simple integer
    (1, 1, 0),
    # (sec, nanosec) tuple of integers
    ((100, 200), 100, 200),
    # simple float
    (1.002, 1, 2000000),
    # string
    ("1.234", 1, 234000000),
    # tuple of strings
    (("1", "234"), 1, 234),
    # high-precision string
    ("1.2345678987654321e9", 1234567898, 765432100),
))
def test_creation(value, sec, nanosec):
    """Test LIGOTimeGPS creation
    """
    if not isinstance(value, tuple):
        value = (value,)
    gps = LIGOTimeGPS(*value)

    assert gps.seconds == sec
    assert gps.gpsSeconds == sec
    assert gps.nanoseconds == nanosec
    assert gps.gpsNanoSeconds == nanosec


def test_copy():
    """Test that we can copy a LIGOTimeGPS to a new object
    """
    a = LIGOTimeGPS(1)
    b = LIGOTimeGPS(a)
    assert b == a
    assert b is not a


@pytest.mark.parametrize('input_, errstr', [
    ('test', 'invalid literal for LIGOTimeGPS: test'),
    (None, 'cannot convert None (NoneType) to LIGOTimeGPS'),
])
def test_creation_errors(input_, errstr):
    with pytest.raises(TypeError) as err:
        LIGOTimeGPS(input_)
    assert str(err.value) == errstr


@pytest.mark.parametrize(("value", "strrep"), (
    (LIGOTimeGPS(1), "1"),
    (LIGOTimeGPS(1, 1), "1.000000001"),
    (LIGOTimeGPS(100, 1), "100.000000001"),
    (LIGOTimeGPS(100, 100), "100.0000001"),
    (LIGOTimeGPS(-100, 100), "-99.9999999"),
    (LIGOTimeGPS(-1, 100), "-0.9999999"),

))
def test_str(value, strrep):
    assert str(value) == strrep


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


@pytest.mark.parametrize(("a", "b"), (
    (LIGOTimeGPS(1), LIGOTimeGPS(1)),
    (LIGOTimeGPS(1), 1),
    (1, LIGOTimeGPS(1)),
    (LIGOTimeGPS(123456789.123456789), 123456789.123456789),
))
def test_eq(a, b):
    """Test 'equal to'
    """
    assert a == b


@pytest.mark.parametrize(("a", "b"), (
    (LIGOTimeGPS(1), LIGOTimeGPS(2)),
))
def test_neq(a, b):
    """Test 'not equal to'
    """
    assert a != b


@pytest.mark.parametrize(("a", "b"), (
    (LIGOTimeGPS(1), LIGOTimeGPS(2)),
    (LIGOTimeGPS(1), 2),
    (1, LIGOTimeGPS(2)),
    (LIGOTimeGPS(1, 200), LIGOTimeGPS(1, 300)),
))
def test_lt(a, b):
    """Test 'less than'
    """
    assert a < b


@pytest.mark.parametrize(("a", "b"), (
    (LIGOTimeGPS(2), LIGOTimeGPS(1)),
    (LIGOTimeGPS(2), 1),
    (2, LIGOTimeGPS(1)),
))
def test_gt(a, b):
    """Test 'greater than'
    """
    assert a > b


@pytest.mark.parametrize(("a", "b"), (
    (LIGOTimeGPS(1), LIGOTimeGPS(2)),
    (LIGOTimeGPS(1), 2),
    (1, LIGOTimeGPS(2)),
    (LIGOTimeGPS(2), LIGOTimeGPS(2)),
))
def test_le(a, b):
    """Test 'less than or equal to'
    """
    assert a <= b


@pytest.mark.parametrize(("a", "b"), (
    (LIGOTimeGPS(2), LIGOTimeGPS(1)),
    (LIGOTimeGPS(2), 1),
    (2, LIGOTimeGPS(1)),
    (LIGOTimeGPS(2), LIGOTimeGPS(2)),
))
def test_ge(a, b):
    """Test 'greater than or equal to'
    """
    assert a >= b


def test_hash():
    h = hash(LIGOTimeGPS(123, 456))
    assert isinstance(h, int)
    assert h == 435


@pytest.mark.parametrize(("value", "truth"), (
    (LIGOTimeGPS(0), False),
    (LIGOTimeGPS(0, 1234), True),
    (LIGOTimeGPS(1), True),
    (LIGOTimeGPS(-1, 1234), True),
))
def test_bool(value, truth):
    """Test bool(x)
    """
    assert bool(value) is truth


def test_round():
    a = LIGOTimeGPS(12345, 67890)
    b = round(a)
    assert isinstance(b, LIGOTimeGPS)
    assert b == 12345


def test_round_up():
    assert round(LIGOTimeGPS(12345, 500000000)) == 12346


def test_round_precision():
    a = LIGOTimeGPS(12345, 67890)
    b = round(a, 1)
    assert isinstance(b, LIGOTimeGPS)
    assert b == 12345.0
    assert round(a, 7) == LIGOTimeGPS(12345, 67900)


@pytest.mark.parametrize(("a", "b", "result"), (
    (LIGOTimeGPS(1), LIGOTimeGPS(2), 3),
    (LIGOTimeGPS(1), 2, 3),
    (1, LIGOTimeGPS(2), 3),
    (123.456, LIGOTimeGPS(456, 999000000), 580.455),
))
def test_add(a, b, result):
    sum_ = a + b
    assert isinstance(sum_, LIGOTimeGPS)
    assert sum_ == result


@pytest.mark.parametrize(("a", "b", "result"), (
    (LIGOTimeGPS(2), LIGOTimeGPS(1), 1),
    (LIGOTimeGPS(2), 1, 1),
    (2, LIGOTimeGPS(1), 1),
))
def test_sub(a, b, result):
    diff = a - b
    assert isinstance(diff, LIGOTimeGPS)
    assert diff == result


@pytest.mark.parametrize(("a", "b", "result"), (
    (LIGOTimeGPS(2), LIGOTimeGPS(5), 10),
    (LIGOTimeGPS(2), 5, 10),
    (2, LIGOTimeGPS(5), 10),
    (LIGOTimeGPS(123, 456000000), LIGOTimeGPS(234, 567000000), 28958.703552),
    (LIGOTimeGPS(-123, 456789000), 2, -245.086422),
))
def test_mul(a, b, result):
    prod = a * b
    assert isinstance(prod, LIGOTimeGPS)
    assert_almost_equal(prod, result)


@pytest.mark.parametrize(("a", "b", "result"), (
    (LIGOTimeGPS(10), LIGOTimeGPS(5), 2),
    (LIGOTimeGPS(10), 5, 2),
    (LIGOTimeGPS(123, 456789012), 3.14159265, 39.2975165039),
))
def test_div(a, b, result):
    quot = a / b
    assert isinstance(quot, LIGOTimeGPS)
    assert quot == result


def test_div_error():
    # check that we can't do int/LIGOTimeGPS
    with pytest.raises(TypeError):
        10 / LIGOTimeGPS(2)


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
