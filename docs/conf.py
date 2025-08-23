# Configuration file for the Sphinx documentation builder.

import  sphinx_rtd_theme 

#//////////////////////////////////////////////
project = 'seclabs'
copyright = '2025, Spyridon Antakis'
author = 'Spyridon Antakis'
extensions = ['sphinx_rtd_theme',]
#----------------------------------------------
add_module_names = False
#----------------------------------------------
logo_url = 'https://github.com/santakis/seclabs'
#----------------------------------------------
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
#----------------------------------------------
html_permalinks = False
html_static_path = ['static']
html_favicon = 'static/favicon.ico'
html_theme = 'sphinx_rtd_theme'
