# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

from asyncio import sleep
from re import IGNORECASE, escape, search

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(incoming=True, disable_edited=True, disable_errors=True)
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.filter_sql import get_filters
            except AttributeError:
                await handler.edit("`Berjalan Pada Mode Non-SQL!`")
                return
            name = handler.raw_text
            filters = get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = r"( |^|[^\w])" + escape(trigger.keyword) + r"( |$|[^\w])"
                pro = search(pattern, name, flags=IGNORECASE)
                if pro and trigger.f_mesg_id:
                    msg_o = await handler.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                    )
                    await handler.reply(msg_o.message, file=msg_o.media)
                elif pro and trigger.reply:
                    await handler.reply(trigger.reply)
    except AttributeError:
        pass


@register(outgoing=True, pattern=r"^.filter (.*)")
async def add_new_filter(new_handler):
    """ For .filter command, allows adding new filters in a chat """
    try:
        from userbot.modules.sql_helper.filter_sql import add_filter
    except AttributeError:
        await new_handler.edit("`Berjalan Pada Mode Non-SQL!`")
        return
    value = new_handler.pattern_match.group(1).split(None, 1)
    """ - The first words after .filter(space) is the keyword - """
    keyword = value[0]
    try:
        string = value[1]
    except IndexError:
        string = None
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await new_handler.client.send_message(
                BOTLOG_CHATID,
                f"#FILTER\nID OBROLAN: {new_handler.chat_id}\nTRIGGER: {keyword}"
                "\n\n`Pesan Berikut Disimpan Sebagai Data Balasan Filter Untuk Obrolan, Mohon Jangan Menghapusnya`",
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            return await new_handler.edit(
                "`Untuk menyimpan media sebagai balasan ke filter, BOTLOG_CHATID harus disetel.`"
            )
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "`Berhasil Menambahkan Filter` **{}** `{}`."
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        await new_handler.edit(success.format(keyword, "Disini"))
    else:
        await new_handler.edit(success.format(keyword, "Disini"))


@register(outgoing=True, pattern=r"^.stop (.*)")
async def remove_a_filter(r_handler):
    """ For .stop command, allows you to remove a filter from a chat. """
    try:
        from userbot.modules.sql_helper.filter_sql import remove_filter
    except AttributeError:
        return await r_handler.edit("`Berjalan Pada Mode Non-SQL!`")
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("`Filter` **{}** `Tidak Ada Disini`.".format(filt))
    else:
        await r_handler.edit(
            "`Berhasil Menghapus Filter` **{}** `Disini`.".format(filt)
        )


@register(outgoing=True, pattern="^.hapusbotfilter (.*)")
async def kick_marie_filter(event):
    """ For .bersihkanbotfilter command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    bot_type = event.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        return await event.edit("`Bot Itu Belum Didukung!`")
    await event.edit("```Saya Akan Menghapus Semua Filter!```")
    await sleep(3)
    resp = await event.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type.lower() == "marie":
            await event.reply("/stop %s" % (i.strip()))
        if bot_type.lower() == "rose":
            i = i.replace("`", "")
            await event.reply("/stop %s" % (i.strip()))
        await sleep(0.3)
    await event.respond("```Berhasil Menghapus Semua Filter Bot!```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "Saya Membersihkan Semua Filter Bot Di " + str(event.chat_id)
        )


@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    try:
        from userbot.modules.sql_helper.filter_sql import get_filters
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")
    transact = "`Tidak Ada Filter Apapun Disini.`"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if transact == "`Tidak Ada Filter Apapun Disini.`":
            transact = "**✥ Daftar Filter Yang Aktif Disini:**\n"
            transact += " ✣ `{}`\n".format(filt.keyword)
        else:
            transact += " ✣ `{}`\n".format(filt.keyword)

    await event.edit(transact)


CMD_HELP.update(
    {
        "filter": "**Plugin : **`filter`\
        \n\n  •  **Syntax :** `.filters`\
        \n  •  **Function : **Melihat filter userbot yang aktif di obrolan.\
        \n\n  •  **Syntax :** `.filter` <keyword> <balasan> atau balas ke pesan ketik `.filter` <keyword>\
        \n  •  **Function : **Membuat filter di obrolan, Bot Akan Membalas Jika Ada Yang Menyebut 'keyword' yang dibuat. Bisa dipakai ke media/sticker/vn/file.\
        \n\n  •  **Syntax :** `.stop` <keyword>\
        \n  •  **Function : **Untuk Nonaktifkan Filter.\
        \n\n  •  **Syntax :** `.hapusbotfilter` <marie/rose>\
        \n  •  **Function : **Menghapus semua filter yang ada di bot grup (Saat ini bot yang didukung: Marie, Rose.) dalam obrolan.\
    "
    }
)
