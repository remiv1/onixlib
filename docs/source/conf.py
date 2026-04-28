"""Configuration de Sphinx pour la documentation d'onixlib."""
import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

# ---------------------------------------------------------------------------
# Infos du projet
# ---------------------------------------------------------------------------
project = "onixlib" # pylint: disable=invalid-name
author = "Rémi Verschuur"   # pylint: disable=invalid-name
release = "0.1.0"   # pylint: disable=invalid-name
language = "fr" # pylint: disable=invalid-name

# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# ---------------------------------------------------------------------------
# Thème HTML
# ---------------------------------------------------------------------------
html_theme = "furo" # pylint: disable=invalid-name
