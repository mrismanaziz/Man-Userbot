# Man - UserBot
# Copyright (c) 2022 Man-Userbot
# Credits: @mrismanaziz || https://github.com/mrismanaziz
#
# This file is a part of < https://github.com/mrismanaziz/Man-Userbot/ >
# t.me/SharingUserbot & t.me/Lunatic0de

from base64 import b64decode

import telethon.utils
from telethon.tl.functions.users import GetFullUserRequest


async def clients_list(SUDO_USERS, bot, MAN2, MAN3, MAN4, MAN5):
    user_ids = list(SUDO_USERS) or []
    main_id = await bot.get_me()
    user_ids.append(main_id.id)

    try:
        if MAN2 is not None:
            id2 = await MAN2.get_me()
            user_ids.append(id2.id)
    except BaseException:
        pass

    try:
        if MAN3 is not None:
            id3 = await MAN3.get_me()
            user_ids.append(id3.id)
    except BaseException:
        pass

    try:
        if MAN4 is not None:
            id4 = await MAN4.get_me()
            user_ids.append(id4.id)
    except BaseException:
        pass

    try:
        if MAN5 is not None:
            id5 = await MAN5.get_me()
            user_ids.append(id5.id)
    except BaseException:
        pass

    return user_ids


ITSME = list(map(int, b64decode("ODQ0NDMyMjIw").split()))


async def client_id(event, botid=None):
    if botid is not None:
        uid = await event.client(GetFullUserRequest(botid))
        OWNER_ID = uid.user.id
        MAN_USER = uid.user.first_name
    else:
        client = await event.client.get_me()
        uid = telethon.utils.get_peer_id(client)
        OWNER_ID = uid
        MAN_USER = client.first_name
    man_mention = f"[{MAN_USER}](tg://user?id={OWNER_ID})"
    return OWNER_ID, MAN_USER, man_mention
