# Copyright (C) 2021 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils import _format, edit_delete, edit_or_reply


@register(outgoing=True, pattern=r"^\.sg(u)?(?:\s|$)([\s\S]*)")
async def _(event):
    "To get name/username history."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(event, "**Mohon Reply Ke Pesan Pengguna.**", 90)
    user, rank = await get_user_from_event(event, secondgroup=True)
    if not user:
        return
    uid = user.id
    chat = "@SangMataInfo_bot"
    manevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await edit_delete(
                manevent, "**Unblock** @sangmatainfo_bot **Dan Coba Lagi**", 120
            )
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(manevent, "**Orang Ini Belum Pernah Mengganti Namanya**", 90)
    if "No records found" in responses:
        await edit_delete(manevent, "**Orang Ini Belum Pernah Mengganti Namanya**", 90)
    names, usernames = await sangamata_seperator(responses)
    cmd = event.pattern_match.group(1)
    risman = None
    check = usernames if cmd == "u" else names
    for i in check:
        if risman:
            await event.reply(i, parse_mode=_format.parse_pre)
        else:
            risman = True
            await manevent.edit(i, parse_mode=_format.parse_pre)


async def get_user_from_event(
    event, manevent=None, secondgroup=None, nogroup=False, noedits=False
):
    if manevent is None:
        manevent = event
    if nogroup is False:
        if secondgroup:
            args = event.pattern_match.group(2).split(" ", 1)
        else:
            args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    try:
        if args:
            user = args[0]
            if len(args) > 1:
                extra = "".join(args[1:])
            if user.isnumeric() or (user.startswith("-") and user[1:].isnumeric()):
                user = int(user)
            if event.message.entities:
                probable_user_mention_entity = event.message.entities[0]
                if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                    user_id = probable_user_mention_entity.user_id
                    user_obj = await event.client.get_entity(user_id)
                    return user_obj, extra
            if isinstance(user, int) or user.startswith("@"):
                user_obj = await event.client.get_entity(user)
                return user_obj, extra
    except Exception as e:
        LOGS.error(str(e))
    try:
        if nogroup is False:
            if secondgroup:
                extra = event.pattern_match.group(2)
            else:
                extra = event.pattern_match.group(1)
        if event.is_private:
            user_obj = await event.get_chat()
            return user_obj, extra
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            if previous_message.from_id is None:
                if not noedits:
                    await edit_delete(
                        manevent, "**ERROR: Dia adalah anonymous admin!**", 60
                    )
                return None, None
            user_obj = await event.client.get_entity(previous_message.sender_id)
            return user_obj, extra
        if not args:
            if not noedits:
                await edit_delete(
                    manevent,
                    "**Berikan Username, user id, atau reply pesan pengguna!**",
                    60,
                )
            return None, None
    except Exception as e:
        LOGS.error(str(e))
    if not noedits:
        await edit_delete(
            manevent, "**ERROR:** __Gagal Mendapatkan history nama orang ini__", 30
        )
    return None, None


async def sangamata_seperator(sanga_list):
    for i in sanga_list:
        if i.startswith("🔗"):
            sanga_list.remove(i)
    s = 0
    for i in sanga_list:
        if i.startswith("Username History"):
            break
        s += 1
    usernames = sanga_list[s:]
    names = sanga_list[:s]
    return names, usernames


CMD_HELP.update(
    {
        "sangmata": "**Plugin : **`sangmata`\
        \n\n  •  **Syntax :** `.sg` <sambil reply chat>\
        \n  •  **Function : **Mendapatkan Riwayat Nama Pengguna selama di telegram.\
        \n\n  •  **Syntax :** `.sgu` <sambil reply chat>\
        \n  •  **Function : **Mendapatkan Riwayat Username Pengguna selama di telegram.\
    "
    }
)
