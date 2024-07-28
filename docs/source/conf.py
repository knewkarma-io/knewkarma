from datetime import date

from knewkarma.version import Version

# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "Knew Karma"
author = "Richard Mwewa"
copyright = (
    f" {date.today().year} MIT License, "
    f'<a href="https://gravatar.com/rly0nheart" target="_blank">{author}</a>'
)


release = Version.release
version = Version.full

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
html_favicon = "_static/favicon.ico"
html_logo = "_static/logo.png"
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
    "github_user": "bellingcat",
    "github_repo": "knewkarma",
    "github_banner": True,
    "sidebar_collapse": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}

# -- Options for EPUB output
epub_show_urls = "footnote"
