# Copyright (c) 2017-2025 Cardiff University

from ligotimegps import __version__ as LIGOTIMEGPS_VERSION

# -- Project information -------------

project = "ligotimegps"
copyright = "2010-2016, Kipp Cannon; 2017-2025 Cardiff University"
author = "Duncan Macleod"
release = LIGOTIMEGPS_VERSION
version = "dev" if ".dev" in LIGOTIMEGPS_VERSION else LIGOTIMEGPS_VERSION

# -- General configuration -----------

# Default role for single backticks
default_role = "obj"

# Epilogue
rst_epilog = """

.. |lal.LIGOTimeGPS| replace:: `lal.LIGOTimeGPS`
.. _lal.LIGOTimeGPS: https://lscsoft.docs.ligo.org/lalsuite/lal/struct_l_i_g_o_time_g_p_s.html

"""

# -- HTML formatting -----------------

html_theme = "furo"
html_title = f"{project} {version}"

# -- Extensions ----------------------

extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_automodapi.automodapi",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]

# Intersphinx directory
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
}

# Don't inherit in automodapi
numpydoc_show_class_members = False
automodapi_inherited_members = False

# myst_parser
myst_enable_extensions = [
    "attrs_block",
]
