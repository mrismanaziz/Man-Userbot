# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port from UniBorg to Userbot by yincen17

import asyncio
import os
import time
import zipfile
from datetime import date

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, ZIP_DOWNLOAD_DIRECTORY
from userbot.utils import man_cmd, progress

# ====================
today = date.today()
# ====================


@man_cmd(pattern="compress(?: |$)(.*)")
async def _(event):
    # Prevent Channel Bug to use update
    if event.is_channel and not event.is_group:
        await event.edit("`Compress Command isn't permitted on channels`")
        return
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("`Reply to a file to compress it.`")
        return
    mone = await event.edit("`Processing...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "[DOWNLOADING]")
                ),
            )
            directory_name = downloaded_file_name
            await event.edit(
                f"Downloaded to `{directory_name}`" "`\ncompressing file...`"
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED).write(
        directory_name
    )
    c_time = time.time()
    await event.client.send_file(
        event.chat_id,
        directory_name + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, mone, c_time, "[UPLOADING]")
        ),
    )
    await event.edit("`Done!!`")
    await asyncio.sleep(7)
    await event.delete()


@man_cmd(pattern="addzip(?: |$)(.*)")
async def addzip(add):
    """Copyright (c) 2020 azrim @github"""
    # Prevent Channel Bug to use update
    if add.is_channel and not add.is_group:
        await add.edit("`Command isn't permitted on channels`")
        return
    if add.fwd_from:
        return
    if not add.is_reply:
        await add.edit("`Reply to a file to compress it.`")
        return
    mone = await add.edit("`Processing...`")
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        os.makedirs(ZIP_DOWNLOAD_DIRECTORY)
    if add.reply_to_msg_id:
        reply_message = await add.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await add.client.download_media(
                reply_message,
                ZIP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "[DOWNLOADING]")
                ),
            )
            success = str(downloaded_file_name).replace("./zips/", "")
            await add.edit(f"`{success} Successfully added to list`")
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
            return


@man_cmd(pattern=r"upzip(?: |$)(.*)")
async def upload_zip(up):
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        await up.edit("`Files not found`")
        return
    mone = await up.edit("`Zipping File...`")
    input_str = up.pattern_match.group(1)
    curdate = today.strftime("%m%d%y")
    title = str(input_str) if input_str else "zipfile" + f"{curdate}"
    zipf = zipfile.ZipFile(title + ".zip", "w", zipfile.ZIP_DEFLATED)
    zipdir(ZIP_DOWNLOAD_DIRECTORY, zipf)
    zipf.close()
    c_time = time.time()
    await up.client.send_file(
        up.chat_id,
        title + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=up.message.id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, mone, c_time, "[UPLOADING]", input_str)
        ),
    )
    os.rmdir(ZIP_DOWNLOAD_DIRECTORY)
    await up.delete()


@man_cmd(pattern=r"rmzip(?: |$)(.*)")
async def remove_dir(rm):
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        await rm.edit("`Directory not found`")
        return
    os.rmdir(ZIP_DOWNLOAD_DIRECTORY)
    await rm.edit("`Zip list removed`")


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


CMD_HELP.update(
    {
        "zipfile": f"**Plugin : **`zipfile`\
        \n\n  •  **Syntax :** `{cmd}compress` **[optional: <reply to file>]**\
        \n  •  **Function : **make files to zip.\
        \n\n  •  **Syntax :** `{cmd}addzip` **<reply to file>**\
        \n  •  **Function : **add files to zip list.\
        \n\n  •  **Syntax :** `{cmd}upzip` **[optional: <zip title>]**\
        \n  •  **Function : **upload zip list.\
        \n\n  •  **Syntax :** `{cmd}rmzip` **[optional: <zip title>]**\
        \n  •  **Function : **clear zip list.\
    "
    }
)
