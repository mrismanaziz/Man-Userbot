# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for keeping control who PM you."""

from sqlalchemy.exc import IntegrityError
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User

from userbot import (
    ALIVE_NAME,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    COUNT_PM,
    LASTMSG,
    LOGS,
    PM_AUTO_BAN,
)
from userbot.events import register

# ========================= CONSTANTS ============================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

DEF_UNAPPROVED_MSG = (
    f"__**ROOM CHAT || {DEFAULTUSER}**__\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    f"__HALLO SELAMAT DATANG, SAYA ADALAH BOT YANG MENJAGA ROOM CHAT INI MOHON JANGAN MELAKUKAN SPAM KARNA SAYA OTOMATIS AKAN MEMBLOKIR ANDA, TUNGGU SAMPAI {DEFAULTUSER} MENERIMA PESAN ANDA__\n"
    "┏━━━━━━━━━━━━━━━━━━━\n"
    "┣[• `PESAN OTOMATIS`\n"
    "┣[• `BY MAN-USERBOT`\n"
    "┗━━━━━━━━━━━━━━━━━━━"
)
# =================================================================


@register(incoming=True, disable_edited=True, disable_errors=True)
async def permitpm(event):
    """Prohibits people from PMing you without approval. \
        Will block retarded nibbas automatically."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not (await event.get_sender()).bot
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import is_approved
        except AttributeError:
            return
        apprv = is_approved(event.chat_id)
        notifsoff = gvarstatus("NOTIF_OFF")

        # Use user custom unapproved message
        getmsg = gvarstatus("unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

        # This part basically is a sanity check
        # If the message that sent before is Unapproved Message
        # then stop sending it again to prevent FloodHit
        if not apprv and event.text != UNAPPROVED_MSG:
            if event.chat_id in LASTMSG:
                prevmsg = LASTMSG[event.chat_id]
                # If the message doesn't same as previous one
                # Send the Unapproved Message again
                if event.text != prevmsg:
                    async for message in event.client.iter_messages(
                        event.chat_id, from_user="me", search=UNAPPROVED_MSG
                    ):
                        await message.delete()
                    await event.reply(f"{UNAPPROVED_MSG}")
            else:
                await event.reply(f"{UNAPPROVED_MSG}")
            LASTMSG.update({event.chat_id: event.text})
            if notifsoff:
                await event.client.send_read_acknowledge(event.chat_id)
            if event.chat_id not in COUNT_PM:
                COUNT_PM.update({event.chat_id: 1})
            else:
                COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

            if COUNT_PM[event.chat_id] > 4:
                await event.respond(
                    "`Anda Telah Di Blokir Karna Melakukan Spam Pesan`\n"
                    "`Ke Room Chat Lord`"
                )

                try:
                    del COUNT_PM[event.chat_id]
                    del LASTMSG[event.chat_id]
                except KeyError:
                    if BOTLOG:
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "Lord, Terjadi Masalah Saat Menghitung Private Message, Mohon Restart Bot!",
                        )
                    return LOGS.info("CountPM wen't rarted boi")

                await event.client(BlockRequest(event.chat_id))
                await event.client(ReportSpamRequest(peer=event.chat_id))

                if BOTLOG:
                    name = await event.client.get_entity(event.chat_id)
                    name0 = str(name.first_name)
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "["
                        + name0
                        + "](tg://user?id="
                        + str(event.chat_id)
                        + ")"
                        + " Telah Diblokir Karna Melakukan Spam Ke Room Chat",
                    )


@register(disable_edited=True, outgoing=True, disable_errors=True)
async def auto_accept(event):
    """Will approve automatically if you texted them first."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not (await event.get_sender()).bot
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import approve, is_approved
        except AttributeError:
            return

        # Use user custom unapproved message
        get_message = gvarstatus("unapproved_msg")
        if get_message is not None:
            UNAPPROVED_MSG = get_message
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

        chat = await event.get_chat()
        if isinstance(chat, User):
            if is_approved(event.chat_id) or chat.bot:
                return
            async for message in event.client.iter_messages(
                event.chat_id, reverse=True, limit=1
            ):
                if (
                    message.text is not UNAPPROVED_MSG
                    and message.from_id == self_user.id
                ):
                    try:
                        approve(event.chat_id)
                    except IntegrityError:
                        return

                if is_approved(event.chat_id) and BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#AUTO-APPROVED\n"
                        + "Pengguna: "
                        + f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@register(outgoing=True, pattern=r"^\.notifoff$")
async def notifoff(noff_event):
    """For .notifoff command, stop getting notifications from unapproved PMs."""
    try:
        from userbot.modules.sql_helper.globals import addgvar
    except AttributeError:
        return await noff_event.edit("`Running on Non-SQL mode!`")
    addgvar("NOTIF_OFF", True)
    await noff_event.edit(
        "`Notifikasi Dari Pesan Pribadi Tidak Disetujui, Telah Dibisukan!`"
    )


@register(outgoing=True, pattern=r"^\.notifon$")
async def notifon(non_event):
    """For .notifoff command, get notifications from unapproved PMs."""
    try:
        from userbot.modules.sql_helper.globals import delgvar
    except AttributeError:
        return await non_event.edit("`Running on Non-SQL mode!`")
    delgvar("NOTIF_OFF")
    await non_event.edit(
        "`Notifikasi Dari Pesan Pribadi Tidak Disetujui, Tidak Lagi Dibisukan!`"
    )


@register(outgoing=True, pattern=r"^\.(?:setuju|ok)\s?(.)?")
async def approvepm(apprvpm):
    """For .ok command, give someone the permissions to PM you."""
    try:
        from userbot.modules.sql_helper.globals import gvarstatus
        from userbot.modules.sql_helper.pm_permit_sql import approve
    except AttributeError:
        return await apprvpm.edit("`Running on Non-SQL mode!`")

    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        replied_user = await apprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id

    else:
        aname = await apprvpm.client.get_entity(apprvpm.chat_id)
        name0 = str(aname.first_name)
        uid = apprvpm.chat_id

    # Get user custom msg
    getmsg = gvarstatus("unapproved_msg")
    if getmsg is not None:
        UNAPPROVED_MSG = getmsg
    else:
        UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

    async for message in apprvpm.client.iter_messages(
        apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG
    ):
        await message.delete()

    try:
        approve(uid)
    except IntegrityError:
        return await apprvpm.edit("`Oke Pesan Anda Sudah Diterima`")

    await apprvpm.edit(
        f"`Hai` [{name0}](tg://user?id={uid}) `Pesan Anda Sudah Diterima`"
    )
    await apprvpm.delete(getmsg)
    await message.delete()

    if BOTLOG:
        await apprvpm.client.send_message(
            BOTLOG_CHATID, "#DITERIMA\n" + "User: " + f"[{name0}](tg://user?id={uid})"
        )


@register(outgoing=True, pattern=r"^\.(?:tolak|nopm)\s?(.)?")
async def disapprovepm(disapprvpm):
    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove
    except BaseException:
        return await disapprvpm.edit("`Running on Non-SQL mode!`")

    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        dissprove(aname)
    else:
        dissprove(disapprvpm.chat_id)
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        name0 = str(aname.first_name)

    await disapprvpm.edit(
        f"`Maaf` [{name0}](tg://user?id={disapprvpm.chat_id}) `Pesan Anda Telah Ditolak, Mohon Jangan Melakukan Spam Ke Room Chat!`"
    )

    if BOTLOG:
        await disapprvpm.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={disapprvpm.chat_id})" " `Berhasil Ditolak` !",
        )


@register(outgoing=True, pattern=r"^\.block$")
async def blockpm(block):
    """For .block command, block people from PMing you!"""
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        await block.client(BlockRequest(aname))
        await block.edit("`Anda Telah Diblokir!`")
        uid = replied_user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        await block.edit("`Anda Telah Diblokir!`")
        name0 = str(aname.first_name)
        uid = block.chat_id

    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove

        dissprove(uid)
    except AttributeError:
        pass

    if BOTLOG:
        await block.client.send_message(
            BOTLOG_CHATID,
            "#BLOKIR\n" + "Pengguna: " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern=r"^\.unblock$")
async def unblockpm(unblock):
    """For .unblock command, let people PMing you again!"""
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.from_id)
        name0 = str(replied_user.first_name)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit("`Anda Sudah Tidak Diblokir Lagi.`")

    if BOTLOG:
        await unblock.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={replied_user.id})" " Tidak Lagi Diblokir.",
        )


@register(outgoing=True, pattern=r"^.(set|get|reset) pm_msg(?: |$)(\w*)")
async def add_pmsg(cust_msg):
    """Set your own Unapproved message"""
    if not PM_AUTO_BAN:
        return await cust_msg.edit(
            "**Lord Anda Harus Menyetel** `PM_AUTO_BAN` **Ke** `True`"
        )
    try:
        import userbot.modules.sql_helper.globals as sql
    except AttributeError:
        await cust_msg.edit("`Running on Non-SQL mode!`")
        return

    await cust_msg.edit("`Sedang Memproses...`")
    conf = cust_msg.pattern_match.group(1)

    custom_message = sql.gvarstatus("unapproved_msg")

    if conf.lower() == "set":
        message = await cust_msg.get_reply_message()
        status = "Pesan"

        # check and clear user unapproved message first
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            status = "Pesan"

        if message:
            # TODO: allow user to have a custom text formatting
            # eg: bold, underline, striketrough, link
            # for now all text are in monoscape
            msg = message.message  # get the plain text
            sql.addgvar("unapproved_msg", msg)
        else:
            return await cust_msg.edit("`Mohon Balas Ke Pesan`")

        await cust_msg.edit("`Pesan Berhasil Disimpan Ke Room Chat`")

        if BOTLOG:
            await cust_msg.client.send_message(
                BOTLOG_CHATID,
                f"**{status} PM Yang Tersimpan Dalam Room Chat Anda:** \n\n{msg}",
            )

    if conf.lower() == "reset":
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            await cust_msg.edit("`Anda Telah Menghapus Pesan Custom PM Ke Default`")
        else:
            await cust_msg.edit("`Pesan PM Anda Sudah Default Sejak Awal`")

    if conf.lower() == "get":
        if custom_message is not None:
            await cust_msg.edit(
                "**Ini Adalah Pesan PM Yang Sekarang Dikirimkan Ke Room Chat Anda:**"
                f"\n\n{custom_message}"
            )
        else:
            await cust_msg.edit(
                "*Anda Belum Menyetel Pesan PM*\n"
                f"Masih Menggunakan Pesan PM Default: \n\n`{DEF_UNAPPROVED_MSG}`"
            )


CMD_HELP.update(
    {
        "pmpermit": "**Plugin : **`pmpermit`\
        \n\n  •  **Syntax :** `.setuju` atau `.ok`\
        \n  •  **Function : **Menerima pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm.\
        \n\n  •  **Syntax :** `.tolak` atau `.nopm\
        \n  •  **Function : **Menolak pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm.\
        \n\n  •  **Syntax :** `.block`\
        \n  •  **Function : **Memblokir Orang Di PM.\
        \n\n  •  **Syntax :** `.unblock`\
        \n  •  **Function : **Membuka Blokir.\
        \n\n  •  **Syntax :** `.notifoff`\
        \n  •  **Function : **Menghidupkan notifikasi pesan yang belum diterima.\
        \n\n  •  **Syntax :** `.notifon`\
        \n  •  **Function : **Menghidupkan notifikasi pesan yang belum diterima.\
        \n\n  •  **Syntax :** `.set pm_msg` <balas ke pesan>\
        \n  •  **Function : **Menyetel Pesan Pribadimu untuk orang yang pesannya belum diterima.\
        \n\n  •  **Syntax :** `.get pm_msg`\
        \n  •  **Function : **Mendapatkan Custom pesan PM mu.\
        \n\n  •  **Syntax :** `.reset pm_msg`\
        \n  •  **Function : **Menghapus pesan PM ke default.\
        \n\n  •  **Pesan Pribadi yang belum diterima saat ini tidak dapat disetel ke teks format kaya bold, underline, link, dll. Pesan akan terkirim normal saja**\
    "
    }
)
