# Copyright (c) 2021 Man-Userbot
# Created by mrismanaziz
# FROM <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
# Thanks To Ultroid <https://github.com/TeamUltroid/Ultroid>
# Thanks To Geez-UserBot <https://github.com/vckyou/Geez-UserBot>

import os
from asyncio import sleep

from telethon import events
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChannelParticipantsKicked

from userbot import ALIVE_NAME, bot
from userbot.events import register
from userbot.utils import edit_delete, edit_or_reply


@register(outgoing=True, pattern=r"^\.open(?: |$)(.*)")
async def _(event):
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    a = await event.reply("**Berkas Sudah Dibaca...**")
    if len(c) > 4095:
        await a.edit("**File Terlalu Panjang Untuk dibaca**")
    else:
        await event.client.send_message(event.chat_id, f"`{c}`")
        await a.delete()
    os.remove(b)


@register(outgoing=True, pattern=r"^\.sendbot (.*)")
async def sendbot(event):
    if event.fwd_from:
        return
    chat = str(event.pattern_match.group(1).split(" ", 1)[0])
    link = str(event.pattern_match.group(1).split(" ", 1)[1])
    if not link:
        return await event.edit("**Maaf BOT Tidak Merespond.**")

    botid = await event.client.get_entity(chat)
    await event.edit("`Processing...`")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=botid)
            )
            msg = await bot.send_message(chat, link)
            response = await response
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply(f"**Unblock Terlebih dahulu {chat} dan coba lagi.**")
            return
        except BaseException:
            await event.edit("**Tidak dapat menemukan bot itu 🥺**")
            await sleep(2)
            return await event.delete()

        await event.edit(f"**Pesan Terkirim:** `{link}`\n**Kepada: {chat}**")
        await bot.send_message(event.chat_id, response.message)
        await bot.send_read_acknowledge(event.chat_id)
        await event.client.delete_messages(conv.chat_id, [msg.id, response.id])


@register(outgoing=True, groups_only=True, pattern=r"^\.unbanall$")
async def _(event):
    await event.edit("`Searching Participant Lists...`")
    p = 0
    title = (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except BaseException:
            pass
    await event.edit(f"**Berhasil unbanned** `{p}` **Orang di Grup {title}**")


@register(outgoing=True, pattern=r"^\.(?:dm)\s?(.*)?")
async def dm(event):
    p = event.pattern_match.group(1)
    m = p.split(" ")
    chat_id = m[0]
    try:
        chat_id = int(chat_id)
    except BaseException:
        pass
    msg = ""
    mssg = await event.get_reply_message()
    if event.reply_to_msg_id:
        await event.client.send_message(chat_id, mssg)
        await event.edit("**Berhasil Mengirim Pesan Anda.**")
    for i in m[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await event.client.send_message(chat_id, msg)
        await event.edit("**Berhasil Mengirim Pesan Anda.**")
    except BaseException:
        await event.edit("**ERROR: Gagal Mengirim Pesan.**")


@register(outgoing=True, pattern=r"^\.fwdreply ?(.*)")
async def _(e):
    message = e.pattern_match.group(1)
    if not e.reply_to_msg_id:
        return await edit_or_reply(e, "`Mohon Reply ke pesan seseorang.`")
    if not message:
        return await edit_or_reply(e, "`Tidak ditemukan pesan untuk disampaikan`")
    msg = await e.get_reply_message()
    fwd = await msg.forward_to(msg.sender_id)
    await fwd.reply(message)
    await edit_delete(e, "**Check in Private**", 15)


@register(outgoing=True, pattern=r"^\.getlink(?: |$)(.*)", groups_only=True)
async def _(event):
    await event.edit("`Processing...`")
    try:
        e = await event.client(
            ExportChatInviteRequest(event.chat_id),
        )
    except ChatAdminRequiredError:
        return await bot.send_message(f"**Maaf {ALIVE_NAME} Bukan Admin 👮**")
        sleep(15)
        await event.delete()
    await event.edit(f"**Link Invite GC**: {e.link}")


@register(outgoing=True, pattern=r"^\.tmsg (.*)")
async def _(event):
    k = await event.get_reply_message()
    if k:
        a = await bot.get_messages(event.chat_id, 0, from_user=k.sender_id)
        return await event.edit(
            f"**Total ada** `{a.total}` **Chat Yang dikirim Oleh** {u} **di Grup Chat ini**"
        )
    u = event.pattern_match.group(1)
    if not u:
        u = "me"
    a = await bot.get_messages(event.chat_id, 0, from_user=u)
    await event.edit(
        f"**Total ada `{a.total}` Chat Yang dikirim Oleh saya di Grup Chat ini**"
    )


CMD_HELP.update(
    {
        "open": "**Plugin : **`open`\
        \n\n  •  **Syntax :** `.open`\
        \n  •  **Function : **Untuk Melihat isi File Menjadi Text yang dikirim menjadi pesan telegram.\
    "
    }
)


CMD_HELP.update(
    {
        "dm": "**Plugin : **`dm`\
        \n\n  •  **Syntax :** `.dm` <username> <text>\
        \n  •  **Function : **Untuk mengirim chat dengan menggunakan userbot.\
        \n\n  •  **Syntax :** `.fwdreply` <username> <text>\
        \n  •  **Function : **Untuk meneruskan chat yang di reply dengan membalasnya ke pc.\
    "
    }
)


CMD_HELP.update(
    {
        "sendbot": "**Plugin : **`sendbot`\
        \n\n  •  **Syntax :** `.sendbot` <username bot> <text>\
        \n  •  **Function : **Untuk mengirim ke bot dan mendapatkan respond chat dengan menggunakan userbot.\
    "
    }
)


CMD_HELP.update(
    {
        "tmsg": "**Plugin : **`tmsg`\
        \n\n  •  **Syntax :** `.tmsg` <username/me>\
        \n  •  **Function : **Untuk Menghitung total jumlah chat yang sudah dikirim.\
    "
    }
)


CMD_HELP.update(
    {
        "getlink": "**Plugin : **`getlink`\
        \n\n  •  **Syntax :** `.getlink`\
        \n  •  **Function : **Untuk Mendapatkan link invite grup chat.\
    "
    }
)


CMD_HELP.update(
    {
        "unbanall": "**Plugin : **`unbanall`\
        \n\n  •  **Syntax :** `.unbanall`\
        \n  •  **Function : **Untuk Menghapus Semua Pengguna yang dibanned di Daftar Banned GC.\
    "
    }
)
