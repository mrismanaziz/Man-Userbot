# Man - UserBot
# Copyright (c) 2022 Man-Userbot
# Credits: @mrismanaziz || https://github.com/mrismanaziz
#
# This file is a part of < https://github.com/mrismanaziz/Man-Userbot/ >
# t.me/SharingUserbot & t.me/Lunatic0de

import sys

from telethon.utils import get_peer_id

from userbot import BOT_TOKEN
from userbot import BOT_VER as version
from userbot import (
    DEFAULT,
    DEVS,
    LOGS,
    LOOP,
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
    call_py,
    tgbot,
)
from userbot.modules.gcast import GCAST_BLACKLIST as GBL

EOL = "EOL\nMan-UserBot v{}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"
MSG_BLACKLIST = "MAKANYA GA USAH BERTINGKAH GOBLOK, USERBOT {} GUA MATIIN NAJIS BANGET DIPAKE JAMET KEK LU.\nMan-UserBot v{}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"


async def man_client(client):
    client.me = await client.get_me()
    client.uid = get_peer_id(client.me)


def multiman():
    if 844432220 not in DEVS:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if -1001473548283 not in GBL:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if 844432220 not in DEFAULT:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    failed = 0
    if STRING_SESSION:
        try:
            bot.start()
            call_py.start()
            LOOP.run_until_complete(man_client(bot))
            user = bot.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(
                f"STRING_SESSION detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——"
            )
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e))

    if STRING_2:
        try:
            MAN2.start()
            LOOP.run_until_complete(man_client(MAN2))
            user = MAN2.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_2 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e))

    if STRING_3:
        try:
            MAN3.start()
            LOOP.run_until_complete(man_client(MAN3))
            user = MAN3.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_3 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e))

    if STRING_4:
        try:
            MAN4.start()
            LOOP.run_until_complete(man_client(MAN4))
            user = MAN4.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_4 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e))

    if STRING_5:
        try:
            MAN5.start()
            LOOP.run_until_complete(man_client(MAN5))
            user = MAN5.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_5 detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e))

    if BOT_TOKEN:
        try:
            user = tgbot.get_me()
            name = user.first_name
            uname = user.username
            LOGS.info(
                f"BOT_TOKEN detected!\n┌ First Name: {name}\n└ Username: @{uname}\n——"
            )
        except Exception as e:
            LOGS.info(str(e))

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
