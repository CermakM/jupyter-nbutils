"""Tools and utilities to improve your experience with Jupyter Notebooks."""


from .datatables import init_datatables_mode
from .config import defaults

__all__ = [
    'init_datatables_mode', 'init_notebook_mode',
    'load_ipython_extension'
]


def init_notebook_mode(opts: dict = None):
    """Initialize default tools."""
    opts: dict = opts or defaults

    # initialize tools
    init_datatables_mode(opts.pop('datatables', {}))


def load_ipython_extension(ipython):
    """Load the IPython extension."""
    from .warnings import suppress_warnings  # autoregister

