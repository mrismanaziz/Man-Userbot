# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module containing commands for interacting with dogbin(https://del.dog)"""

import os

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils.pastebin import PasteBin


@register(outgoing=True, pattern=r"^\.paste(?: (-d|-n|-h|-k)|$)?(?: ([\s\S]+)|$)")
async def paste(pstl):
    """For .paste command, pastes the text directly to a pastebin."""
    service = pstl.pattern_match.group(1)
    match = pstl.pattern_match.group(2)
    reply_id = pstl.reply_to_msg_id

    if not (match or reply_id):
        return await pstl.edit("`Elon Musk said I cannot paste void.`")

    if match:
        message = match.strip()
    elif reply_id:
        message = await pstl.get_reply_message()
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = message.message

    await pstl.edit("`Pasting text . . .`")
    async with PasteBin(message) as client:
        if service:
            service = service.strip()
            if service not in ["-d", "-n", "-h", "-k"]:
                return await pstl.edit("Invalid flag")
            await client(client.service_match[service])
        else:
            await client.post()

        if client:
            reply_text = (
                "**Pasted successfully!**\n\n"
                f"[URL]({client.link})\n"
                f"[View RAW]({client.raw_link})"
            )
        else:
            reply_text = "**Failed to reach Pastebin Service**"

    await pstl.edit(reply_text, link_preview=False)


CMD_HELP.update(
    {
        "paste": "**Plugin : **`paste`\
        \n\n  •  **Syntax :** `.paste` <text/reply>\
        \n  •  **Function : **Untuk Menyimpan text ke ke layanan pastebin gunakan flags [`-d`, `-n`, `-h`]\
        \n\n  •  **NOTE :** `-d` = **Dogbin** atau `-n` = **Nekobin** atau `-h` = **Hastebin** atau `-k` = **katbin**\
    "
    }
)
