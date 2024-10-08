from datetime import date

from knewkarma.meta import about, version

# Configuration file for the Sphinx documentation builder.

# -- Project information
author_name, author_username, author_link = about.author

project = about.name
author = author_name
copyright = f' {date.today().year} GPL-3.0 License, <a href="{author_link}" target="_blank">{author_name}</a>'

release = version.release
version = version.full

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
    "github_user": author_username,
    "github_repo": about.package,
    "github_banner": True,
    "sidebar_collapse": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}

# -- Options for EPUB output
epub_show_urls = "footnote"
