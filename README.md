# LIGOTimeGPS

This module provides a pure-python version of the `LIGOTimeGPS` class, used to represent GPS times (number of seconds elapsed since GPS epoch) with nanoseconds precision.

[![PyPI version](https://badge.fury.io/py/ligotimegps.svg)](http://badge.fury.io/py/ligotimegps)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/ligotimegps.svg)](https://anaconda.org/conda-forge/ligotimegps/)
[![License](https://img.shields.io/pypi/l/ligotimegps.svg)](https://choosealicense.com/licenses/gpl-3.0/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/ligotimegps.svg)

## Description

This module is primarily for use as a drop-in replacement for the 'official' `lal.LIGOTimeGPS` class (provided by the SWIG-python bindings of [LAL](//wiki.ligo.org/DASWG/LALSuite)) for use on those environments where LAL is not available, or building LAL is unnecessary for the application (e.g. testing).

The code provided here is much slower than the C-implementation provided by LAL, so if you really care about performance, don't use this module.

## How to install

```bash
python -m pip install ligotimegps
```

## How to use

```python
>>> from ligotimegps import LIGOTimeGPS
>>> t = LIGOTimeGPS(12345, 67890)
>>> print(t)
12345.00006789
```
