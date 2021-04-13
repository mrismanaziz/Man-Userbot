# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

import math
import os
from asyncio import sleep
from subprocess import PIPE, Popen

import aria2p
from requests import get

from userbot import CMD_HELP, LOGS, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils import humanbytes


def subprocess_run(cmd):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        print(
            "An error was detected while running the subprocess:\n"
            f"exit code: {exitCode}\n"
            f"stdout: {talk[0]}\n"
            f"stderr: {talk[1]}"
        )
    return talk


# Get best trackers for improved download speeds, thanks K-E-N-W-A-Y.
trackers_list = get(
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
).text.replace("\n\n", ",")
trackers = f"[{trackers_list}]"

cmd = f"aria2c \
--allow-overwrite=true \
--bt-max-peers=0 \
--bt-tracker={trackers} \
--check-certificate=false \
--daemon=true \
--enable-rpc \
--follow-torrent=mem \
--max-concurrent-downloads=5 \
--max-connection-per-server=10 \
--max-upload-limit=1K \
--min-split-size=10M \
--rpc-listen-all=false \
--rpc-listen-port 8210 \
--rpc-max-request-size=1024M \
--seed-time=0.01 \
--split=10 \
"

subprocess_run(cmd)

if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
    os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

download_path = os.getcwd() + TEMP_DOWNLOAD_DIRECTORY.strip(".")
if not download_path.endswith("/"):
    download_path += "/"

aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=8210, secret=""))

aria2.set_global_options({"dir": download_path})


@register(outgoing=True, pattern=r"^\.amag(?: |$)(.*)")
async def magnet_download(event):
    magnet_uri = event.pattern_match.group(1)
    # Add Magnet URI Into Queue
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        return await event.edit(f"**Error:**\n`{e}`")
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    await sleep(15)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=event, previous=None)


@register(outgoing=True, pattern=r"^\.ator(?: |$)(.*)")
async def torrent_download(event):
    torrent_file_path = event.pattern_match.group(1)
    # Add Torrent Into Queue
    try:
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None
        )
    except Exception as e:
        return await event.edit(f"**Error:**\n`{e}`")
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)


@register(outgoing=True, pattern=r"^\.aurl(?: |$)(.*)")
async def aurl_download(event):
    uri = [event.pattern_match.group(1)]
    try:  # Add URL Into Queue
        download = aria2.add_uris(uri, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        return await event.edit(f"**Error:**\n`{e}`")
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, event=event, previous=None)


@register(outgoing=True, pattern=r"^\.aclear(?: |$)(.*)")
async def remove_all(event):
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except Exception:
        pass
    if not removed:  # If API returns False Try to Remove Through System Call.
        subprocess_run("aria2p remove-all")
    await event.edit("`Clearing on-going downloads...`")
    await sleep(2.5)
    await event.edit("`Successfully cleared all downloads.`")


@register(outgoing=True, pattern=r"^\.apause(?: |$)(.*)")
async def pause_all(event):
    # Pause ALL Currently Running Downloads.
    await event.edit("`Pausing downloads...`")
    aria2.pause_all(force=True)
    await sleep(2.5)
    await event.edit("`Successfully paused on-going downloads.`")


@register(outgoing=True, pattern=r"^\.aresume(?: |$)(.*)")
async def resume_all(event):
    await event.edit("`Resuming downloads...`")
    aria2.resume_all()
    await sleep(1)
    await event.edit("`Resumed downloads.`")
    await sleep(2.5)
    await event.delete()


@register(outgoing=True, pattern=r"^\.ashow(?: |$)(.*)")
async def show_all(event):
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = (
            msg
            + "File: `"
            + str(download.name)
            + "`\nSpeed: "
            + str(download.download_speed_string())
            + "\nProgress: "
            + str(download.progress_string())
            + "\nTotal Size: "
            + str(download.total_length_string())
            + "\nStatus: "
            + str(download.status)
            + "\nETA:  "
            + str(download.eta_string())
            + "\n\n"
        )
    if len(msg) <= 4096:
        await event.edit("**On-going Downloads:**\n" + msg)
        await sleep(5)
    else:
        await event.edit("`Output is too big, sending it as a file...`")
        output = "output.txt"
        with open(output, "w") as f:
            f.write(msg)
        await sleep(2)
        await event.client.send_file(
            event.chat_id,
            output,
            reply_to=event.message.id,
        )

    await event.delete()


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    LOGS.info("Changing GID " + gid + " to" + new_gid)
    return new_gid


async def check_progress_for_dl(gid, event, previous):
    complete = None
    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            if complete or file.error_message:
                await event.edit(f"`{msg}`")
            else:
                percentage = int(file.progress)
                downloaded = percentage * int(file.total_length) / 100
                prog_str = "**Downloading:** `[{}{}]` **{}**".format(
                    "".join("●" for _ in range(math.floor(percentage / 10))),
                    "".join("○" for _ in range(10 - math.floor(percentage / 10))),
                    file.progress_string(),
                )

                msg = (
                    f"**Name:** `{file.name}`\n"
                    f"**Status:** {file.status.capitalize()}\n"
                    f"{prog_str}\n"
                    f"{humanbytes(downloaded)} of {file.total_length_string()}"
                    f" @ {file.download_speed_string()}\n"
                    f"**ETA:** {file.eta_string()}\n"
                )
                if msg != previous:
                    await event.edit(msg)
                    msg = previous
            await sleep(15)
            await check_progress_for_dl(gid, event, previous)
            file = aria2.get_download(gid)
            complete = file.is_complete
            if complete:
                return await event.edit(
                    "**Downloaded successfully!**\n\n"
                    f"**Name:** `{file.name}`\n"
                    f"**Size:** {file.total_length_string()}\n"
                    f"**Path:** `{TEMP_DOWNLOAD_DIRECTORY + file.name}`\n"
                )
        except Exception as e:
            if " not found" in str(e) or "'file'" in str(e):
                await event.edit(f"**Download canceled:**\n`{file.name}`")
                await sleep(2.5)
                return await event.delete()
            if " depth exceeded" in str(e):
                file.remove(force=True)
                await event.edit(
                    f"**Download cancelled automatically:**\n`{file.name}`\n**Given link/torrent is dead.**"
                )


CMD_HELP.update(
    {
        "aria": "**Plugin : **`aria`\
        \n\n  •  **Syntax :** `.aurl [URL]` (or) >`.amag [Magnet Link]` (or) >`.ator [path to torrent file]`\
        \n  •  **Function : **Downloads the file into your userbot server storage.\
        \n\n  •  **Syntax :** `.apause` (or) `.aresume`\
        \n  •  **Function : **Pauses/resumes on-going downloads.\
        \n\n  •  **Syntax :** `.aclear`\
        \n  •  **Function : **Clears the download queue, deleting all on-going downloads.\
        \n\n  •  **Syntax :** `.ashow`\
        \n  •  **Function : **Shows progress of the on-going downloads.\
    "
    }
)
