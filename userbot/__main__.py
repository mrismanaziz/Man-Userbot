# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Copyright (C) 2021 TeamUltroid for autobot
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
""" Userbot start point """


import sys
from importlib import import_module
from platform import python_version

from pytgcalls import __version__ as pytgcalls
from pytgcalls import idle
from telethon import version

from userbot import BOT_TOKEN
from userbot import BOT_VER as ubotversion
from userbot import LOGS, bot, tgbot
from userbot.clients import man_userbot_on, multiman
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking


def startup():
    try:
        for module_name in ALL_MODULES:
            import_module(f"userbot.modules.{module_name}")
        client = multiman()
        total = 5 - client
        LOGS.info(f"Total Clients = {total} User")
        LOGS.info(f"Python Version - {python_version()}")
        LOGS.info(f"Telethon Version - {version.__version__}")
        LOGS.info(f"PyTgCalls Version - {pytgcalls.__version__}")
        LOGS.info(f"Man-Userbot Version - {ubotversion} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
        idle()
    except (ConnectionError, KeyboardInterrupt, NotImplementedError, SystemExit):
        pass
    except BaseException as e:
        LOGS.info(str(e), exc_info=True)
        sys.exit(1)


async def activated():
    await checking()
    await man_userbot_on()
    if not BOT_TOKEN:
        await autobot()


bot.loop.run_until_complete(startup())
bot.loop.run_until_complete(activated())
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass
