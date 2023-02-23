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

import glob
import os
import pathlib

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files, get_module_file_attribute
from PyInstaller import compat

hiddenimports = ['numpy']

# On Windows, make sure that opencv_videoio_ffmpeg*.dll is bundled
binaries = []
if compat.is_win:
    # If conda is active, look for the DLL in its library path
    if compat.is_conda:
        libdir = os.path.join(compat.base_prefix, 'Library', 'bin')
        pattern = os.path.join(libdir, 'opencv_videoio_ffmpeg*.dll')
        for f in glob.glob(pattern):
            binaries.append((f, '.'))

    # Include any DLLs from site-packages/cv2 (opencv_videoio_ffmpeg*.dll
    # can be found there in the PyPI version)
    binaries += collect_dynamic_libs('cv2')

# OpenCV loader from 4.5.4.60 requires extra config files and modules
datas = collect_data_files('cv2', include_py_files=True, includes=['**/*.py'])

# The OpenCV versions that attempt to perform module substitution via sys.path manipulation (== 4.5.4.58, >= 4.6.0.66)
# do not directly import the cv2.cv2 extension anymore, so in order to ensure it is collected, we need to add it to
# hidden imports.
hiddenimports += ['cv2.cv2']

# Mark the cv2 package to be collected in source form, bypassing PyInstaller's PYZ archive and FrozenImporter. This is
# necessary because recent versions of cv2 package attempt to perform module substritution via sys.path manipulation,
# which is incompatible with the way that FrozenImporter works. This requires pyinstaller/pyinstaller#6945, i.e.,
# PyInstaller > 5.2. On earlier versions, the following statement does nothing, and problematic cv2 versions
# (== 4.5.4.58, >= 4.6.0.66) will not work.
#
# Note that the collect_data_files() above is still necessary, because some of the cv2 loader's config scripts are not
# valid module names (e.g., config-3.py). So the two collection approaches are complementary, and any overlap in files
# (e.g., __init__.py) is handled gracefully due to PyInstaller's uniqueness constraints on collected files.
module_collection_mode = 'py'

# In linux PyPI opencv-python wheels, the cv2 extension is linked against Qt, and the wheel bundles a basic subset of Qt
# shared libraries, plugins, and font files. This is not the case on other OSes (presumably native UI APIs are used by
# OpenCV HighGUI module), nor in the headless PyPI wheels (opencv-python-headless).
# The bundled Qt shared libraries should be picked up automatically due to binary dependency analysis, but we need to
# collect plugins and font files from the `qt` subdirectory.
if compat.is_linux:
    pkg_path = pathlib.Path(get_module_file_attribute('cv2')).parent
    # Collect .ttf files fron fonts directory.
    # NOTE: since we are using glob, we can skip checks for (sub)directories' existence.
    qt_fonts_dir = pkg_path / 'qt' / 'fonts'
    datas += [
        (str(font_file), str(font_file.parent.relative_to(pkg_path.parent)))
        for font_file in qt_fonts_dir.rglob('*.ttf')
    ]
    # Collect .so files from plugins directory.
    qt_plugins_dir = pkg_path / 'qt' / 'plugins'
    binaries += [
        (str(plugin_file), str(plugin_file.parent.relative_to(pkg_path.parent)))
        for plugin_file in qt_plugins_dir.rglob('*.so')
    ]
