# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import powerlaw

project = 'powerlaw'
copyright = '2025, Jeff Alstott'
author = 'Jeff Alstott'
release = powerlaw.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'numpydoc',
              'sphinx.ext.autosummary',
              'sphinx_subfigure',
              'sphinx.ext.githubpages',
              'sphinx_exec_code',
              'matplotlib.sphinxext.plot_directive',
             ]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": True,
}

templates_path = ['_templates']
exclude_patterns = []

autoclass_content = 'both'

#autosummary_generate = True

numpydoc_class_members_toctree = False

# Options for exec-code

# Root directory is the working dir
#exec_code_working_dir = '..'
#exec_code_source_folders = ['../powerlaw']

# Options for matplotlib plotting directive
plot_include_source = True
plot_pre_code = """
# Suppress all warnings, mostly useful for stopping powerlaw warnings, not
# mpl ones.
import warnings
warnings.filterwarnings('ignore')  
"""
plot_rcparams = {"figure.figsize": (4.5, 4.5),
                 "figure.dpi": 150,
                 "font.size": 12}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

html_css_files = ['overrides.css']
