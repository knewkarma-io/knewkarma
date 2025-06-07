import os
import sys
from datetime import date

# Add the path to the 'src' directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)
from knewkarma.meta.about import Project
from knewkarma.meta.version import Version

# Ignore warning for files not in toctree (We have a custom sidebar.html file)
suppress_warnings = ["toc.not_included"]


# Configuration file for the Sphinx documentation builder.

# -- Project information
project = Project.name

copyright = f' {date.today().year} GPL-3.0+ License, <a href="https://github.com/knewkarma-io" target="_blank">Knew Karma IO</a>'

release = Version.release
version = Version.full_version

# -- General configuration

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output
master_doc = "index"
html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]
html_favicon = "_static/favicon16x16.ico"
html_logo = "_static/logo512x512.png"
html_show_sphinx = False
html_show_sourcelink = False
html_sidebars = {
    "**": [
        "sidebar.html",  # Add your custom sidebar logo template here
        "searchbox.html",
    ]
}
html_theme_options = {
    "show_powered_by": False,
    "github_user": "knewkarma-io",
    "github_repo": Project.package,
    "github_banner": True,
    "sidebar_collapse": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}

# -- Options for EPUB output
epub_show_urls = "footnote"
