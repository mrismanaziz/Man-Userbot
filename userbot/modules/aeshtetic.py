# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Ported for Lord-Userbot By liualvinas/Alvin

from telethon import events

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd

PRINTABLE_ASCII = range(0x21, 0x7F)


def aesthetify(string):
    for c in string:
        c = ord(c)
        if c in PRINTABLE_ASCII:
            c += 0xFF00 - 0x20
        elif c == ord(" "):
            c = 0x3000
        yield chr(c)


@bot.on(man_cmd(outgoing=True, pattern="ae(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    text = event.pattern_match.group(1)
    text = "".join(aesthetify(text))
    await event.edit(text=text, parse_mode=None, link_preview=False)
    raise events.StopPropagation


CMD_HELP.update(
    {
        "aeshtetic": f"**Plugin : **`aeshtetic`\
        \n\n  •  **Syntax :** `{cmd}ae <teks>`\
        \n  •  **Function : **Mengubah font teks Menjadi aeshtetic.\
    "
    }
)
