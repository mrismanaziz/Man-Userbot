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
from userbot import LOGS, MAN2, MAN3, MAN4, MAN5, bot
from userbot.clients import man_userbot_on, multiman
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking

try:
    for module_name in ALL_MODULES:
        imported_module = import_module("userbot.modules." + module_name)
    client = multiman()
    total = 5 - client
    LOGS.info(f"Total Clients = {total} User")
    LOGS.info(f"Python Version - {python_version()}")
    LOGS.info(f"Telethon Version - {version.__version__}")
    LOGS.info(f"PyTgCalls Version - {pytgcalls.__version__}")
    LOGS.info(f"Man-Userbot Version - {ubotversion} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
except (ConnectionError, KeyboardInterrupt, NotImplementedError, SystemExit):
    pass
except BaseException as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)


bot.loop.run_until_complete(checking())
bot.loop.run_until_complete(man_userbot_on())
if not BOT_TOKEN:
    bot.loop.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    try:
        bot.disconnect()
    except Exception:
        pass
    try:
        MAN2.disconnect()
    except Exception:
        pass
    try:
        MAN3.disconnect()
    except Exception:
        pass
    try:
        MAN4.disconnect()
    except Exception:
        pass
    try:
        MAN5.disconnect()
    except Exception:
        pass
else:
    try:
        bot.run_until_disconnected()
    except Exception:
        pass
    try:
        MAN2.run_until_disconnected()
    except Exception:
        pass
    try:
        MAN3.run_until_disconnected()
    except Exception:
        pass
    try:
        MAN4.run_until_disconnected()
    except Exception:
        pass
    try:
        MAN5.run_until_disconnected()
    except Exception:
        pass
