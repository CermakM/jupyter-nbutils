# jupyter-tools
# Copyright 2019 Marek Cermak <macermak@redhat.com>

"""Default configuration for Jupyter tools."""

from collections import namedtuple

__all__ = ['defaults']


_DEFAULT_CONFIG = {
    'warnings': True,
}

DefaultConfig = namedtuple('DefaultConfig', _DEFAULT_CONFIG.keys())

defaults = DefaultConfig(**_DEFAULT_CONFIG)
"""Default configuration for Jupyter tools."""
