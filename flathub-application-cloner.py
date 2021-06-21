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

import fnmatch
import json
import os
import requests
import shutil
import subprocess
from pathlib import Path

# Make sure folder is there to git clone later
if not Path("flathub").is_dir():
    os.makedirs("flathub")

# Patterns are here to be easy to change in the future
package_pattern = ["*.*.*", "*.*.*.*", "*.*.*.*.*", "*.*.*.*.*"]
not_application_pattern = [
    "org.kde.PlatformTheme.*",
    "org.gtk.Gtk3theme.*",
    "org.kde.KStyle.*",
    "org.kde.PlatformInputContexts.*",
    "org.kde.WaylandDecoration.*",
    "org.freedesktop.Platform.*",
    "org.freedesktop.Sdk.*",
    "*.*.BaseApp",
    "*.*.*.BaseApp",
]

# Ask info about flathub repo to make the number of pages
response = requests.get("https://api.github.com/orgs/flathub")
flathub_info = response.json()

if flathub_info["public_repos"] % 100 > 0:
    nbPage = int((flathub_info["public_repos"] / 100) + 1)
else:
    nbPage = int(flathub_info["public_repos"] / 100)

# For every page of 100repos in Flathub
for i in range(nbPage):
    url = f"https://api.github.com/orgs/flathub/repos?per_page=100&page={i}"

    # Grab the JSON of the page
    response = requests.get(url)
    page = response.json()

    # For each repo in a package, do filtering and clone or pull appropriately
    for repo in page:

        repo_url = f"{repo['html_url']}.git"
        repo_name = repo["name"]

        # Value to check to see if inner loop is bad
        inner_loop_detected = False

        # If repo is archived, skip
        if repo["archived"]:
            print(repo_name + " is EOL, skipping...")
            if Path(f"flathub/{repo_name}").is_dir():
                shutil.rmtree(f"flathub/{repo_name}")
            continue

        # If repo is not in *.*.* format, it's not a package
        if not repo_name.count(".") >= 2:
            print(repo_name + " is not a package, skipping...")
            inner_loop_detected = True
            continue

        # If a repo matches one of these patterns, it's not an application
        # It may be icons or themes
        for pattern in not_application_pattern:
            if fnmatch.fnmatch(repo_name, pattern):
                print(repo_name + " is not an application, skipping...")
                inner_loop_detected = True
                break
        if inner_loop_detected:
            continue

        # If folder exists then try pulling.
        # If it doesn't then clone.
        if Path(f"flathub/{repo_name}").is_dir():
            print(repo_name + " is already cloned, pulling...")
            subprocess.run([f"( cd flathub/{repo_name}; git pull )"], shell=True)
            if Path(f"flathub/{repo_name}/.gitmodules").is_file():
                subprocess.run([f"( cd flathub/{repo_name}; git submodule update )"], shell=True)
        else:
            subprocess.run(
                [f"git clone --recursive --depth=1 {repo_url} flathub/{repo_name}"],
                shell=True,
            )
