# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="hentai(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@nHentaiBot"
    xx = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=424466890)
            )
            await event.client.send_message(chat, link)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await event.client.send_message(chat, link)
            response = await response
        if response.text.startswith("**Sorry I couldn't get manga from**"):
            await xx.edit("**Saya pikir ini bukan link yang benar**")
        else:
            await xx.delete()
            await event.client.send_message(event.chat_id, response.message)


CMD_HELP.update(
    {
        "hentai": f"**Plugin : **`hentai`\
        \n\n  •  **Syntax :** `{cmd}hentai` <link nhentai>\
        \n  •  **Function : **Melihat nhentai di telegra.ph XD\
    "
    }
)
