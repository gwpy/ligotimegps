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

import sys

if sys.version < '2.7':
    import unittest2 as unittest
else:
    import unittest

from six import PY2

from ligotimegps import LIGOTimeGPS


class LIGOTimeGPSTests(unittest.TestCase):
    def test_creation(self):
        # test simple creations
        a = LIGOTimeGPS(1)
        self.assertIsInstance(a, LIGOTimeGPS)
        self.assertEqual(a.seconds, 1)
        self.assertEqual(a.gpsSeconds, 1)
        self.assertEqual(a.nanoseconds, 0)
        self.assertEqual(a.gpsNanoSeconds, 0)
        a = LIGOTimeGPS(100, 200)
        self.assertEqual(a.gpsSeconds, 100)
        self.assertEqual(a.gpsNanoSeconds, 200)
        a = LIGOTimeGPS(1.002)
        self.assertEqual(a.gpsSeconds, 1)
        self.assertEqual(a.gpsNanoSeconds, 2000000)
        b = LIGOTimeGPS(a)
        self.assertEqual(a, b)
        # test string creation
        a = LIGOTimeGPS("1.234")
        self.assertEqual(a.gpsSeconds, 1)
        self.assertEqual(a.gpsNanoSeconds, 234000000)
        a = LIGOTimeGPS("1", "234")
        self.assertEqual(a.gpsSeconds, 1)
        self.assertEqual(a.gpsNanoSeconds, 234)
        a = LIGOTimeGPS("1.2345678987654321e9")
        self.assertEqual(a.gpsSeconds, 1234567898)
        self.assertEqual(a.gpsNanoSeconds, 765432100)
        # check errors
        self.assertRaises(TypeError, LIGOTimeGPS, 'test')
        self.assertRaises(TypeError, LIGOTimeGPS, None)

    def test_str(self):
        self.assertEqual(str(LIGOTimeGPS(1)), "1")
        self.assertEqual(str(LIGOTimeGPS(1, 1)), "1.000000001")
        self.assertEqual(str(LIGOTimeGPS(100, 1)), "100.000000001")
        self.assertEqual(str(LIGOTimeGPS(100, 100)), "100.0000001")
        self.assertEqual(str(LIGOTimeGPS(-100, 100)), "-99.9999999")
        self.assertEqual(str(LIGOTimeGPS(-1, 100)), "-0.9999999")

    def test_repr(self):
        self.assertEqual(repr(LIGOTimeGPS(1)), "LIGOTimeGPS(1, 0)")

    def test_float(self):
        f = float(LIGOTimeGPS(1))
        self.assertIsInstance(f, float)
        self.assertEqual(f, 1.0)

    def test_int(self):
        i = int(LIGOTimeGPS(1, 100))
        self.assertIsInstance(i, int)
        self.assertEqual(i, 1)

    if PY2:
        def test_long(self):
            l = long(LIGOTimeGPS(123456789, 123456789))
            self.assertIsInstance(l, long)
            self.assertEqual(l, 123456789)

    def test_ns(self):
        n = LIGOTimeGPS(12345, 67890).ns()
        self.assertIsInstance(n, int)
        self.assertEqual(n, 12345000067890)


    def test_eq_neq(self):
        self.assertEqual(LIGOTimeGPS(1), LIGOTimeGPS(1))
        self.assertNotEqual(LIGOTimeGPS(1), LIGOTimeGPS(2))
        self.assertEqual(LIGOTimeGPS(123456789.123456789),
                         LIGOTimeGPS(123456789.123456789))

    def test_lt_gt(self):
        # less than
        self.assertLess(LIGOTimeGPS(1), LIGOTimeGPS(2))
        self.assertLess(LIGOTimeGPS(1), 2)
        self.assertLess(LIGOTimeGPS(1, 200), LIGOTimeGPS(1, 300))
        # greater than
        self.assertGreater(LIGOTimeGPS(2), LIGOTimeGPS(1))
        self.assertGreater(LIGOTimeGPS(2), 1)
        # less equal
        self.assertLessEqual(LIGOTimeGPS(1), LIGOTimeGPS(2))
        self.assertLessEqual(LIGOTimeGPS(1), 2)
        self.assertLessEqual(1, LIGOTimeGPS(2))
        self.assertLessEqual(LIGOTimeGPS(2), LIGOTimeGPS(2))
        # greater equal
        self.assertGreaterEqual(LIGOTimeGPS(2), LIGOTimeGPS(1))
        self.assertGreaterEqual(LIGOTimeGPS(2), 1)
        self.assertGreaterEqual(2, LIGOTimeGPS(1))
        self.assertGreaterEqual(LIGOTimeGPS(2), LIGOTimeGPS(2))

    def test_hash(self):
        h = hash(LIGOTimeGPS(123, 456))
        self.assertIsInstance(h, int)
        self.assertEqual(h, 435)

    def test_round(self):
        # test round (down) to int
        a = LIGOTimeGPS(12345, 67890)
        b = round(a)
        if PY2:
            self.assertIsInstance(b, float)
        else:
            self.assertIsInstance(b, LIGOTimeGPS)
        self.assertEqual(b, 12345)
        # test round up
        self.assertEqual(round(LIGOTimeGPS(12345, 500000000)), 12346)
        # test round with decimal point
        b = round(a, 1)
        if not PY2:
            self.assertIsInstance(b, LIGOTimeGPS)
        self.assertEqual(b, 12345.0)
        self.assertEqual(round(a, 7), LIGOTimeGPS(12345, 67900))

    def test_add(self):
        a = LIGOTimeGPS(1) + LIGOTimeGPS(2)
        self.assertIsInstance(a, LIGOTimeGPS)
        self.assertEqual(a, 3)
        b = LIGOTimeGPS(1) + 2
        self.assertIsInstance(b, LIGOTimeGPS)
        self.assertEqual(a, b)
        c = 1 + LIGOTimeGPS(2)
        self.assertIsInstance(c, LIGOTimeGPS)
        self.assertEqual(a, c)
        a = 123.456 + LIGOTimeGPS(456, 999000000)
        self.assertEqual(a, 580.455)

    def test_sub(self):
        a = LIGOTimeGPS(2) - LIGOTimeGPS(1)
        self.assertIsInstance(a, LIGOTimeGPS)
        self.assertEqual(a, 1)
        b = LIGOTimeGPS(2) - 1
        self.assertIsInstance(a, LIGOTimeGPS)
        self.assertEqual(a, 1)
        c = 2 - LIGOTimeGPS(1)
        self.assertIsInstance(c, LIGOTimeGPS)
        self.assertEqual(c, 1)

    def test_mul(self):
        a = LIGOTimeGPS(2) * LIGOTimeGPS(5)
        self.assertIsInstance(a, LIGOTimeGPS)
        self.assertEqual(a, 10)
        b = LIGOTimeGPS(2) * 5
        self.assertIsInstance(b, LIGOTimeGPS)
        self.assertEqual(a, b)
        c = 2 * LIGOTimeGPS(5)
        self.assertIsInstance(c, LIGOTimeGPS)
        self.assertEqual(a, c)
        d = LIGOTimeGPS(123, 456000000) * LIGOTimeGPS(234, 567000000)
        self.assertAlmostEqual(d, 28958.703552)
        self.assertEqual(LIGOTimeGPS(-123, 456789000) * 2, -245.086422)
        self.assertAlmostEqual(LIGOTimeGPS(123, -456000000) * 4, 490.176)

    def test_div(self):
        a = LIGOTimeGPS(10) / LIGOTimeGPS(5)
        self.assertIsInstance(a, LIGOTimeGPS)
        self.assertEqual(a, 2)
        b = LIGOTimeGPS(10) / 5.
        self.assertIsInstance(b, LIGOTimeGPS)
        self.assertEqual(a, b)
        # check that we can't do int/LIGOTimeGPS
        with self.assertRaises(TypeError):
            10 / LIGOTimeGPS(2)
        # check crazy numbers work (almost)
        d = LIGOTimeGPS(123, 456789012) / 3.14159265
        self.assertAlmostEqual(d, 39.2975165039)

    def test_mod(self):
        self.assertEqual(LIGOTimeGPS(100.5) % 3, 1.5)

    def test_pos(self):
        a = LIGOTimeGPS(1, 234)
        self.assertEqual(a, +a)

    def test_neg(self):
        a = LIGOTimeGPS(1, 234)
        self.assertEqual(-a, LIGOTimeGPS(-2, 999999766))

    def test_abs(self):
        a = LIGOTimeGPS(123, 456789)
        self.assertEqual(abs(a), a)
        self.assertEqual(abs(-a), a)
