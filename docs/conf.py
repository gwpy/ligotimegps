# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config


from ligotimegps import __version__ as VERSION

# -- Project information -----------------------------------------------------

project = "ligotimegps"
copyright = "2010-2016, Kipp Cannon; 2017-2025 Cardiff University"
author = "Duncan Macleod"

# The full version, including alpha/beta/rc tags
release = VERSION


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_automodapi.automodapi",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "monokai"

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "obj"

# Default file type
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Epilogue
rst_epilog = """

.. |lal.LIGOTimeGPS| replace:: `lal.LIGOTimeGPS`
.. _lal.LIGOTimeGPS: https://lscsoft.docs.ligo.org/lalsuite/lal/struct_l_i_g_o_time_g_p_s.html

"""


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

# -- Extensions --------------------------------------------------------------

# Intersphinx directory
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
}

# Don't inherit in automodapi
numpydoc_show_class_members = False
automodapi_inherited_members = False
