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

import os
import json
import datetime
import time
from pathlib import Path

all_data = {"runtime_version_information": {}}

base = "runtime_version_information"
for year in os.listdir(f"{base}"):
    for month in os.listdir(f"{base}/{year}"):
        for day in os.listdir(f"{base}/{year}/{month}"):
            fd = open(f"{base}/{year}/{month}/{day}/runtime_information.json")
            raw_data = json.load(fd)
            summary_data = {
                "Freedesktop": {},
                "GNOME": {},
                "KDE": {},
            }
            for runtime_version, runtime_list in raw_data["Freedesktop"].items():
                summary_data["Freedesktop"][runtime_version] = len(runtime_list)
            for runtime_version, runtime_list in raw_data["GNOME"].items():
                summary_data["GNOME"][runtime_version] = len(runtime_list)
            for runtime_version, runtime_list in raw_data["KDE"].items():
                summary_data["KDE"][runtime_version] = len(runtime_list)
            fd.close()
            unix_time = time.mktime(datetime.datetime(int(year), int(month), int(day)).timetuple())
            all_data["runtime_version_information"][unix_time] = summary_data

pretty_summary_data = json.dumps(all_data, indent=4)

# Make sure folder is there to git clone later
if not Path("summaries").is_dir():
    os.makedirs("summaries")

with open(f"summaries/runtime_version_information.json", "w") as stats:
    stats.write(pretty_summary_data)
    stats.close()
