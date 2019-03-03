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

"""Jupyter interactive pandas DataFrame representation."""

import pandas as pd

from pathlib import Path

from jupyter_require import require
from jupyter_require import link_css
from jupyter_require import load_css


_HERE = Path(__file__).parent


def init_datatables_mode():
    """Initialize DataTable mode for pandas DataFrame represenation."""
    # configure path to the datatables library using requireJS
    # that way the library will become globally available
    require('DT', 'https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min')

    # link stylesheets
    link_css('https://cdn.datatables.net/1.10.19/css/jquery.dataTables.css')
    # load custom style
    load_css(
        Path(_HERE, './main.css').read_text(encoding='utf-8'), {'id': 'datatables-stylesheet'})

    def _repr_datatable_(self):
        """Return DataTable representation of pandas DataFrame."""
        # classes for dataframe table (optional)
        classes = ['table', 'table-striped', 'table-bordered']

        # create table DOM
        script = (
            f"const table = $.parseHTML(`{self.to_html(index=False, classes=classes)}`);"
            """
            require(['DT'], function(DT) {
                $(table).ready( () => {
                    // Turn existing table into datatable
                    $(table).DataTable({
                        scrollX: true,
                        pagingType: 'full_numbers'
                    });
                })
            });
            
            $(element).append(table);
            """
        )

        return script

    pd.DataFrame._repr_javascript_ = _repr_datatable_
