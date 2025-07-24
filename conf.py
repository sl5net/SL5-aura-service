import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SL5 Dictation'
copyright = '2025, Sebastian, Lena, Andy'
author = 'Sebastian, Lena, Andy'
release = '0.4.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []
extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['.venv', '_build', 'Thumbs.db', '.DS_Store']
# exclude_patterns = ['.venv']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'furo'

html_static_path = ['_static']
