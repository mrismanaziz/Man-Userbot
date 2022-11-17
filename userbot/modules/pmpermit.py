# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# @SharingUserbot
""" Userbot module for keeping control who PM you. """

from sqlalchemy.exc import IntegrityError
from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User

from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, COUNT_PM, LASTMSG, LOGS, PM_AUTO_BAN, PM_LIMIT, bot
from userbot.events import man_cmd
from userbot.utils import edit_delete, edit_or_reply

DEF_UNAPPROVED_MSG = (
    "╔════════════════════╗\n"
    "     ⛑ 𝗔𝗧𝗧𝗘𝗡𝗧𝗜𝗢𝗡 𝗣𝗟𝗘𝗔𝗦𝗘 ⛑\n"
    "╚════════════════════╝\n"
    "• Saya belum menyetujui anda untuk PM.\n"
    "• Tunggu sampai saya menyetujui PM anda.\n"
    "• Jangan Spam Chat atau anda akan otomatis diblokir.\n"
    "╔════════════════════╗\n"
    "    𝗣𝗲𝘀𝗮𝗻 𝗢𝘁𝗼𝗺𝗮𝘁𝗶𝘀 𝗕𝘆 -𝗨𝘀𝗲𝗿𝗕𝗼𝘁\n"
    "╚════════════════════╝\n"
)


@bot.on(events.NewMessage(incoming=True))
async def permitpm(event):
    """ Prohibits people from PMing you without approval. \
        Will block retarded nibbas automatically. """
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    sender = await event.get_sender()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not sender.bot
        and not sender.contact
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
        UNAPPROVED_MSG = getmsg if getmsg is not None else DEF_UNAPPROVED_MSG
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

            if COUNT_PM[event.chat_id] > PM_LIMIT:
                await event.respond(
                    "**Maaf Anda Telah Di Blokir Karna Melakukan Spam Chat**"
                )

                try:
                    del COUNT_PM[event.chat_id]
                    del LASTMSG[event.chat_id]
                except KeyError:
                    if BOTLOG_CHATID:
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "**Terjadi Error Saat Menghitung Private Message, Mohon Restart Bot!**",
                        )
                    return LOGS.info("Gagal menghitung PM yang diterima")

                await event.client(BlockRequest(event.chat_id))
                await event.client(ReportSpamRequest(peer=event.chat_id))

                if BOTLOG_CHATID:
                    name = await event.client.get_entity(event.chat_id)
                    name0 = str(name.first_name)
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "["
                        + name0
                        + "](tg://user?id="
                        + str(event.chat_id)
                        + ")"
                        + " **Telah Diblokir Karna Melakukan Spam Ke Room Chat**",
                    )


@bot.on(events.NewMessage(outgoing=True))
async def auto_accept(event):
    """Will approve automatically if you texted them first."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    sender = await event.get_sender()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not sender.bot
        and not sender.contact
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import approve, is_approved
        except AttributeError:
            return

        # Use user custom unapproved message
        get_message = gvarstatus("unapproved_msg")
        UNAPPROVED_MSG = get_message if get_message is not None else DEF_UNAPPROVED_MSG
        chat = await event.get_chat()
        if isinstance(chat, User):
            if is_approved(event.chat_id) or chat.bot:
                return
            async for message in event.client.iter_messages(
                event.chat_id, reverse=True, limit=1
            ):
                if (
                    message.text is not UNAPPROVED_MSG
                    and message.sender_id == self_user.id
                ):
                    try:
                        approve(event.chat_id)
                    except IntegrityError:
                        return

                if is_approved(event.chat_id) and BOTLOG_CHATID:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "**#AUTO_APPROVED**\n"
                        + "👤 **User:** "
                        + f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@bot.on(man_cmd(outgoing=True, pattern=r"notifoff$"))
async def notifoff(noff_event):
    try:
        from userbot.modules.sql_helper.globals import addgvar
    except AttributeError:
        return await noff_event.edit("`Running on Non-SQL mode!`")
    addgvar("NOTIF_OFF", True)
    await noff_event.edit(
        "**Notifikasi Pesan Pribadi Tidak Disetujui, Telah Dibisukan!**"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"notifon$"))
async def notifon(non_event):
    try:
        from userbot.modules.sql_helper.globals import delgvar
    except AttributeError:
        return await non_event.edit("`Running on Non-SQL mode!`")
    delgvar("NOTIF_OFF")
    await non_event.edit(
        "**Notifikasi Pesan Pribadi Disetujui, Tidak Lagi Dibisukan!**"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"(?:setuju|ok)\s?(.)?"))
async def approvepm(apprvpm):
    """For .ok command, give someone the permissions to PM you."""
    try:
        from userbot.modules.sql_helper.globals import gvarstatus
        from userbot.modules.sql_helper.pm_permit_sql import approve
    except AttributeError:
        return await edit_delete(apprvpm, "`Running on Non-SQL mode!`")

    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        replied_user = await apprvpm.client.get_entity(reply.sender_id)
        uid = replied_user.id
        name0 = str(replied_user.first_name)

    elif apprvpm.pattern_match.group(1):
        inputArgs = apprvpm.pattern_match.group(1)

        try:
            inputArgs = int(inputArgs)
        except ValueError:
            pass

        try:
            user = await apprvpm.client.get_entity(inputArgs)
        except BaseException:
            return await edit_delete(apprvpm, "**Invalid username/ID.**")

        if not isinstance(user, User):
            return await edit_delete(
                apprvpm, "**Mohon Reply Pesan User Yang ingin diterima.**"
            )

        uid = user.id
        name0 = str(user.first_name)

    else:
        aname = await apprvpm.client.get_entity(apprvpm.chat_id)
        if not isinstance(aname, User):
            return await edit_delete(
                apprvpm, "**Mohon Reply Pesan User Yang ingin diterima.**"
            )
        name0 = str(aname.first_name)
        uid = apprvpm.chat_id

    # Get user custom msg
    getmsg = gvarstatus("unapproved_msg")
    UNAPPROVED_MSG = getmsg if getmsg is not None else DEF_UNAPPROVED_MSG
    async for message in apprvpm.client.iter_messages(
        apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG
    ):
        await message.delete()

    try:
        approve(uid)
    except IntegrityError:
        return await edit_delete(apprvpm, "**Pesan Anda Sudah Diterima**")

    await edit_delete(
        apprvpm, f"**Menerima Pesan Dari** [{name0}](tg://user?id={uid})", 5
    )


@bot.on(man_cmd(outgoing=True, pattern=r"(?:tolak|nopm)\s?(.)?"))
async def disapprovepm(disapprvpm):
    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove
    except BaseException:
        return await edit_delete(disapprvpm, "`Running on Non-SQL mode!`")

    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.sender_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        dissprove(aname)

    elif disapprvpm.pattern_match.group(1):
        inputArgs = disapprvpm.pattern_match.group(1)

        try:
            inputArgs = int(inputArgs)
        except ValueError:
            pass

        try:
            user = await disapprvpm.client.get_entity(inputArgs)
        except BaseException:
            return await edit_delete(
                disapprvpm, "**Mohon Reply Pesan User Yang ingin ditolak.**"
            )

        if not isinstance(user, User):
            return await edit_delete(
                disapprvpm, "**Mohon Reply Pesan User Yang ingin ditolak.**"
            )

        aname = user.id
        dissprove(aname)
        name0 = str(user.first_name)

    else:
        dissprove(disapprvpm.chat_id)
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        if not isinstance(aname, User):
            return await edit_delete(
                disapprvpm, "**This can be done only with users.**"
            )
        name0 = str(aname.first_name)
        aname = aname.id

    await edit_or_reply(
        disapprvpm,
        f" **Maaf Pesan** [{name0}](tg://user?id={aname}) **Telah Ditolak, Mohon Jangan Melakukan Spam Ke Room Chat!**",
    )


@bot.on(man_cmd(outgoing=True, pattern=r"block$"))
async def blockpm(block):
    """For .block command, block people from PMing you!"""
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.sender_id)
        aname = replied_user.id
        await block.client(BlockRequest(aname))
        await block.edit("**Anda Telah Diblokir!**")
        uid = replied_user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        if not isinstance(aname, User):
            return await block.edit("**This can be done only with users.**")
        await block.edit("**Kamu Telah Diblokir!**")
        uid = block.chat_id

    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove

        dissprove(uid)
    except AttributeError:
        pass


@bot.on(man_cmd(outgoing=True, pattern=r"unblock$"))
async def unblockpm(unblock):
    """For .unblock command, let people PMing you again!"""
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.sender_id)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit("**Anda Sudah Tidak Diblokir Lagi.**")


@bot.on(man_cmd(outgoing=True, pattern=r"(set|get|reset) pmpermit(?: |$)(\w*)"))
async def add_pmsg(cust_msg):
    """Set your own Unapproved message"""
    if not PM_AUTO_BAN:
        return await cust_msg.edit(
            "**Anda Harus Menyetel Var** `PM_AUTO_BAN` **Ke** `True`\n\n**Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `.set var PM_AUTO_BAN True`"
        )
    try:
        import userbot.modules.sql_helper.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return

    await cust_msg.edit("`Processing...`")
    conf = cust_msg.pattern_match.group(1)

    custom_message = sql.gvarstatus("unapproved_msg")

    if conf.lower() == "set":
        message = await cust_msg.get_reply_message()
        status = "Pesan"

        # check and clear user unapproved message first
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            status = "Pesan"

        if not message:
            return await cust_msg.edit("**Mohon Reply Ke Pesan**")

        # TODO: allow user to have a custom text formatting
        # eg: bold, underline, striketrough, link
        # for now all text are in monoscape
        msg = message.message  # get the plain text
        sql.addgvar("unapproved_msg", msg)
        await cust_msg.edit("**Pesan Berhasil Disimpan Ke Room Chat**")

        if BOTLOG_CHATID:
            await cust_msg.client.send_message(
                BOTLOG_CHATID,
                f"**{status} PMPERMIT Yang Tersimpan:** \n\n{msg}",
            )

    if conf.lower() == "reset":
        if custom_message is None:
            await cust_msg.edit(
                "`Anda Telah Menghapus Pesan Custom PMPERMIT menjadi Default`"
            )

        else:
            sql.delgvar("unapproved_msg")
            await cust_msg.edit("`Pesan PMPERMIT Anda Sudah Default Sejak Awal`")
    if conf.lower() == "get":
        if custom_message is not None:
            await cust_msg.edit(
                "**Pesan PMPERMIT Yang Sekarang:**" f"\n\n{custom_message}"
            )
        else:
            await cust_msg.edit(
                "**Anda Belum Menyetel Pesan Costum PMPERMIT,**\n"
                f"**Masih Menggunakan Pesan PM Default:**\n\n{DEF_UNAPPROVED_MSG}"
            )


CMD_HELP.update(
    {
        "pmpermit": f"**Plugin : **`pmpermit`\
        \n\n  •  **Syntax :** `{cmd}setuju` atau `{cmd}ok`\
        \n  •  **Function : **Menerima pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm.\
        \n\n  •  **Syntax :** `{cmd}tolak` atau `{cmd}nopm`\
        \n  •  **Function : **Menolak pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm.\
        \n\n  •  **Syntax :** `{cmd}block`\
        \n  •  **Function : **Memblokir Orang Di PM.\
        \n\n  •  **Syntax :** `{cmd}unblock`\
        \n  •  **Function : **Membuka Blokir.\
        \n\n  •  **Syntax :** `{cmd}notifoff`\
        \n  •  **Function : **Menghidupkan notifikasi pesan yang belum diterima.\
        \n\n  •  **Syntax :** `{cmd}notifon`\
        \n  •  **Function : **Menghidupkan notifikasi pesan yang belum diterima.\
        \n\n  •  **Syntax :** `{cmd}set pmpermit` <balas ke pesan>\
        \n  •  **Function : **Menyetel Pesan Pribadimu untuk orang yang pesannya belum diterima.\
        \n\n  •  **Syntax :** `{cmd}get pmpermit`\
        \n  •  **Function : **Mendapatkan Custom pesan PM mu.\
        \n\n  •  **Syntax :** `{cmd}reset pmpermit`\
        \n  •  **Function : **Menghapus pesan PM ke default.\
        \n\n  •  **Pesan Pribadi yang belum diterima saat ini tidak dapat disetel ke teks format kaya bold, underline, link, dll. Pesan akan terkirim normal saja**\
        \n\n**NOTE: Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `.set var PM_AUTO_BAN True`\
    "
    }
)
