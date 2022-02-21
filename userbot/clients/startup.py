# Man - UserBot
# Copyright (c) 2022 Man-Userbot
# Credits: @mrismanaziz || https://github.com/mrismanaziz
#
# This file is a part of < https://github.com/mrismanaziz/Man-Userbot/ >
# t.me/SharingUserbot & t.me/Lunatic0de

import sys

import telethon.utils
from telethon.tl.functions.channels import InviteToChannelRequest

from userbot import BOT_USERNAME
from userbot import BOT_VER as version
from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import (
    DEFAULT,
    DEVS,
    LOGS,
    MAN2,
    MAN3,
    MAN4,
    MAN5,
    STRING_2,
    STRING_3,
    STRING_4,
    STRING_5,
    STRING_SESSION,
    blacklistman,
    bot,
    branch,
    call_py,
)
from userbot.clients import ITSME
from userbot.modules.gcast import GCAST_BLACKLIST as GBL

EOL = "EOL\nMan-UserBot v{}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"
MSG_BLACKLIST = "MAKANYA GA USAH BERTINGKAH GOBLOK, USERBOT {} GUA MATIIN NAJIS BANGET DIPAKE JAMET KEK LU.\nMan-UserBot v{}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"
MSG_ON = """
🔥 **Man-Userbot Berhasil Di Aktifkan**
━━
➠ **Userbot Version -** `{}@{}`
➠ **Ketik** `{}alive` **untuk Mengecheck Bot**
➠ **Managed By** {}
━━
"""
try:
    user = bot.get_me()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
except BaseException:
    pass


async def man_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


def multiman():
    if ITSME not in DEVS:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if -1001473548283 not in GBL:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if ITSME not in DEFAULT:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    failed = 0
    if STRING_SESSION:
        try:
            bot.start()
            call_py.start()
            bot.loop.run_until_complete(man_client(bot))
            user = bot.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(
                f"STRING_SESSION detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——"
            )
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
            if BOTLOG_CHATID != 0:
                bot.send_message(
                    BOTLOG_CHATID,
                    f"🔥 **Man-Userbot Berhasil Di Aktifkan**\n━━\n➠ **Userbot Version -** `{version}@{branch}`\n➠ **Ketik** `{cmd}alive` **untuk Mengecheck Bot**\n━━",
                )
        except Exception as e:
            LOGS.info(f"{e}")
        try:
            bot(InviteToChannelRequest(int(BOTLOG_CHATID), [BOT_USERNAME]))
        except BaseException:
            pass

    if STRING_2:
        try:
            MAN2.start()
            MAN2.loop.run_until_complete(man_client(MAN2))
            user = MAN2.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_2 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
            if BOTLOG_CHATID != 0:
                MAN2.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd, mention),
                )
        except Exception as e:
            LOGS.info(f"{e}")

    if STRING_3:
        try:
            MAN3.start()
            MAN3.loop.run_until_complete(man_client(MAN3))
            user = MAN3.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_3 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
            if BOTLOG_CHATID != 0:
                MAN3.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd, mention),
                )
        except Exception as e:
            LOGS.info(f"{e}")

    if STRING_4:
        try:
            MAN4.start()
            MAN4.loop.run_until_complete(man_client(MAN4))
            user = MAN4.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_4 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
            if BOTLOG_CHATID != 0:
                MAN4.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd, mention),
                )
        except Exception as e:
            LOGS.info(f"{e}")

    if STRING_5:
        try:
            MAN5.start()
            MAN5.loop.run_until_complete(man_client(MAN5))
            user = MAN5.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_5 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
            if BOTLOG_CHATID != 0:
                MAN5.send_message(
                    BOTLOG_CHATID,
                    MSG_ON.format(version, branch, cmd, mention),
                )
        except Exception as e:
            LOGS.info(f"{e}")

    if not STRING_SESSION:
        failed += 1
    if not STRING_2:
        failed += 1
    if not STRING_3:
        failed += 1
    if not STRING_4:
        failed += 1
    if not STRING_5:
        failed += 1
    return failed
