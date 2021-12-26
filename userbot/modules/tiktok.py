# Copyright (C) 2020 Frizzy.
# All rights reserved.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# Lord Userbot

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, edit_or_reply, man_cmd

# Alvin Gans


@man_cmd(pattern="tiktok(?: |$)(.*)")
async def _(event):
    xxnx = event.pattern_match.group(1)
    if xxnx:
        d_link = xxnx
    elif event.is_reply:
        d_link = await event.get_reply_message()
    else:
        return await edit_delete(
            event,
            "**Berikan Link Tiktok Pesan atau Reply Link Tiktok Untuk di Download**",
        )
    xx = await edit_or_reply(event, "`Video Sedang Diproses...`")
    chat = "@thisvidbot"
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.send_message(d_link)
            video = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message("/start")
            await conv.send_message(d_link)
            video = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(event.chat_id, video)
        await event.client(DeleteHistoryRequest(peer=chat, max_id=0))
        await xx.delete()


CMD_HELP.update(
    {
        "tiktok": f"**Plugin : **`tiktok`\
        \n\n  •  **Syntax :** `{cmd}tiktok` <link>\
        \n  •  **Function : **Download Video Tiktok Tanpa Watermark\
    "
    }
)
