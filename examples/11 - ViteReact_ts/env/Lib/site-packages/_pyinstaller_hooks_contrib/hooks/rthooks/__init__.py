# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the Apache License 2.0
#
# The full license is available in LICENSE.APL.txt, distributed with
# this software.
#
# SPDX-License-Identifier: Apache-2.0
# ------------------------------------------------------------------
import os
DIR = os.path.dirname(__file__)

"""
This sub-package includes runtime hooks for pyinstaller.
"""


def get_hook_dirs():
    dirs = []
    # For every directory and sub directory (including cwd)
    for path, _, _ in os.walk(DIR):
        # Add the norm'd path to dirs
        dirs.append(os.path.normpath(path))
    
    return dirs