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

# core/_templates/*
# server/static/**/*
# subcommands/*.py
# bokeh/_sri.json

datas = collect_data_files('bokeh.core') + \
        collect_data_files('bokeh.server') + \
        collect_data_files('bokeh.command.subcommands', include_py_files=True) + \
        collect_data_files('bokeh')
