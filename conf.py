import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# Get the version from the environment variable set by the CI workflow
# Fallback to 'dev' for local builds
release = os.environ.get('DOCS_VERSION', 'dev')
version = release


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SL5 Dictation'
copyright = '2025, Sebastian, Lena, Andy'
author = 'Sebastian, Lena, Andy'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []
extensions = ['sphinx.ext.autodoc', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = ['.venv', '_build', 'Thumbs.db', '.DS_Store']
# exclude_patterns = ['.venv']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'furo'

html_static_path = ['_static']
