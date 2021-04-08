# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A Plugin to tagall in the chat for @UniBorg and cmd is `.all`"""

import re

from userbot import CMD_HELP, bot
from userbot.events import register

usernexp = re.compile(r"@(\w{3,32})\[(.+?)\]")
nameexp = re.compile(r"\[([\w\S]+)\]\(tg://user\?id=(\d+)\)\[(.+?)\]")


@register(outgoing=True, pattern="^.all(?: |$)(.*)", disable_errors=True)
async def all(event):
    if event.fwd_from:
        return
    await event.delete()
    query = event.pattern_match.group(1)
    mentions = f"@all {query}"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, 100500):
        mentions += f"[\u2063](tg://user?id={x.id} {query})"
    await bot.send_message(chat, mentions, reply_to=event.message.reply_to_msg_id)


CMD_HELP.update(
    {
        "tag_all": "**Plugin : **`tag_all`\
        \n\n  •  **Syntax :** `.all`\
        \n  •  **Function : **Untuk Mengetag semua anggota yang ada di group.\
    "
    }
)
