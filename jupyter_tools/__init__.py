"""Tools and utilities to improve your experience with Jupyter Notebooks."""

from pathlib import Path

from jupyter_require import load_css


_HERE = Path(__file__).parent


def set_style():
    """Set default jupyter-tools stylesheets."""
    load_css(Path(_HERE, 'assets/main.css'))


def load_ipython_extension(ipython):
    """Load the IPython extension."""
    from .warnings import suppress_warnings  # autoregister

