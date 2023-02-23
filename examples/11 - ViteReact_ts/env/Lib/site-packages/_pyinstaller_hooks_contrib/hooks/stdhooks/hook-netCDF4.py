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

from PyInstaller.utils.hooks import is_module_satisfies

# netCDF4 (tested with v.1.1.9) has some hidden imports
hiddenimports = ['netCDF4.utils']

# Around netCDF4 1.4.0, netcdftime changed name to cftime
if is_module_satisfies("netCDF4 < 1.4.0"):
    hiddenimports += ['netcdftime']
else:
    hiddenimports += ['cftime']
