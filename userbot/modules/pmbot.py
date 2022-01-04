# Copyright (C) 2021 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
from datetime import datetime
from math import floor

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError
from telethon.utils import get_display_name

from userbot import BOT_USERNAME, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot, tgbot, user
from userbot.modules.sql_helper.bot_blacklists import (
    add_user_to_bl,
    check_is_black_list,
    get_all_bl_users,
    rem_user_from_bl,
)
from userbot.modules.sql_helper.bot_pms_sql import get_user_id
from userbot.modules.sql_helper.bot_starters import (
    del_starter_from_db,
    get_all_starters,
)
from userbot.utils import (
    _format,
    asst_cmd,
    edit_delete,
    edit_or_reply,
    man_cmd,
    reply_id,
    time_formatter,
)
from userbot.utils.logger import logging

LOGS = logging.getLogger(__name__)

botusername = BOT_USERNAME
OWNER_ID = user.id
OWNER = user.first_name
FINISHED_PROGRESS_STR = "●"
UNFINISHED_PROGRESS_STR = "○"


async def get_user_and_reason(event):
    id_reason = event.pattern_match.group(1)
    replied = await reply_id(event)
    user_id, reason = None, None
    if replied:
        users = get_user_id(replied)
        if users is not None:
            for usr in users:
                user_id = int(usr.chat_id)
                break
            reason = id_reason
    elif id_reason:
        data = id_reason.split(maxsplit=1)
        if len(data) == 2:
            user, reason = data
        elif len(data) == 1:
            user = data[0]
        if user.isdigit():
            user_id = int(user)
        if user.startswith("@"):
            user_id = user
    return user_id, reason


# taken from
# https://github.com/code-rgb/USERGE-X/blob/f95766027ef95854d05e523b42cd158c2e8cdbd0/userge/plugins/bot/bot_forwards.py#L420
def progress_str(total: int, current: int) -> str:
    percentage = current * 100 / total
    prog_arg = "**Progress** : `{}%`\n" "```[{}{}]```"
    return prog_arg.format(
        percentage,
        "".join((FINISHED_PROGRESS_STR for i in range(floor(percentage / 5)))),
        "".join((UNFINISHED_PROGRESS_STR for i in range(20 - floor(percentage / 5)))),
    )


async def ban_user_from_bot(user, reason, reply_to=None):
    try:
        date = str(datetime.now().strftime("%B %d, %Y"))
        add_user_to_bl(user.id, get_display_name(user), user.username, reason, date)
    except Exception as e:
        LOGS.error(str(e))
    banned_msg = f"**Anda Telah Dibanned dari Bot ini.\nKarena:** `{reason}`"
    await tgbot.send_message(user.id, banned_msg)
    info = f"**#Banned_Bot_PM_User**\
            \n**First Name:** {_format.mentionuser(get_display_name(user) , user.id)}\
            \n**User ID:** `{user.id}`\
            \n**Reason:** `{reason}`"
    if BOTLOG_CHATID:
        await bot.send_message(BOTLOG_CHATID, info)
    return info


async def unban_user_from_bot(user, reason, reply_to=None):
    try:
        rem_user_from_bl(user.id)
    except Exception as e:
        LOGS.error(str(e))
    banned_msg = "**Anda Telah diunbanned dari Bot ini.**"

    if reason is not None:
        banned_msg += f"\n**Karena:** {reason}"
    await tgbot.send_message(user.id, banned_msg)
    info = f"**#Unbanned_Bot_PM_User**\
            \n**First Name:** {_format.mentionuser(get_display_name(user) , user.id)}\
            \n**User ID:** `{user.id}`"
    if BOTLOG_CHATID:
        await bot.send_message(BOTLOG_CHATID, info)
    return info


@asst_cmd(pattern="^/broadcast$", from_users=OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**Mohon Balas Ke Pesan Yang ingin di Broadcast!**")
    start_ = datetime.now()
    br_cast = await replied.reply("`Broadcasting...`")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("**Belum ada yang memulai bot Anda.** 🥺")
    users = get_all_starters()
    if users is None:
        return await event.reply("**Terjadi Error saat mengambil daftar pengguna.**")
    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "🔊 You received a **new** Broadcast."
            )
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**Terjadi Error Saat Broadcast**\n`{e}`"
                )

        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "🔊 **Broadcasting...**\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️ **Berhasil** :  `{count}`\n"
                        + f"• ✖️ **Gagal** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"🔊 <b>Berhasil Mengirim Broadcast Pesan Ke</b> ➜ <code>{count}</code> <b>Users.</b>"
    if blocked_users:
        b_info += f"\n🚫 <code>{len(blocked_users)}</code> <b>user memblokir bot Anda baru-baru ini, jadi telah dihapus.</b>"
    b_info += f"\n⏳ <b>Dalam Waktu</b>  <code>{time_formatter((end_ - start_).seconds)}</code>."
    await br_cast.edit(b_info, parse_mode="html")


@man_cmd(pattern="botuser$")
async def bot_user(event):
    "To get list of users who started bot."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "**Belum ada yang memulai bot Anda.** 🥺")
    msg = "**Daftar Pengguna yang Memulai Bot Anda adalah:\n\n**"
    for user in ulist:
        msg += f"• **First Name:** {_format.mentionuser(user.first_name , user.user_id)}\n**User ID:** `{user.user_id}`\n**Tanggal: **{user.date}\n\n"
    await edit_or_reply(event, msg)


@asst_cmd(pattern="^/ban\\s+([\\s\\S]*)", from_users=OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id,
            "**Saya tidak dapat menemukan user untuk dibanned**",
            reply_to=reply_to,
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id,
            "**Untuk Membanned User mohon Berikan alasan terlebih dahulu**",
            reply_to=reply_to,
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**ERROR:**\n`{e}`")
    if user_id == OWNER_ID:
        return await event.reply("**Saya Tidak Bisa Membanned Master** 🥺")
    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"**#Already_Banned**\
            \n**Pengguna sudah ada di Daftar Banned saya.**\
            \n**Alasan diBanned:** `{check.reason}`\
            \n**Tanggal:** `{check.date}`",
        )
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@asst_cmd(pattern="^/unban(?:\\s|$)([\\s\\S]*)", from_users=OWNER_ID)
async def unban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id,
            "**Saya tidak dapat menemukan pengguna untuk di unbanned**",
            reply_to=reply_to,
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**Error:**\n`{e}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"**#User_Not_Banned**\
            \n• {_format.mentionuser(user.first_name , user.id)} **Tidak ada di List Banned saya.**",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@man_cmd(pattern="bblist$")
async def listban_bot(event):
    "To get list of users who are banned in bot."
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "**Belum ada yang dibanned di bot Anda.**")
    msg = "**Daftar Pengguna Yang diBanned di Bot Anda adalah:\n\n**"
    for user in ulist:
        msg += f"• **Nama:** {_format.mentionuser(user.first_name , user.chat_id)}\n**User ID:** `{user.chat_id}`\n**Tanggal: **{user.date}\n**Karena:** {user.reason}\n\n"
    await edit_or_reply(event, msg)


@asst_cmd(pattern="^/uinfo$", from_users=OWNER_ID)
async def bot_uinfo(event):
    reply_to = await reply_id(event)
    if not reply_to:
        return await event.reply(
            "**Silahkan Balas ke pesan untuk mendapatkan info pesan**"
        )
    info_msg = await event.client.send_message(
        event.chat_id,
        "`🔎 Sedang Mencari di Database...`",
        reply_to=reply_to,
    )
    users = get_user_id(reply_to)
    if users is None:
        return await info_msg.edit(
            "**ERROR: Maaf! Tidak Dapat Menemukan pengguna ini di database saya 🥺**"
        )
    for usr in users:
        user_id = int(usr.chat_id)
        user_name = usr.first_name
        break
    if user_id is None:
        return await info_msg.edit(
            "**ERROR: Maaf! Tidak Dapat Menemukan pengguna ini di database saya 🥺**"
        )
    uinfo = f"**Pesan ini dikirim oleh**\
            \n**First Name:** {_format.mentionuser(user_name , user_id)}\
            \n**User ID:** `{user_id}`"
    await info_msg.edit(uinfo)


@man_cmd(pattern="(set|reset) pmbot(?: |$)(\\w*)")
async def setpmbot(event):
    try:
        import userbot.modules.sql_helper.globals as sql
    except AttributeError:
        await event.edit("**Running on Non-SQL mode!**")
        return
    xnxx = await edit_or_reply(event, "`Processing...`")
    conf = event.pattern_match.group(1)
    custom_message = sql.gvarstatus("START_TEXT")
    if conf.lower() == "set":
        message = await event.get_reply_message()
        status = "Pesan"
        if custom_message is not None:
            sql.delgvar("START_TEXT")
            status = "Pesan"
        if not message:
            return await xnxx.edit("**Mohon Reply Ke Pesan**")
        msg = message.message
        sql.addgvar("START_TEXT", msg)
        await xnxx.edit("**Berhasil Mengcustom Pesan Start BOT**")
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**{status} PMBOT Yang Tersimpan:** \n\n{msg}",
            )
    if conf.lower() == "reset":
        if custom_message is not None:
            sql.delgvar("START_TEXT")
        await edit_delete(xnxx, "**Berhasil Menghapus Pesan Custom PMBOT**")


CMD_HELP.update(
    {
        "pmbot": f"**Plugin : **`pmbot`\
        \n\n  •  **Syntax :** `{cmd}bblist`\
        \n  •  **Function : **Untuk Melihat Daftar pengguna yang dibanned di bot anda.\
        \n\n  •  **Syntax :** `{cmd}botuser`\
        \n  •  **Function : **Untuk Melihat Daftar Pengguna yang Memulai Bot anda.\
        \n\n  •  **Syntax :** `{cmd}set pmbot` <balas ke pesan>\
        \n  •  **Function : **Mengcustom Pesan start pmbot.\
        \n\n  •  **Syntax :** `{cmd}reset pmbot`\
        \n  •  **Function : **Mengembalikan Custom Start PMBOT menjadi default.\
    "
    }
)
