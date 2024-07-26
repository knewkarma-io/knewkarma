from datetime import date

# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "Knew Karma"
author = "Richard Mwewa"
copyright = f"{date.today().year}, {author}"

release = "5.3"
version = "5.3.6"

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

html_theme = "alabaster"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_show_sphinx = False
html_theme_options = {
    "show_powered_by": False,
    "github_user": "bellingcat",
    "github_repo": "knewkarma",
    "github_banner": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}

# -- Options for EPUB output
epub_show_urls = "footnote"
