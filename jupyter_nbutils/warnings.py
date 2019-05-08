# jupyter-nbutils
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

"""Suppress and manage warnings in Jupyter notebook on demand."""

import re

from IPython.core.getipython import get_ipython
from IPython.core.magic import register_cell_magic

from jupyter_require.core import execute_with_requirements


@register_cell_magic
def suppress_warnings(line: str = None, cell: str = None, local_ns: dict = None):
    """Suppress all stderr output produced by function call.

    NOTE: The output is still present in the DOM, but not visible.
    """
    _ = line  # line
    _ = local_ns  # ignore

    shell = get_ipython()

    code = cell
    last_command = None

    code_lines = cell.splitlines()
    if not re.search(r"^(\s)+", code_lines[-1]):
        # is not part of a block, evaluate separately
        last_command = code_lines.pop()
        code = '\n'.join(code_lines)

    # evaluate the whole script except the last line
    shell.ex(code)

    try:
        # try to evaluate and return last command
        ret = shell.ev(last_command)
    except SyntaxError:
        # if this one throws too, then its users error
        ret = shell.ex(last_command)

    # suppress warnings produced by the execution
    script = """
        $(element)
            .parents('.output')
            .find('.output_stderr')
            .css('display', 'none');
    """

    execute_with_requirements(script, required=[])

    return ret


def display_suppressed_warnings():
    """Display all stderr output cells suppresed by `suppress_warnings`."""
    script = """
        $(element)
            .parents('.output')
            .find('.output_stderr')
            .css('display', 'block');
    """

    return execute_with_requirements(script, required=[])

