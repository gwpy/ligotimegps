# Copyright (c) 2017-2025 Cardiff University
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

"""Tests for `ligotimegps.LIGOTimeGPS`."""

from numbers import Integral

import pytest

from .. import LIGOTimeGPS


@pytest.mark.parametrize(("value", "sec", "nanosec"), [
    # empty constructor
    pytest.param((), 0, 0, id="empty"),
    # simple integer
    pytest.param((1,), 1, 0, id="int"),
    # (sec, nanosec) tuple of integers
    pytest.param((100, 200), 100, 200, id="int-tuple"),
    # simple float
    pytest.param((1.002,), 1, 2000000, id="float"),
    # string
    pytest.param(("1.234",), 1, 234000000, id="str"),
    # tuple of strings
    pytest.param(("1", "234"), 1, 234, id="str-tuple"),
    # high-precision string
    pytest.param(
        ("1.2345678987654321e9",),
        1234567898,
        765432100,
        id="high-precision-str",
    ),
    # overly precise string (rounded)
    pytest.param(
        ("1.2345678987654321987654321e9",),
        1234567898,
        765432198,
        id="overly-precise-str",
    ),
])
def test_creation(value, sec, nanosec):
    """Test `LIGOTimeGPS` creation."""
    gps = LIGOTimeGPS(*value)
    assert gps.gpsSeconds == sec
    assert gps.gpsNanoSeconds == nanosec


def test_copy():
    """Test that we can copy a `LIGOTimeGPS` to a new object."""
    a = LIGOTimeGPS(1)
    b = LIGOTimeGPS(a)
    assert b == a
    assert b is not a


@pytest.mark.parametrize(("input_", "errstr"), [
    pytest.param(
        "test",
        r"invalid literal for LIGOTimeGPS: 'test'",
        id="string",
    ),
    pytest.param(
        None,
        r"cannot convert None \(NoneType\) to LIGOTimeGPS",
        id="None",
    ),
])
def test_creation_errors(input_, errstr):
    """Test `LIGOTimeGPS` creation errors."""
    with pytest.raises(TypeError, match=errstr):
        LIGOTimeGPS(input_)


@pytest.mark.parametrize(("value", "strrep"), [
    (LIGOTimeGPS(1), "1"),
    (LIGOTimeGPS(1, 1), "1.000000001"),
    (LIGOTimeGPS(100, 1), "100.000000001"),
    (LIGOTimeGPS(100, 100), "100.0000001"),
    (LIGOTimeGPS(-100, 100), "-99.9999999"),
    (LIGOTimeGPS(-1, 100), "-0.9999999"),

])
def test_str(value, strrep):
    """Test ``str(x)``."""
    assert str(value) == strrep


def test_repr():
    """Test ``repr(x)``."""
    assert repr(LIGOTimeGPS(1)) == "LIGOTimeGPS(1, 0)"


def test_float():
    """Test ``float(x)``."""
    f = float(LIGOTimeGPS(1))
    assert isinstance(f, float)
    assert f == 1.0


def test_int():
    """Test ``int(x)``."""
    i = int(LIGOTimeGPS(1, 100))
    assert isinstance(i, int)
    assert i == 1


def test_ns():
    """Test ``LIGOTimeGPS.ns()``."""
    n = LIGOTimeGPS(12345, 67890).ns()
    assert isinstance(n, Integral)
    assert n == 12345000067890


@pytest.mark.parametrize(("a", "b"), [
    (LIGOTimeGPS(1), LIGOTimeGPS(1)),
    (LIGOTimeGPS(1), 1),
    (1, LIGOTimeGPS(1)),
    (LIGOTimeGPS(123456789.123456789), 123456789.123456789),
])
def test_eq(a, b):
    """Test 'equal to'."""
    assert a == b


@pytest.mark.parametrize(("a", "b"), [
    (LIGOTimeGPS(1), LIGOTimeGPS(2)),
    (LIGOTimeGPS(1), 2),
    (1, LIGOTimeGPS(2)),
    (LIGOTimeGPS(1), "test"),
])
def test_neq(a, b):
    """Test 'not equal to'."""
    assert a != b


@pytest.mark.parametrize(("a", "b"), [
    (LIGOTimeGPS(1), LIGOTimeGPS(2)),
    (LIGOTimeGPS(1), 2),
    (1, LIGOTimeGPS(2)),
    (LIGOTimeGPS(1, 200), LIGOTimeGPS(1, 300)),
])
def test_lt(a, b):
    """Test 'less than'."""
    assert a < b


def test_lt_notimplemented():
    """Test that 'less than' with something odd raises `TypeError`."""
    with pytest.raises(
        TypeError,
        match="'<' not supported between instances of 'LIGOTimeGPS' and",
    ):
        assert LIGOTimeGPS(1) < "test"


@pytest.mark.parametrize(("a", "b"), [
    (LIGOTimeGPS(2), LIGOTimeGPS(1)),
    (LIGOTimeGPS(2), 1),
    (2, LIGOTimeGPS(1)),
])
def test_gt(a, b):
    """Test 'greater than'."""
    assert a > b


@pytest.mark.parametrize(("a", "b"), [
    (LIGOTimeGPS(1), LIGOTimeGPS(2)),
    (LIGOTimeGPS(1), 2),
    (1, LIGOTimeGPS(2)),
    (LIGOTimeGPS(2), LIGOTimeGPS(2)),
])
def test_le(a, b):
    """Test 'less than or equal to'."""
    assert a <= b


@pytest.mark.parametrize(("a", "b"), [
    (LIGOTimeGPS(2), LIGOTimeGPS(1)),
    (LIGOTimeGPS(2), 1),
    (2, LIGOTimeGPS(1)),
    (LIGOTimeGPS(2), LIGOTimeGPS(2)),
])
def test_ge(a, b):
    """Test 'greater than or equal to'."""
    assert a >= b


def test_hash():
    """Test ``hash(x)``."""
    h = hash(LIGOTimeGPS(123, 456))
    assert isinstance(h, int)
    assert h == 435


@pytest.mark.parametrize(("value", "truth"), [
    (LIGOTimeGPS(0), False),
    (LIGOTimeGPS(0, 1234), True),
    (LIGOTimeGPS(1), True),
    (LIGOTimeGPS(-1, 1234), True),
])
def test_bool(value, truth):
    """Test ``bool(x)``."""
    assert bool(value) is truth


def test_round():
    """Test ``round(x)``."""
    a = LIGOTimeGPS(12345, 67890)
    b = round(a)
    assert isinstance(b, LIGOTimeGPS)
    assert b == 12345


def test_round_up():
    """Test ``round(x)`` rounding up."""
    assert round(LIGOTimeGPS(12345, 500000000)) == 12346


def test_round_precision():
    """Test ``round(x, n)`` with precision."""
    a = LIGOTimeGPS(12345, 67890)
    b = round(a, 1)
    assert isinstance(b, LIGOTimeGPS)
    assert b == 12345.0
    assert round(a, 7) == LIGOTimeGPS(12345, 67900)


@pytest.mark.parametrize(("a", "b", "result"), [
    (LIGOTimeGPS(1), LIGOTimeGPS(2), 3),
    (LIGOTimeGPS(1), 2, 3),
    (1, LIGOTimeGPS(2), 3),
    (123.456, LIGOTimeGPS(456, 999000000), 580.455),
])
def test_add(a, b, result):
    """Test addition."""
    sum_ = a + b
    assert isinstance(sum_, LIGOTimeGPS)
    assert sum_ == result


@pytest.mark.parametrize(("a", "b", "result"), [
    (LIGOTimeGPS(2), LIGOTimeGPS(1), 1),
    (LIGOTimeGPS(2), 1, 1),
    (2, LIGOTimeGPS(1), 1),
])
def test_sub(a, b, result):
    """Test subtraction."""
    diff = a - b
    assert isinstance(diff, LIGOTimeGPS)
    assert diff == result


@pytest.mark.parametrize(("a", "b", "result"), [
    (LIGOTimeGPS(2), LIGOTimeGPS(5), 10),
    (LIGOTimeGPS(2), 5, 10),
    (2, LIGOTimeGPS(5), 10),
    (LIGOTimeGPS(123, 456000000), LIGOTimeGPS(234, 567000000), 28958.703552),
    (LIGOTimeGPS(-123, 456789000), 2, -245.086422),
])
def test_mul(a, b, result):
    """Test multiplication."""
    prod = a * b
    assert isinstance(prod, LIGOTimeGPS)
    assert float(prod) == pytest.approx(result)


@pytest.mark.parametrize(("a", "b", "result"), [
    (LIGOTimeGPS(10), LIGOTimeGPS(5), 2),
    (LIGOTimeGPS(10), 5, 2),
    (LIGOTimeGPS(123, 456789012), 3.14159265, 39.2975165039),
])
def test_div(a, b, result):
    """Test division."""
    quot = a / b
    assert isinstance(quot, LIGOTimeGPS)
    assert quot == result


def test_div_error():
    """Test that we can't do ``int / LIGOTimeGPS``."""
    # check that we can't do int/LIGOTimeGPS
    with pytest.raises(TypeError):
        10 / LIGOTimeGPS(2)


def test_mod():
    """Test modulo operation."""
    assert LIGOTimeGPS(100.5) % 3 == 1.5


def test_pos():
    """Test unary plus."""
    a = LIGOTimeGPS(1, 234)
    assert a == +a


def test_neg():
    """Test unary minus."""
    a = LIGOTimeGPS(1, 234)
    assert -a == LIGOTimeGPS(-2, 999999766)


def test_abs():
    """Test abs(x)."""
    a = LIGOTimeGPS(123, 456789)
    assert abs(a) == a
    assert abs(-a) == a


def test_infinity():
    """Test comparisons with infinity."""
    assert LIGOTimeGPS(1) < float("inf")
    assert LIGOTimeGPS(1) > -float("inf")
    assert LIGOTimeGPS(1) != float("inf")
    assert LIGOTimeGPS(1) != -float("inf")


def test_lal():
    """Test compatibility with `lal.LIGOTimeGPS`."""
    lal = pytest.importorskip("lal")
    a = LIGOTimeGPS(123, 456789012)
    b = lal.LIGOTimeGPS(a.gpsSeconds, a.gpsNanoSeconds)
    assert a == b
    c = LIGOTimeGPS(b)
    assert a == c
    assert b == c
