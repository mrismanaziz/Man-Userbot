# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# FROM Man-Userbot
# t.me/SharingUserbot
#
""" Userbot module containing commands for keeping costum global notes. """

from userbot import BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"\.\w*", ignore_unsafe=True, disable_errors=True)
async def on_snip(event):
    """costums logic."""
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip:
        if snip.f_mesg_id:
            msg_o = await event.client.get_messages(
                entity=BOTLOG_CHATID, ids=int(snip.f_mesg_id)
            )
            await event.client.send_message(
                event.chat_id,
                msg_o.message,
                reply_to=message_id_to_reply,
                file=msg_o.media,
            )
            await event.delete()
        elif snip.reply:
            await event.client.send_message(
                event.chat_id, snip.reply, reply_to=message_id_to_reply
            )
            await event.delete()


@register(outgoing=True, pattern=r"^\.costum (\w*)")
async def on_snip_save(event):
    """For .costum command, saves costums for future use."""
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit("**Berjalan pada mode Non-SQL!**")
        return
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"📝 **#COSTUM**\
            \n • **KEYWORD:** `{keyword}`\
            \n • 🔖 Pesan ini disimpan sebagai catatan data untuk costum, Tolong JANGAN Dihapus!!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await event.edit(
                "**Menyimpan kostum dengan media membutuhkan `BOTLOG_CHATID` untuk disetel.**"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = (
        "**Costum {} disimpan. Gunakan** `.{}` **di mana saja untuk menggunakannya**"
    )
    if add_snip(keyword, string, msg_id) is False:
        await event.edit(success.format("Berhasil", keyword))
    else:
        await event.edit(success.format("Berhasil", keyword))


@register(outgoing=True, pattern=r"^\.costums$")
async def on_snip_list(event):
    """For .costums command, lists costums saved by you."""
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("**Berjalan pada mode Non-SQL!**")
        return

    message = "**Tidak ada kostum yang tersedia saat ini.**"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "**Tidak ada kostum yang tersedia saat ini.**":
            message = "**List Costum yang tersedia:**\n"
        message += f"✣ `.{a_snip.snip}`\n"
    await event.edit(message)


@register(outgoing=True, pattern=r"^\.delcostum (\w*)")
async def on_snip_delete(event):
    """For .delcostum command, deletes a costum."""
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("**Berjalan pada mode Non-SQL!**")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"**Berhasil menghapus costum:** `{name}`")
    else:
        await event.edit(f"**Tidak dapat menemukan costum:** `{name}`")


CMD_HELP.update(
    {
        "costum": "**Plugin : **`costum`\
        \n\n  •  **Syntax :** `.costum` <nama> <data> atau membalas pesan dengan .costum <nama>\
        \n  •  **Function : **Menyimpan pesan costum (catatan global) dengan nama. (bisa dengan gambar, docs, dan stickers!)\
        \n\n  •  **Syntax :** `.costums`\
        \n  •  **Function : **Mendapat semua costums yang disimpan.\
        \n\n  •  **Syntax :** `.delcostum` <nama_costum>\
        \n  •  **Function : **Menghapus costum yang ditentukan.\
    "
    }
)
