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
date_prefix = str(date.today()).replace("-","/")
if Path(f'runtime_arch_information/{date_prefix}/runtime_information.json').is_file():
    print("Here are today's runtime numbers!")
else:
    date_prefix = str(date.today() - timedelta(days = 1)).replace("-","/")
    print("Here are yesterday's runtime numbers!")

with open(f'runtime_arch_information/{date_prefix}/runtime_information.json', 'r') as raw_stats:
    stats = json.load(raw_stats)

    # Print numbers of each architectures
    print()
    for arch in stats:
        print(f'{arch:<8} : {len(stats[arch]):<4}')

