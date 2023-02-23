# ------------------------------------------------------------------
# Copyright (c) 2022 PyInstaller Development Team.
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

# As of v2022.05.18, yt_dlp requires a hidden import of yt_dlp.compat._legacy due to indirect import
if is_module_satisfies("yt_dlp >= 2022.05.18"):
    hiddenimports = ['yt_dlp.compat._legacy']
