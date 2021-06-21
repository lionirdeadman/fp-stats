#!/usr/bin/env python3
#
# Copyright © 2021 Lionir
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <https://www.gnu.org/licenses/>.
#

import json
from pathlib import Path
from distutils.version import LooseVersion
from datetime import date, timedelta

# Check if date for today is available, if not use yesterday.
date_prefix = str(date.today()).replace("-", "/")
if Path(f"runtime_version_information/{date_prefix}/runtime_information.json").is_file():
    print("Here are today's runtime numbers!")
else:
    date_prefix = str(date.today() - timedelta(days=1)).replace("-", "/")
    print("Here are yesterday's runtime numbers!")

with open(f"runtime_version_information/{date_prefix}/runtime_information.json", "r") as raw_stats:
    stats = json.load(raw_stats)

    # Make totals for percentages
    total_freedesktop = 0
    total_gnome = 0
    total_kde = 0
    for runtime_version, runtime_list in stats["Freedesktop"].items():
        total_freedesktop += len(runtime_list)

    for runtime_version, runtime_list in stats["GNOME"].items():
        total_gnome += len(runtime_list)

    for runtime_version, runtime_list in stats["KDE"].items():
        total_kde += len(runtime_list)

    # Print numbers and percentages
    print()
    print("Freedesktop:")
    print()
    for runtime_version, runtime_list in stats["Freedesktop"].items():
        print(f"{runtime_version:<35} : {len(runtime_list):<5} ({round(len(runtime_list)*100/total_freedesktop, 1):<4}%)")
    print(f"org.freedesktop.*//*:               : {total_freedesktop:<4}")

    print()
    print("GNOME:")
    print()
    for runtime_version, runtime_list in stats["GNOME"].items():
        print(f"{runtime_version:<35} : {len(runtime_list):<5} ({round(len(runtime_list)*100/total_gnome, 1):<4}%)")
    print(f"org.gnome.*//*:                     : {total_gnome:<4}")

    print()
    print("KDE:")
    print()
    for runtime_version, runtime_list in stats["KDE"].items():
        print(f"{runtime_version:<35} : {len(runtime_list):<5} ({round(len(runtime_list)*100/total_kde, 1):<4}%)")
    print(f"org.kde.*//*:                       : {total_kde:<4}")
