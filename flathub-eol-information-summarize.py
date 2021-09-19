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

runtime_eol = {
    "1.6": "1541548800",
    "18.08": "1577577600",
    "19.08": "1631836800",
    "3.24": "1541548800",
    "3.26": "1541548800",
    "3.28": "1541548800",
    "3.30": "1584921600",
    "3.32": "1584921600",
    "3.34": "1599436800",
    "3.36": "1616544000",
    "5.9": "1576627200",
    "5.10": "1526342400",
    "5.11": "1544659200",
    "5.12": "1600819200",
    "5.13": "1584921600",
}

all_data = {"runtime_eol_information": {}}

base = "runtime_version_information"
for year in os.listdir(f"{base}"):
    for month in os.listdir(f"{base}/{year}"):
        for day in os.listdir(f"{base}/{year}/{month}"):
            fd = open(f"{base}/{year}/{month}/{day}/runtime_information.json")
            raw_data = json.load(fd)
            summary_data = {
                "EOL": 0,
                "Supported": 0,
            }

            unix_time = time.mktime(datetime.datetime(int(year), int(month), int(day)).timetuple())

            for category in raw_data:
                print(category)
                for runtime, applications in raw_data[category].items():
                    print(runtime)
                    runtime_version = runtime.split("/")[-1]

                    if runtime_version in runtime_eol.keys() and int(unix_time) >= int(runtime_eol[runtime_version]):
                        summary_data["EOL"] += len(applications)
                    else:
                        summary_data["Supported"] += len(applications)

            fd.close()

            all_data["runtime_eol_information"][unix_time] = summary_data

pretty_summary_data = json.dumps(all_data, indent=4)

# Make sure folder is there to git clone later
if not Path("summaries").is_dir():
    os.makedirs("summaries")

with open(f"summaries/runtime_eol_information.json", "w") as stats:
    stats.write(pretty_summary_data)
    stats.close()
