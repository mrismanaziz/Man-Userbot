# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import time

from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import bash, edit_or_reply, man_cmd, progress


@man_cmd(pattern="ssvideo(?: |$)(.*)")
async def ssvideo(event):
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "`Reply to any media..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "`reply to a video..`")
        return
    try:
        frame = int(event.pattern_match.group(1))
        if frame > 10:
            return await edit_or_reply(event, "`hey..dont put that much`")
    except BaseException:
        return await edit_or_reply(event, "`Please input number of frame!`")
    if reply_message.photo:
        return await edit_or_reply(event, "`Hey..this is an image!`")
    if (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        return await edit_or_reply(event, "`Unsupported files..`")
    if (
        DocumentAttributeFilename(file_name="sticker.webp")
        in reply_message.media.document.attributes
    ):
        return await edit_or_reply(event, "`Unsupported files..`")
    c_time = time.time()
    await edit_or_reply(event, "`Downloading media..`")
    ss = await event.client.download_media(
        reply_message,
        "anu.mp4",
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[DOWNLOAD]")
        ),
    )
    try:
        await edit_or_reply(event, "`Proccessing..`")
        command = f"vcsi -g {frame}x{frame} {ss} -o ss.png "
        await bash(command)
        await event.client.send_file(
            event.chat_id,
            "ss.png",
            reply_to=event.reply_to_msg_id,
        )
        await event.delete()
        await bash("rm -rf *.png")
        await bash("rm -rf *.mp4")
    except BaseException as e:
        await bash("rm -rf *.png")
        await bash("rm -rf *.mp4")
        return await edit_or_reply(event, f"{e}")


CMD_HELP.update(
    {
        "ssvideo": f"**Plugin : **`ssvideo`\
        \n\n  •  **Syntax :** `{cmd}ssvideo <frame>`\
        \n  •  **Function : **Untuk Screenshot video dari frame per frame\
    "
    }
)
