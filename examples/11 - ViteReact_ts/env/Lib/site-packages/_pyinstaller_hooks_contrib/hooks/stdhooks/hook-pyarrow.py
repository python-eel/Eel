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

# Hook for https://pypi.org/project/pyarrow/

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

hiddenimports = [
    "pyarrow._parquet",
    "pyarrow.lib",
    "pyarrow.compat",
]

datas = collect_data_files('pyarrow')
binaries = collect_dynamic_libs('pyarrow')
