# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# FROM Man-Userbot
# t.me/SharingUserbot
#

import pyfiglet

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import deEmojify, edit_delete, man_cmd


@man_cmd(pattern="figlet (\w+) (.+)")
async def figlet(event):
    if event.fwd_from:
        return
    style_list = {
        "slant": "slant",
        "3d": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    style = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    try:
        font = style_list[style]
    except KeyError:
        return await edit_delete(
            event,
            "**Style yang dipilih tidak valid, ketik** `.help figlet` **bila butuh bantuan**",
        )
    result = pyfiglet.figlet_format(deEmojify(text), font=font)
    await event.respond(f"‌‌‎`{result}`")
    await event.delete()


CMD_HELP.update(
    {
        "figlet": f"**Plugin : **`figlet`\
        \n\n  •  **Syntax :** `{cmd}figlet` <style> <text>\
        \n  •  **Function : **Menyesuaikan gaya teks Anda dengan figlet.\
        \n\n  •  **List style :** `slant`, `3d`, `5line`, `alpha`, `banner`, `doh`, `iso`, `letter`, `allig`, `dotm`, `bubble`, `bulb`, `digi`\
    "
    }
)
