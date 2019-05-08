"""Tools and utilities to improve your experience with Jupyter Notebooks."""

from .__about__ import __version__

from .config import defaults

from .utils import disable_nbextension
from .utils import enable_nbextension
from .utils import install_nbextension
from .utils import load_nbextension

__all__ = [
    'init_notebook_mode',
    'load_ipython_extension'
]


def init_notebook_mode(opts: dict = None):
    """Initialize default tools."""
    opts: dict = opts or defaults


def load_ipython_extension(ipython):
    """Load the IPython extension."""
    from .warnings import suppress_warnings  # autoregister
