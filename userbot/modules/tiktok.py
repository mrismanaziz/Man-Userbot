# Copyright (C) 2020 Frizzy.
# All rights reserved.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# Lord Userbot

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register

# Alvin Gans


@register(outgoing=True, pattern="^.tiktok(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit(
            "`Berikan Link Video Tiktok Untuk Download Video Tiktok` **(._.)**"
        )
    else:
        await event.edit("```Video Sedang Diproses.....```")
    chat = "@ttsavebot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit(
                "**Error:** `Mohon Buka Blokir` @ttsavebot `Dan Coba Lagi!`"
            )
            return
        await bot.send_file(event.chat_id, video)
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, r.id, msg.id, details.id, video.id]
        )
        await event.delete()


CMD_HELP.update(
    {
        "tiktok": "**Plugin : **`tiktok`\
        \n\n  •  **Syntax :** `.tiktok` <link>\
        \n  •  **Function : **Download Video Tiktok Tanpa Watermark\
    "
    }
)
