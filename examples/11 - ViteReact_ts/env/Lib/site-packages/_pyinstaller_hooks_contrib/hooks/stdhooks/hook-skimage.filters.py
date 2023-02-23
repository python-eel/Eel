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

from PyInstaller.utils.hooks import is_module_satisfies

# The following missing module prevents import of skimage.feature
# with skimage 0.18.x.
if is_module_satisfies("scikit_image >= 0.18.0"):
    hiddenimports = ['skimage.filters.rank.core_cy_3d', ]
