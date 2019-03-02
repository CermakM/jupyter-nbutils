# jupyter-tools
# Copyright 2019 Marek Cermak <macermak@redhat.com>
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Interactive debugging and breakpoint setting."""

import re

from typing import List

from IPython.core.getipython import get_ipython
from IPython.core.magic import register_cell_magic

from jupyter_d3.core import execute_js


@register_cell_magic
def debug(line: str = None, cell: str = None, local_ns = None):
    """Toggle debugging mode for the current cell."""
    is_on = re.match(r"\b(on|true)\b", line.strip().lower(), re.IGNORECASE)

    breakpoints = _get_breakpoints()


def _get_breakpoints() -> List[int]:
    """Retrieve breakpoints from the current cell.

    :returns: list of line numbers containing breakpoints
    """
    breakpoints = []

    return breakpoints
