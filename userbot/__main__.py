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

import asyncio
import sys
from importlib import import_module
from random import randint

from pytgcalls import idle
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest

from userbot import ALIVE_NAME, BOT_TOKEN, BOT_VER, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import LOGS, UPSTREAM_REPO_BRANCH, bot, call_py
from userbot.modules import ALL_MODULES
from userbot.modules.sql_helper.globals import addgvar, gvarstatus

INVALID_PH = (
    "\nERROR: Nomor Telepon yang kamu masukkan SALAH."
    "\nTips: Gunakan Kode Negara beserta nomornya atau periksa nomor telepon Anda dan coba lagi."
)

try:
    bot.start()
    call_py.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(
    f"Jika {ALIVE_NAME} Membutuhkan Bantuan, Silahkan Gabung ke Grup https://t.me/SharingUserbot"
)

LOGS.info(f"Man-Userbot ⚙️ V{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")


async def autobot():
    if gvarstatus("BOT_TOKEN"):
        return
    if BOT_TOKEN:
        return addgvar("BOT_TOKEN", BOT_TOKEN)
    await bot.start()
    await bot.send_message(
        BOTLOG_CHATID, "**SEDANG MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather**"
    )
    who = await bot.get_me()
    name = who.first_name + " Assistant Bot"
    if who.username:
        username = who.username + "_ubot"
    else:
        username = "man" + (str(who.id))[5:] + "ubot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
        )
        sys.exit(1)
    await bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
            )
            sys.exit(1)
    await bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "man" + (str(who.id))[6:] + str(ran) + "ubot"
        await bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            addgvar("BOT_TOKEN", f"{token}")
            addgvar("BOT_USERNAME", f"@{username}")
            await bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, "Search")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_file(bf, "userbot/resources/logo.jpg")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"Managed With ☕️ By {who.first_name}")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(
                bf, f"✨ Owner ~ {who.first_name} ✨\n\n✨ Powered By ~ @Lunatic0de ✨"
            )
            await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [username]))
            await bot.send_message(
                BOTLOG_CHATID,
                f"**BERHASIL MEMBUAT BOT TELEGRAM DENGAN USERNAME @{username}**",
            )
        else:
            LOGS.info(
                "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        addgvar("BOT_TOKEN", f"{token}")
        addgvar("BOT_USERNAME", f"@{username}")
        await bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, "Search")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setuserpic")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_file(bf, "userbot/resources/logo.jpg")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"Managed With ☕️ By {who.first_name}")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setdescription")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(
            bf, f"✨ Owner ~ {who.first_name} ✨\n\n✨ Powered By ~ @Lunatic0de ✨"
        )
        await bot(InviteToChannelRequest(int(BOTLOG_CHATID), [username]))
        await bot.send_message(
            BOTLOG_CHATID,
            f"**BERHASIL MEMBUAT BOT TELEGRAM DENGAN USERNAME @{username}**",
        )
    else:
        LOGS.info(
            "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
        )
        sys.exit(1)


bot.loop.create_task(autobot())


async def man_userbot_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_message(
                BOTLOG_CHATID,
                f"🔥 **Man-Userbot Berhasil Di Aktifkan**\n━━\n➠ **Userbot Version -** `{BOT_VER}@{UPSTREAM_REPO_BRANCH}`\n➠ **Ketik** `{cmd}alive` **untuk Mengecheck Bot**\n━━",
            )
    except Exception as e:
        LOGS.info(str(e))
    # KALO LU NGEFORK LINK CH & GRUP PUNYA GUA NYA JANGAN DI HAPUS YA GOBLOK 😡
    try:
        await bot(JoinChannelRequest("@Lunatic0de"))
        await bot(JoinChannelRequest("@SharingUserbot"))
    except BaseException:
        pass


# JANGAN DI HAPUS GOBLOK 😡 LU COPY/EDIT AJA TINGGAL TAMBAHIN PUNYA LU
# DI HAPUS GUA GBAN YA 🥴 GUA TANDAIN LU AKUN TELENYA 😡
bot.loop.create_task(man_userbot_on())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
