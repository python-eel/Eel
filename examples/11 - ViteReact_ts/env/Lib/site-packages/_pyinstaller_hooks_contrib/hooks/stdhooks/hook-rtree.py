# ------------------------------------------------------------------
# Copyright (c) 2021 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE.GPL.txt, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------

from PyInstaller.compat import is_pure_conda
from PyInstaller.utils.hooks import collect_dynamic_libs, conda

binaries = collect_dynamic_libs('rtree', destdir='rtree/lib')
if not binaries and is_pure_conda:
    binaries = conda.collect_dynamic_libs('libspatialindex', dest='rtree/lib', dependencies=False)
