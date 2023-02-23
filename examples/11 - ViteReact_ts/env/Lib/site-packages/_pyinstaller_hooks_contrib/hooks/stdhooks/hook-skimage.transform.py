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
from PyInstaller.utils.hooks import collect_data_files

# Hook tested with scikit-image (skimage) 0.9.3 on Mac OS 10.9 and Windows 7
# 64-bit
hiddenimports = ['skimage.draw.draw',
                 'skimage._shared.geometry',
                 'skimage._shared.transform',
                 'skimage.filters.rank.core_cy']

datas = collect_data_files('skimage')
