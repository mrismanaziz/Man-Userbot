# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

import asyncio

from userbot import CHANNEL
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, ICON_HELP, bot
from userbot.events import man_cmd

modules = CMD_HELP


@bot.on(man_cmd(pattern="help(?: |$)(.*)", outgoing=True))
async def help(event):
    """For help command"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(f"`{args}` **Bukan Nama Modul yang Valid.**")
            await asyncio.sleep(15)
            await event.delete()
    else:
        user = await bot.get_me()
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += f"`\t\t\t{ICON_HELP}\t\t\t"
        await event.edit(
            f"**✦ Daftar Perintah Untuk [Man-Userbot](https://github.com/mrismanaziz/Man-Userbot):**\n"
            f"**✦ Jumlah** `{len(modules)}` **Modules**\n"
            f"**✦ Owner:** [{user.first_name}](tg://user?id={user.id})\n\n"
            f"{ICON_HELP}   {string}"
            f"\n\nSupport @{CHANNEL}",
        )
        await event.reply(
            f"\n**Contoh Ketik** `{cmd}help afk` **Untuk Melihat Informasi Module**"
        )
