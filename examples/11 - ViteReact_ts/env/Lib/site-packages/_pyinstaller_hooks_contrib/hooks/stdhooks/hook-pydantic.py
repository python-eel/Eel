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

from PyInstaller.utils.hooks import get_module_attribute, collect_submodules
from PyInstaller.utils.hooks import is_module_satisfies

# By default, pydantic from PyPi comes with all modules compiled as
# cpython extensions, which seems to prevent pyinstaller from automatically
# picking up the submodules.
# NOTE: in PyInstaller 4.x and earlier, get_module_attribute() returns the
# string representation of the value ('True'), while in PyInstaller 5.x
# and later, the actual value is returned (True).
is_compiled = get_module_attribute('pydantic', 'compiled') in {'True', True}
if is_compiled:
    # Compiled version; we need to manually collect the submodules from
    # pydantic...
    hiddenimports = collect_submodules('pydantic')
    # ... as well as the following modules from the standard library
    hiddenimports += [
        'colorsys',
        'dataclasses',
        'decimal',
        'json',
        'ipaddress',
        'pathlib',
        'uuid',
        # Optional dependencies.
        'dotenv',
    ]
    # Older releases (prior 1.4) also import distutils.version
    if not is_module_satisfies('pydantic >= 1.4'):
        hiddenimports += ['distutils.version']
    # Version 1.8.0 introduced additional dependency on typing_extensions
    if is_module_satisfies('pydantic >= 1.8'):
        hiddenimports += ['typing_extensions']
