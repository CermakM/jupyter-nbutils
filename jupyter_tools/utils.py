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

"""Common utilities for IPython operations."""

import json
import sys

from . import config


_IPYTHON_VARS = {'In', 'Out'}


def sanitize_namespace(user_ns, bindings=None, blacklist=None, allow_private=False):
    """Filter namespace."""
    bindings = bindings or dict()
    blacklist = blacklist or dict()

    namespace = dict()

    for k, v in user_ns.items():

        try:
            json.dumps(v)
        except Exception as exc:
            if config.defaults.warnings:
                print("[WARNING] Serialization of object `{obj}` failed. Skipping.".format(obj=k),
                      exc, file=sys.stderr)
            continue

        if k in blacklist:
            continue

        # pop ipython vars (if they are not overridden by user)
        if k in _IPYTHON_VARS and k not in bindings:
            continue

        if k.startswith('_') and not allow_private:
            if k in bindings:
                namespace[k] = v
            else:
                continue

        namespace[k] = v

    return namespace
