# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing userid, chatid and log commands"""

from asyncio import sleep
from datetime import datetime
from math import sqrt

from emoji import emojize
from telethon import functions
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    MessageActionChannelMigrateFrom,
)
from telethon.utils import get_input_location

from userbot import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event


@register(outgoing=True, pattern=r"^\.userid$")
async def useridgetter(target):
    """For .userid command, returns the ID of the target user."""
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit(f"**Username:** {name} \n**User ID:** `{user_id}`")


@register(outgoing=True, pattern=r"^\.link(?: |$)(.*)")
async def permalink(mention):
    """For .link command, generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = (
            user.first_name.replace("\u2060", "") if user.first_name else user.username
        )
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern=r"^\.getbot(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Bot Di Channel Ini:** \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Bot Dalam {} Channel: \n".format(input_str)
        try:
            chat = await bot.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in bot.iter_participants(chat, filter=ChannelParticipantsBots):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.edit(mentions)


@register(outgoing=True, pattern=r"^\.log(?: |$)([\s\S]*)")
async def log(log_text):
    """For .log command, forwards a message or the command argument to the bot logs group"""
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"**#LOG** / **Chat ID:** {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            return await log_text.edit("**Apa yang harus saya log?**")
        await log_text.edit("**Berhasil disimpan di Group Log**")
    else:
        await log_text.edit("**Fitur Ini Mengharuskan Loging Diaktifkan!**")
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern=r"^\.kickme$")
async def kickme(leave):
    """Basically it's .kickme command"""
    await leave.edit(f"`{ALIVE_NAME} has left this group, bye!!`")
    await leave.client.kick_participant(leave.chat_id, "me")


@register(outgoing=True, pattern=r"^\.kikme$")
async def kickme(leave):
    """Basically it's .kickme command"""
    await leave.edit("**GC NYA JELEK GOBLOK KELUAR DULU AH CROTT** 🥴")
    await leave.client.kick_participant(leave.chat_id, "me")


@register(outgoing=True, pattern=r"^\.unmutechat$")
async def unmute_chat(unm_e):
    """For .unmutechat command, unmute a muted chat."""
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        return await unm_e.edit("**Running on Non-SQL Mode!**")
    unkread(str(unm_e.chat_id))
    await unm_e.edit("**Berhasil Dibuka, Obrolan Tidak Lagi Dibisukan!**")
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern=r"^\.mutechat$")
async def mute_chat(mute_e):
    """For .mutechat command, mute any chat."""
    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        return await mute_e.edit("**Running on Non-SQL mode!**")
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit(f"**{ALIVE_NAME} Telah Membisukan Obrolan!**")
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID, str(mute_e.chat_id) + " Telah Dibisukan."
        )


@register(incoming=True, disable_errors=True)
async def keep_read(message):
    """The mute logic."""
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)


@register(outgoing=True, pattern=r"^s/")
async def sedNinja(event):
    """For regex-ninja module, auto delete command starting with s/"""
    try:
        from userbot.modules.sql_helper.globals import gvarstatus
    except AttributeError:
        return await event.edit("**Running on Non-SQL mode!**")
    if gvarstatus("regexNinja"):
        await event.delete()


@register(outgoing=True, pattern=r"^\.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """Enables or disables the regex ninja module."""
    if event.pattern_match.group(1) == "on":
        try:
            from userbot.modules.sql_helper.globals import addgvar
        except AttributeError:
            return await event.edit("**Running on Non-SQL mode!**")
        addgvar("regexNinja", True)
        await event.edit("**Berhasil Mengaktifkan Mode Regez Ninja.**")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        try:
            from userbot.modules.sql_helper.globals import delgvar
        except AttributeError:
            return await event.edit("**Running on Non-SQL mode!**")
        delgvar("regexNinja")
        await event.edit("**Berhasil Menonaktifkan Mode Regez Ninja.**")
        await sleep(1)
        await event.delete()


@register(pattern=r"^\.chatinfo(?: |$)(.*)", outgoing=True)
async def info(event):
    await event.edit("`Menganalisis Obrolan Ini...`")
    chat = await get_chatinfo(event)
    caption = await fetch_info(chat, event)
    try:
        await event.edit(caption, parse_mode="html")
    except Exception as e:
        print("Exception:", e)
        await event.edit("**Terjadi Kesalah Yang Tidak Terduga.**")
    return


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await event.reply(
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Invalid channel/group`")
            return None
    return chat_info


async def fetch_info(chat, event):
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    # Same for msg_info.users
    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Akun Terhapus"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception as e:
        dc_id = "Unknown"
        str(e)

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "Tidak"
    )
    slowmode = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "Tidak"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "Tidak"
    )
    verified = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "Tidak"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for _ in bots_list:
            bots += 1

    caption = "<b>INFORMASI OBROLAN:</b>\n"
    caption += f"ID: <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"{chat_type} Nama: {chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"Nama Lama: {former_title}\n"
    if username is not None:
        caption += f"{chat_type} Type: Publik\n"
        caption += f"Link: {username}\n"
    else:
        caption += f"{chat_type} type: Privasi\n"
    if creator_username is not None:
        caption += f"Pembuat: {creator_username}\n"
    elif creator_valid:
        caption += (
            f'Pembuat: <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"Informasi Pembuatan: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"Informasi Pembuatan: <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"Data Centre ID: {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"{chat_type} Level: <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"Pesan Yang Dapat Dilihat: <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"Pesan Dikirim: <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"Pesan Dikirim: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"Member: <code>{members}</code>\n"
    if admins is not None:
        caption += f"Admin: <code>{admins}</code>\n"
    if bots_list:
        caption += f"Bot: <code>{bots}</code>\n"
    if members_online:
        caption += f"Sedang Online: <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"Pengguna Yang Dibatasi: <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"Banned Pengguna: <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'{chat_type} Sticker: <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"Mode Slow: {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
        caption += f"Supergrup: {supergroup}\n\n"
    if hasattr(chat_obj_info, "Terbatas"):
        caption += f"Terbatas: {restricted}\n"
        if chat_obj_info.restricted:
            caption += f"> Platform: {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> Alasan: {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> Teks: {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "Scam: <b>Yes</b>\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"Di Verifikasi Oleh Telegram: {verified}\n\n"
    if description:
        caption += f"Deskripsi: \n<code>{description}</code>\n"
    return caption


@register(outgoing=True, pattern=r"^\.invite(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` users to a chat, not to a Private Message")
    else:
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split():
                try:
                    if user_id.isdigit():
                        user_id = int(user_id)
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    return await event.edit(str(e))
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split():
                try:
                    if user_id.isdigit():
                        user_id = int(user_id)
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    return await event.edit(str(e))

        await event.edit("`Invited Successfully`")
        await sleep(3)
        await event.delete()


# inviteall Ported By @VckyouuBitch
# From Geez - Projects <https://github.com/vckyou/Geez-UserBot>
# Copyright © Team Geez - Project


@register(outgoing=True, pattern=r"^\.inviteall(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if sender.id != me.id:
        man = await event.reply("`Processing...`")
    else:
        man = await event.edit("`Processing...`")
    manuserbot = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await man.edit("**Maaf, tidak bisa menambahkan pengguna di sini**")
    s = 0
    f = 0
    error = "None"

    await man.edit("**Terminal Status**\n\n`Sedang Mengumpulkan Pengguna...`")
    async for user in event.client.iter_participants(manuserbot.full_chat.id):
        try:
            if error.startswith("Too"):
                return await man.edit(
                    f"**Terminal Finished With Error**\n(**Mungkin Mendapat Limit dari telethon Silakan coba lagi Nanti**)\n**Error** : \n`{error}`\n\n• Menambahkan `{s}` orang \n• Gagal Menambahkan `{f}` orang"
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s += 1
            await man.edit(
                f"**Terminal Running...**\n\n• **Menambahkan** `{s}` **orang** \n• **Gagal Menambahkan** `{f}` **orang**\n\n**× LastError:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f += 1
    return await man.edit(
        f"**Terminal Finished** \n\n• **Berhasil Menambahkan** `{s}` **orang** \n• **Gagal Menambahkan** `{f}` **orang**"
    )


CMD_HELP.update(
    {
        "chat": "**Plugin : **`chat`\
        \n\n  •  **Syntax :** `.userid`\
        \n  •  **Function : **untuk Mengambil ID obrolan saat ini\
        \n\n  •  **Syntax :** `.getbot`\
        \n  •  **Function : **Dapatkan List Bot dalam grup caht.\
        \n\n  •  **Syntax :** `.log`\
        \n  •  **Function : **Meneruskan pesan yang Anda balas di grup log bot Anda.\
        \n\n  •  **Syntax :** `.mutechat`\
        \n  •  **Function : **membisukan Grup chat (membutuhkan hak admin).\
        \n\n  •  **Syntax :** `.unmutechat`\
        \n  •  **Function : **Membuka Grup chat yang dibisukan (membutuhkan hak admin).\
        \n\n  •  **Syntax :** `.getbot`\
        \n  •  **Function : **Dapatkan List Bot dalam grup caht.\
        \n\n  •  **Syntax :** `.chatinfo [opsional: <reply/tag/chat id/invite link>]`\
        \n  •  **Function : **Mendapatkan info obrolan. Beberapa info mungkin dibatasi karena izin yang hilang.\
    "
    }
)


CMD_HELP.update(
    {
        "invite": "**Plugin : **`invite`\
        \n\n  •  **Syntax :** `.invite` <username/user id>\
        \n  •  **Function : **Untuk Menambahkan/invite pengguna ke group chat.\
        \n\n  •  **Syntax :** `.inviteall`\
        \n  •  **Function : **Untuk Menambahkan/invite pengguna dari yang chat kita ke group chat.\
    "
    }
)


CMD_HELP.update(
    {
        "kickme": "**Plugin : **`kickme`\
        \n\n  •  **Syntax :** `.kickme`\
        \n  •  **Function : **Keluar grup dengan menampilkan pesan Master has left this group, bye!!\
        \n\n  •  **Syntax :** `.leave`\
        \n  •  **Function : **Keluar grup dengan menampilkan pesan Master Telah Meninggalkan Grup, bye !!\
        \n\n  •  **Syntax :** `.kikme`\
        \n  •  **Function : **Keluar grup dengan menampilkan pesan GC NYA JELEK GOBLOK KELUAR DULU AH CROTT 🥴\
    "
    }
)


CMD_HELP.update(
    {
        "link": "**Plugin : **`link`\
        \n\n  •  **Syntax :** `.link` <username/userid> <opsional teks> (atau) Reply pesan .link <teks opsional>\
        \n  •  **Function : **Membuat link permanen ke profil pengguna dengan teks ubahsuaian opsional.\
        \n  •  **Contoh : **.link @mrismanaziz Ganteng\
    "
    }
)


CMD_HELP.update(
    {
        "regexninja": "**Plugin : **`regexninja`\
        \n\n  •  **Syntax :** `regexninja on`\
        \n  •  **Function : **Mengaktifkan modul ninja regex secara global. \
        \n\n  •  **Syntax :** `regexninja off`)\
        \n  •  **Function : **Menonaktifkan modul ninja regex secara global. \
        \n\n  •  **NOTE :** Modul Regex Ninja dapat membantu menghapus pesan pemicu bot regex.\
    "
    }
)
