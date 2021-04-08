# Copyright (C) 2020 Adek Maulana
#
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
import math

from .tools import humanbytes, time_formatter
from .exceptions import CancelProcess


async def progress(
    current, total, gdrive, start, prog_type, file_name=None, is_cancelled=False
):
    now = time.time()
    diff = now - start
    if is_cancelled is True:
        raise CancelProcess

    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        eta = round((total - current) / speed)
        if "upload" in prog_type.lower():
            status = "Uploading"
        elif "download" in prog_type.lower():
            status = "Downloading"
        else:
            status = "Unknown"
        progress_str = "[{0}{1}] `{2}%`".format(
            "".join("█" for i in range(math.floor(percentage / 10))),
            "".join("░" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )
        tmp = (
            f"{progress_str} - {status}\n"
            f"`Size:` {humanbytes(current)} of {humanbytes(total)}\n"
            f"`Speed:` {humanbytes(speed)}\n"
            f"`ETA:` {time_formatter(eta)}\n"
            f"`Duration:` {time_formatter(elapsed_time)}"
        )
        await gdrive.edit(f"`{prog_type}`\n\n" f"`Status`\n{tmp}")
