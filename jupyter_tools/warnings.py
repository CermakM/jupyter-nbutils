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

"""Suppress and manage warnings in Jupyter notebook on demand."""


from IPython.core.getipython import get_ipython
from IPython.core.magic import register_cell_magic

from jupyter_d3.core import execute_js


@register_cell_magic
def suppress_warnings(line: str = None, cell: str = None, local_ns = None):
    """Suppress all stderr output produced by function call.

    NOTE: The output is still present in the DOM, but not visible.
    """
    shell = get_ipython()
    shell.ex(cell)
    
    # suppress warnings produced by the execution
    execute_js("""
        $(element)
            .parents('.output')
            .find('.output_stderr')
            .css('display', 'none');
    """)

    # evaluate the last command in the current namespace
    # to display the output
    namespace = shell.user_ns
    namespace.update(shell.user_global_ns)
    
    last_command = cell.splitlines()[-1]
    try:
        # already evaluated expression, display statement
        ret = namespace[last_command]
    except KeyError:
        # evaluate and display the result
        ret = shell.ev(last_command)
    
    return ret

def display_suppressed_warnings():
    """Display all stderr output cells suppresed by `suppress_warnings`."""
    return execute_js("""
            $(element)
                .parents('.output')
                .find('.output_stderr')
                .css('display', 'block');
        """)

