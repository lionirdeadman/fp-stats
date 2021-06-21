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

import collections
import fnmatch
import json
import os
import subprocess
from os.path import exists
from distutils.version import LooseVersion
from datetime import date
from pathlib import Path

# These are all the known runtimes, this is used to filter out extensions
valid_runtimes = [
    "org.gnome.Platform",
    "org.gnome.Sdk",
    "org.kde.Platform",
    "org.kde.Sdk",
    "org.freedesktop.Platform",
    "org.freedesktop.Sdk",
]

# By default, they should start with list for easy appending
runtime_information = collections.defaultdict(lambda: collections.defaultdict(list))

# Create class to handle version format
def by_version(kv):
    return LooseVersion(kv[0].split("//")[1])


# For each folder, do X
for i in os.listdir("flathub/"):

    # Check the extension of the manifest
    if exists(f"flathub/{i}/{i}.json"):
        extension = ".json"
    if exists(f"flathub/{i}/{i}.yml"):
        extension = ".yml"
    if exists(f"flathub/{i}/{i}.yaml"):
        extension = ".yaml"

    # This application is broken and breaks running
    if i == "io.github.markummitchell.Engauge_Digitizer":
        continue

    # If EOL (but not yet archived), don't count it
    if exists(f"flathub/{i}/flathub.json"):
        with open(f"flathub/{i}/flathub.json", "r") as json_file:
            flathub_json = json.load(json_file)
            if flathub_json.get("end-of-life"):
                print(f"{i} is not archived but EOL!")
                continue

    # Run flatpak-builder to get a JSON output even if it's a YAML file
    raw_output = subprocess.run(
        ["flatpak-builder", "--show-manifest", f"flathub/{i}/{i}{extension}"],
        check=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
    )
    output = raw_output.stdout
    manifest = json.loads(output)

    # Check if runtime is valid to avoid extensions cluttering things up
    if not manifest["runtime"] in valid_runtimes:
        continue

    # Divide runtimes into 3 categories to make clearer data later
    runtime_name_and_syntax = manifest["runtime"] + "//" + manifest["runtime-version"]
    if fnmatch.fnmatch(manifest["runtime"], "org.kde.*"):
        runtime_information["KDE"][runtime_name_and_syntax].append(manifest["id"])
    if fnmatch.fnmatch(manifest["runtime"], "org.gnome.*"):
        runtime_information["GNOME"][runtime_name_and_syntax].append(manifest["id"])
    if fnmatch.fnmatch(manifest["runtime"], "org.freedesktop.*"):
        runtime_information["Freedesktop"][runtime_name_and_syntax].append(manifest["id"])

# Sort it by version
sorted_runtime_information = {group: dict(sorted(runtime_version.items(), key=by_version, reverse=True)) for group, runtime_version in runtime_information.items()}

# Prettify the JSON
pretty_runtime_information = json.dumps(sorted_runtime_information, indent=4)

# Save data to file based on date
date_prefix = str(date.today()).replace("-", "/")

# Make sure folder is there to git clone later
if not Path(f"runtime_version_information/{date_prefix}").is_dir():
    os.makedirs(f"runtime_version_information/{date_prefix}")

with open(f"runtime_version_information/{date_prefix}/runtime_information.json", "w") as stats:
    stats.write(pretty_runtime_information)
    stats.close()
