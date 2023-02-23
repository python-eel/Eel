# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE.GPL.txt, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------
import os
from . import stdhooks
from . import rthooks
_FILE_DIR = os.path.dirname(__file__)


def get_hook_dirs():
    return [
        *stdhooks.get_hook_dirs(),
        *rthooks.get_hook_dirs(),
        _FILE_DIR  # pre_* hooks
    ]
