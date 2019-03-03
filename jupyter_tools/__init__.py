"""Tools and utilities to improve your experience with Jupyter Notebooks."""


def load_ipython_extension(ipython):
    """Load the IPython extension."""
    from .warnings import suppress_warnings  # autoregister

