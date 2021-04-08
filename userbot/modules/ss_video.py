# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import os
import time

from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.utils import progress


@register(outgoing=True, pattern=r"^\.ssvideo(?: |$)(.*)")
async def ssvideo(event):
    if not event.reply_to_msg_id:
        await event.edit("`Reply to any media..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`reply to a video..`")
        return
    try:
        frame = int(event.pattern_match.group(1))
        if frame > 10:
            return await event.edit("`hey..dont put that much`")
    except BaseException:
        return await event.edit("`Please input number of frame!`")
    if reply_message.photo:
        return await event.edit("`Hey..this is an image!`")
    if (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        return await event.edit("`Unsupported files..`")
    elif (
        DocumentAttributeFilename(file_name="sticker.webp")
        in reply_message.media.document.attributes
    ):
        return await event.edit("`Unsupported files..`")
    c_time = time.time()
    await event.edit("`Downloading media..`")
    ss = await bot.download_media(
        reply_message,
        "anu.mp4",
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[DOWNLOAD]")
        ),
    )
    try:
        await event.edit("`Proccessing..`")
        command = f"vcsi -g {frame}x{frame} {ss} -o ss.png "
        os.system(command)
        await event.client.send_file(
            event.chat_id,
            "ss.png",
            reply_to=event.reply_to_msg_id,
        )
        await event.delete()
        os.system("rm -rf *.png")
        os.system("rm -rf *.mp4")
    except BaseException as e:
        os.system("rm -rf *.png")
        os.system("rm -rf *.mp4")
        return await event.edit(f"{e}")


CMD_HELP.update(
    {
        "ssvideo": "**Plugin : **`ssvideo`\
        \n\n  •  **Syntax :** `.ssvideo <frame>`\
        \n  •  **Function : **Untuk Screenshot video dari frame per frame\
    "
    }
)
