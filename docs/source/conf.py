from datetime import date

# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "Knew Karma"
author = "Richard Mwewa"
copyright = f"{date.today().year}, {author}"

release = "5.3.4"
version = "5.3.4"

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

html_theme = "sphinx_rtd_theme"
html_favicon = "images/favicon.ico"

# -- Options for EPUB output
epub_show_urls = "footnote"
