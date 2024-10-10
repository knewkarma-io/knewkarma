from datetime import date

from knewkarma.meta.about import Author
from knewkarma.meta.about import Project
from knewkarma.meta.version import Version

# Configuration file for the Sphinx documentation builder.

# -- Project information
project = Project.name

copyright = f' {date.today().year} GPL-3.0+ License, <a href="{Author.gravatar}" target="_blank">{Author.name}</a>'

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
