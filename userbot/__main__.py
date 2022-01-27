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

import requests
from pytgcalls import idle
from telethon.tl.functions.channels import InviteToChannelRequest

from userbot import (
    LOGS,
    MAN2,
    MAN3,
    MAN4,
    MAN5,
    MAN6,
    MAN7,
    MAN8,
    MAN9,
    MAN10,
    STRING_2,
    STRING_3,
    STRING_4,
    STRING_5,
    STRING_6,
    STRING_7,
    STRING_8,
    STRING_9,
    STRING_10,
    STRING_SESSION,
    bot,
)
from userbot import BOT_TOKEN, BOT_USERNAME, BOT_VER, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import DEVS, LOGS, bot, branch, call_py
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, checking


async def man_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


def multiman():
    if STRING_SESSION:
        LOGS.info("STRING_1 detected! Starting 1st Client.")
        try:
            bot.start()
            call_py.start()
            bot.loop.run_until_complete(man_client(bot))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_1 Not Found")

    if STRING_2:
        LOGS.info("STRING_2 detected! Starting 2nd Client.")
        try:
            MAN2.start()
            MAN2.loop.run_until_complete(man_client(MAN2))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_2 Not Found")

    if STRING_3:
        LOGS.info("STRING_3 detected! Starting 3rd Client.")
        try:
            MAN3.start()
            MAN3.loop.run_until_complete(man_client(MAN3))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_3 Not Found")

    if STRING_4:
        LOGS.info("STRING_4 detected! Starting 4th Client.")
        try:
            MAN4.start()
            MAN4.loop.run_until_complete(man_client(MAN4))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_4 Not Found")

    if STRING_5:
        LOGS.info("STRING_5 detected! Starting 5th Client.")
        try:
            MAN5.start()
            MAN5.loop.run_until_complete(man_client(MAN5))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_5 Not Found")

    if STRING_6:
        LOGS.info("STRING_6 detected! Starting 6th Client.")
        try:
            MAN6.start()
            MAN6.loop.run_until_complete(man_client(MAN6))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_6 Not Found")

    if STRING_7:
        LOGS.info("STRING_7 detected! Starting 7th Client.")
        try:
            MAN7.start()
            MAN7.loop.run_until_complete(man_client(MAN7))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_7 Not Found")

    if STRING_8:
        LOGS.info("STRING_8 detected! Starting 8th Client.")
        try:
            MAN8.start()
            MAN8.loop.run_until_complete(man_client(MAN8))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_8 Not Found")

    if STRING_9:
        LOGS.info("STRING_9 detected! Starting 9th Client.")
        try:
            MAN9.start()
            MAN9.loop.run_until_complete(man_client(MAN9))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_9 Not Found")

    if STRING_10:
        LOGS.info("STRING_10 detected! Starting 10th Client.")
        try:
            MAN10.start()
            MAN10.loop.run_until_complete(man_client(MAN10))
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_10 Not Found")

try:
    client = multiman()
    user = bot.get_me()
    blacklistman = requests.get(
        "https://raw.githubusercontent.com/mrismanaziz/Reforestation/master/manblacklist.json"
    ).json()
    if user.id in blacklistman:
        LOGS.warning(
            "MAKANYA GA USAH BERTINGKAH GOBLOK, USERBOTnya GUA MATIIN NAJIS BANGET DIPAKE JAMET KEK LU.\nCredits: @mrismanaziz"
        )
        sys.exit(1)
    if 844432220 not in DEVS:
        LOGS.warning(
            f"EOL\nMan-UserBot v{BOT_VER}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"
        )
        sys.exit(1)
except Exception as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(
    f"Jika {user.first_name} Membutuhkan Bantuan, Silahkan Tanyakan di Grup https://t.me/SharingUserbot"
)

LOGS.info(f"Man-Userbot ⚙️ V{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")


async def man_userbot_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_message(
                BOTLOG_CHATID,
                f"🔥 **Man-Userbot Berhasil Di Aktifkan**\n━━\n➠ **Userbot Version -** `{BOT_VER}@{branch}`\n➠ **Ketik** `{cmd}alive` **untuk Mengecheck Bot**\n━━",
            )
    except Exception as e:
        LOGS.info(str(e))
    try:
        await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
    except BaseException:
        pass


bot.loop.run_until_complete(checking())
bot.loop.run_until_complete(man_userbot_on())
if not BOT_TOKEN:
    bot.loop.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
