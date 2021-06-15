# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import asyncio
import errno
import json
import math
import multiprocessing
import os
import re
import time
from asyncio import create_subprocess_shell as asyncSubprocess
from asyncio.subprocess import PIPE as asyncPIPE
from urllib.error import HTTPError

from pySmartDL import SmartDL

from userbot import CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.modules.google_drive import create_app, get_mimeType, upload
from userbot.utils import humanbytes, time_formatter
from userbot.utils.exceptions import CancelProcess


async def subprocess_run(megadl, cmd):
    subproc = await asyncSubprocess(cmd, stdout=asyncPIPE, stderr=asyncPIPE)
    stdout, stderr = await subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        await megadl.edit(
            "**Terdeteksi Error saat Menjalankan Subproses.**\n"
            f"exitCode : `{exitCode}`\n"
            f"stdout : `{stdout.decode().strip()}`\n"
            f"stderr : `{stderr.decode().strip()}`"
        )
        return exitCode
    return stdout.decode().strip(), stderr.decode().strip(), exitCode


@register(outgoing=True, pattern=r"^\.mega(?: |$)(.*)")
async def mega_downloader(megadl):
    await megadl.edit("`Mengumpulkan informasi...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    msg_link = await megadl.get_reply_message()
    link = megadl.pattern_match.group(1)
    if link:
        pass
    elif msg_link:
        link = msg_link.text
        link_msg_id = msg_link.id
    else:
        return await megadl.edit("Usage: `.mega` **<MEGA.nz link>**")
    try:
        link = re.findall(r"\bhttps?://.*mega.*\.nz\S+", link)[0]
        """ - Mega changed their URL again - """
        if "file" in link:
            link = link.replace("#", "!").replace("file/", "#!")
        elif "folder" in link or "#F" in link or "#N" in link:
            await megadl.edit("`Folder Download dihapus...`")
            return
    except IndexError:
        await megadl.edit("`MEGA.nz link Tidak Ditemukan...`")
        return None
    cmd = f"bin/megadown -q -m {link}"
    result = await subprocess_run(megadl, cmd)
    try:
        data = json.loads(result[0])
    except json.JSONDecodeError:
        await megadl.edit("**JSONDecodeError**: `Gagal Mengekstrak Link...`")
        return None
    except (IndexError, TypeError):
        return
    file_name = data["file_name"]
    file_url = data["url"]
    hex_key = data["hex_key"]
    hex_raw_key = data["hex_raw_key"]
    temp_file_name = file_name + ".temp"
    temp_file_path = TEMP_DOWNLOAD_DIRECTORY + temp_file_name
    file_path = TEMP_DOWNLOAD_DIRECTORY + file_name
    mimeType = await get_mimeType(file_path)
    service = await create_app(megadl)
    if service is False:
        return None
    if os.path.isfile(file_path):
        try:
            raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), file_path)
        except FileExistsError as e:
            await megadl.edit(f"`{str(e)}`")
            return None
    downloader = SmartDL(file_url, temp_file_path, progress_bar=False)
    display_message = None
    try:
        downloader.start(blocking=False)
    except HTTPError as e:
        await megadl.edit(f"**HTTPError**: `{str(e)}`")
        return None
    start = time.time()
    while not downloader.isFinished():
        status = downloader.get_status().capitalize()
        total_length = downloader.filesize or None
        downloaded = downloader.get_dl_size()
        percentage = int(downloader.get_progress() * 100)
        speed = downloader.get_speed(human=True)
        estimated_total_time = round(downloader.get_eta())
        progress_str = "`{0}` | [{1}{2}] `{3}%`".format(
            status,
            "".join("●" for i in range(math.floor(percentage / 10))),
            "".join("○" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        diff = time.time() - start
        try:
            current_message = (
                f"`{file_name}`\n\n"
                "Status\n"
                f"{progress_str}\n"
                f"`{humanbytes(downloaded)} of {humanbytes(total_length)}"
                f" @ {speed}`\n"
                f"`ETA` -> {time_formatter(estimated_total_time)}\n"
                f"`Duration` -> {time_formatter(round(diff))}"
            )
            if round(diff % 15.00) == 0 and (
                display_message != current_message or total_length == downloaded
            ):
                await megadl.edit(current_message)
                await asyncio.sleep(0.2)
                display_message = current_message
        except Exception:
            pass
        finally:
            if status == "Combining":
                wait = round(downloader.get_eta())
                await asyncio.sleep(wait)
    if downloader.isSuccessful():
        download_time = round(downloader.get_dl_time() + wait)
        try:
            P = multiprocessing.Process(
                target=await decrypt_file(
                    megadl, file_path, temp_file_path, hex_key, hex_raw_key
                ),
                name="Decrypt_File",
            )
            P.start()
            P.join()
        except FileNotFoundError as e:
            await megadl.edit(f"`{str(e)}`")
            return None
        else:
            await megadl.edit(
                f"`{file_name}`\n\n"
                f"Berhasil didownload di: '`{file_path}`'.\n"
                f"Download took: {time_formatter(download_time)}.",
            )

        try:
            resultgd = await upload(megadl, service, file_path, file_name, mimeType)
        except CancelProcess:
            megadl.respond(
                "`[FILE - CANCELLED]`\n\n"
                "`Status` : **OK** - Sinyal yang diterima dibatalkan."
            )
        if resultgd:
            if msg_link:
                await megadl.respond(
                    "`[FILE - UPLOAD]`\n\n"
                    f"`Name   :` `{file_name}`\n"
                    f"`Size   :` `{humanbytes(resultgd[0])}`\n"
                    f"`Link   :` [{file_name}]({resultgd[1]})\n"
                    "`Status :` **OK** - Berhasil diupload.\n",
                    link_preview=False,
                    reply_to=link_msg_id,
                )
                await megadl.delete()
            elif link:
                await megadl.respond(
                    "`[FILE - UPLOAD]`\n\n"
                    f"`Name   :` `{file_name}`\n"
                    f"`Size   :` `{humanbytes(resultgd[0])}`\n"
                    f"`Link   :` [{file_name}]({resultgd[1]})\n"
                    "`Status :` **OK** - Berhasil diupload.\n",
                    link_preview=False,
                )
                await megadl.delete()

        if os.path.exists(file_path):
            os.remove(file_path)
    else:
        await megadl.edit(
            "`Gagal Mendownload, " "Check Log heroku untuk lebih jelasnya.`"
        )
        for e in downloader.get_errors():
            LOGS.info(str(e))
    return


async def decrypt_file(megadl, file_path, temp_file_path, hex_key, hex_raw_key):
    cmd = "cat '{}' | openssl enc -d -aes-128-ctr -K {} -iv {} > '{}'".format(
        temp_file_path, hex_key, hex_raw_key, file_path
    )
    if await subprocess_run(megadl, cmd):
        os.remove(temp_file_path)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    return


CMD_HELP.update(
    {
        "mega": "**Plugin : **`mega`\
        \n\n  •  **Syntax :** `.mega` <MEGA.nz link>\
        \n  •  **Function : **Balas link MEGA.nz atau salin tautan MEGA.nz Anda ke download file server userbot Anda.\
    "
    }
)
