# Credits: @mrismanaziz || https://github.com/mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import sys

import requests
import telethon.utils

from userbot import BOT_VER as version
from userbot import (
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
    bot,
    call_py,
)

while 0 < 6:
    _BLACKLIST = requests.get(
        "https://raw.githubusercontent.com/mrismanaziz/Reforestation/master/manblacklist.json"
    )
    if _BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        blacklistman = []
        break
    blacklistman = _BLACKLIST.json()
    break

del _BLACKLIST

MSG_BLACKLIST = "MAKANYA GA USAH BERTINGKAH GOBLOK, USERBOT {} GUA MATIIN NAJIS BANGET DIPAKE JAMET KEK LU.\nMan-UserBot v{}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"


async def man_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


def multiman():
    if 844432220 not in DEVS:
        LOGS.warning(
            f"EOL\nMan-UserBot v{version}, Copyright © 2021-2022 ʀɪsᴍᴀɴ• <https://github.com/mrismanaziz>"
        )
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
            LOGS.info(f"STRING_SESSION detected!\n┌ First Name: {name}\n└ User ID: {uid}")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_1 Not Found")

    if STRING_2:
        try:
            MAN2.start()
            MAN2.loop.run_until_complete(man_client(MAN2))
            user = MAN2.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_2 detected!\n┌ First Name: {name}\n└ User ID: {uid}")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_2 Not Found")

    if STRING_3:
        try:
            MAN3.start()
            MAN3.loop.run_until_complete(man_client(MAN3))
            user = MAN3.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_3 detected!\n┌ First Name: {name}\n└ User ID: {uid}")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_3 Not Found")

    if STRING_4:
        try:
            MAN4.start()
            MAN4.loop.run_until_complete(man_client(MAN4))
            user = MAN4.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_4 detected!\n┌ First Name: {name}\n└ User ID: {uid}")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_4 Not Found")

    if STRING_5:
        try:
            MAN5.start()
            MAN5.loop.run_until_complete(man_client(MAN5))
            user = MAN5.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(f"STRING_5 detected!\n┌ First Name: {name}\n└ User ID: {uid}")
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            print(e)
    else:
        LOGS.info("STRING_5 Not Found")

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
