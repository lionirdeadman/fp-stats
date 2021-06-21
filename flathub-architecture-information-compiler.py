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

# These are all the known runtimes, this is used to filter out extensions
valid_runtimes = ["org.gnome.Platform", "org.gnome.Sdk", "org.kde.Platform", "org.kde.Sdk", "org.freedesktop.Platform", "org.freedesktop.Sdk"]

# Map GNOME, KDE and Freedesktop to assume available archs
runtime_versions_1_6 = ["1.6", "3.26", "3.28", "5.9","5.10","5.11"]
runtime_versions_18_08 = ["18.08", "3.30", "3.32", "5.12"]
runtime_versions_19_08 = ["19.08", "3.34", "3.36", "5.13", "5.14"]
runtime_versions_20_08 = ["20.08", "3.38", "5.15", "40"]

# Assumed available runtimes
archs_1_6 = {"x86_64","i386","aarch64", "arm"}
archs_18_08 = {"x86_64","i386","aarch64", "arm"}
archs_19_08 = {"x86_64","aarch64","arm"}
archs_20_08 = {"x86_64","aarch64"}

# By default, they should start with list for easy appending
runtime_information = collections.defaultdict(list)

# Create class to handle version format
def by_version(kv):
    return LooseVersion(kv[0].split('//')[1])

# For each folder, do X
for i in os.listdir('flathub/'):

    # Check the extension of the manifest
    if exists(f'flathub/{i}/{i}.json'):
        extension = ".json"
    if exists(f'flathub/{i}/{i}.yml'):
        extension = ".yml"
    if exists(f'flathub/{i}/{i}.yaml'):
        extension = ".yaml"

    # This application is broken and breaks running
    if i == "io.github.markummitchell.Engauge_Digitizer":
        continue

    # If EOL (but not yet archived), don't count it
    if exists(f'flathub/{i}/flathub.json'):
        with open(f'flathub/{i}/flathub.json', 'r') as json_file:
            flathub_json = json.load(json_file)
            if flathub_json.get('end-of-life'):
                print(f'{i} is not archived but EOL!')
                continue

    # Run flatpak-builder to get a JSON output even if it's a YAML file
    raw_output = subprocess.run(['flatpak-builder', '--show-manifest', f'flathub/{i}/{i}{extension}'], check=True, universal_newlines=True, stdout=subprocess.PIPE)
    output = raw_output.stdout
    manifest = json.loads(output)

    # Check if runtime is valid to avoid extensions cluttering things up
    if not manifest['runtime'] in valid_runtimes:
        continue

    # Make the runtime version to a set of arch based on fsdk supported architectures
    if manifest['runtime-version'] in runtime_versions_1_6:
        available_archs = set(archs_1_6)
    elif manifest['runtime-version'] in runtime_versions_18_08:
        available_archs = set(archs_18_08)
    elif manifest['runtime-version'] in runtime_versions_19_08:
        available_archs = set(archs_19_08)
    elif manifest['runtime-version'] in runtime_versions_20_08:
        available_archs = set(archs_20_08)
    else:
        print(f'{manifest["runtime"]}//{manifest["runtime-version"]} is unsorted')
        continue

    # Check skip-arches
    if exists(f'flathub/{i}/flathub.json'):
        with open(f'flathub/{i}/flathub.json', 'r') as json_file:
            flathub_json = json.load(json_file)
            if flathub_json.get('skip-arches'):
                for arch in flathub_json['skip-arches']:
                    available_archs -= set(flathub_json['skip-arches'])

    # Check only-arches
    if exists(f'flathub/{i}/flathub.json'):
        with open(f'flathub/{i}/flathub.json', 'r') as json_file:
            flathub_json = json.load(json_file)
            if flathub_json.get('only-arches'):
                available_archs &= set(flathub_json['only-arches'])

    # Append number to each arch if available
    for arch in available_archs:
        runtime_information[arch].append(manifest['id'])

# Sort it by version
sorted_runtime_information = {key: order_dict(value) if isinstance(value, dict) else value for key, value in sorted(runtime_information.items())}

# Prettify the JSON
pretty_runtime_information = json.dumps(sorted_runtime_information, indent=4)

# Save data to file based on date
date_prefix = str(date.today()).replace("-","/")

# Make sure folder is there to git clone later
if not os.path.isdir(f'runtime_arch_information/{date_prefix}'):
   os.makedirs(f'runtime_arch_information/{date_prefix}')
with open(f'runtime_arch_information/{date_prefix}/runtime_information.json', 'w') as stats:
    stats.write(pretty_runtime_information)
    stats.close()
