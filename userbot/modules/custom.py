# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# FROM Man-Userbot
# t.me/SharingUserbot
#

import io

from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.modules.sql_helper import snips_sql as sql
from userbot.utils import edit_delete, edit_or_reply, man_cmd, reply_id


@man_cmd(pattern=r"\#(\S+)")
async def incom_note(event):
    if not BOTLOG_CHATID:
        return
    try:
        if not (await event.get_sender()).bot:
            notename = event.text[1:]
            notename = notename.lower()
            note = sql.get_note(notename)
            message_id_to_reply = await reply_id(event)
            if note:
                if note.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(note.f_mesg_id)
                    )
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        msg_o,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
                elif note.reply:
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        note.reply,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
    except AttributeError:
        pass


@man_cmd(pattern="custom(?:\\s|$)([\\s\\S]*)")
async def add_snip(event):
    trigger = event.pattern_match.group(1)
    stri = event.text.partition(trigger)[2]
    cht = await event.get_reply_message()
    cht_id = None
    trigger = trigger.lower()
    if cht:
        if stri:
            return await edit_delete(
                event,
                f"**Balas pesan dengan** `{cmd}custom <trigger>` **untuk menambahkan ke custom cmd**",
            )
        await event.client.send_message(
            BOTLOG_CHATID,
            f"📝 **#CUSTOM_CMD**\n • **KEYWORD:** `#{trigger}`\n • 🔖 Pesan ini disimpan sebagai catatan data untuk custom, Tolong JANGAN Dihapus!!",
        )
        cht_o = await event.client.forward_messages(
            entity=BOTLOG_CHATID, messages=cht, from_peer=event.chat_id, silent=True
        )
        cht_id = cht_o.id
    if not cht:
        if not stri:
            return await edit_delete(
                event,
                f"**Perintah tidak diketahui! ketik** `{cmd}help custom` **bila butuh bantuan.**",
            )
        await event.client.send_message(
            BOTLOG_CHATID,
            f"📝 **#CUSTOM_CMD**\n • **KEYWORD:** `#{trigger}`\n • 🔖 Pesan ini disimpan sebagai catatan data untuk custom, Tolong JANGAN Dihapus!!",
        )
        cht_o = await event.client.send_message(BOTLOG_CHATID, stri)
        cht_id = cht_o.id
        stri = None
    success = "**custom {}. Gunakan** `#{}` **di mana saja untuk menggunakannya**"
    if sql.add_note(trigger, stri, cht_id) is False:
        sql.rm_note(trigger)
        if sql.add_note(trigger, stri, cht_id) is False:
            return await edit_or_reply(event, "**Gagal Menambahkan Custom CMD**")
        return await edit_or_reply(event, success.format("Berhasil di Update", trigger))
    return await edit_or_reply(event, success.format("Berhasil disimpan", trigger))


@man_cmd(pattern="delcustom(?:\\s|$)([\\s\\S]*)")
async def _(event):
    input_str = (event.pattern_match.group(1)).lower()
    if not input_str:
        return await edit_delete(event, "**Berikan nama custom untuk dihapus**")
    if input_str.startswith("#"):
        input_str = input_str.replace("#", "")
    try:
        sql.rm_note(input_str)
        await edit_or_reply(
            event, "**Berhasil menghapus custom:** `#{}`".format(input_str)
        )
    except BaseException:
        await edit_or_reply(event, "Tidak ada snip yang disimpan dengan pemicu ini.")


@man_cmd(pattern="customs$")
async def lsnote(event):
    all_snips = sql.get_notes()
    OUT_STR = "**List Custom yang tersedia:**\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"✣ `#{a_snip.keyword}` \n"
    else:
        OUT_STR = "**Tidak ada custom cmd yang disimpan.**"
    if len(OUT_STR) > 4000:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "snips.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="**List Custom yang tersedia**",
                reply_to=event,
            )
            await event.delete()
    else:
        await edit_or_reply(event, OUT_STR)


CMD_HELP.update(
    {
        "custom": f"**Plugin : **`custom`\
        \n\n  •  **Syntax :** `{cmd}custom` <nama> <data> atau membalas pesan dengan .custom <nama>\
        \n  •  **Function : **Menyimpan pesan custom (catatan global) dengan nama. (bisa dengan gambar, docs, dan stickers!)\
        \n\n  •  **Syntax :** `{cmd}customs`\
        \n  •  **Function : **Mendapat semua customs yang disimpan.\
        \n\n  •  **Syntax :** `{cmd}delcustom` <nama_custom>\
        \n  •  **Function : **Menghapus custom yang ditentukan.\
    "
    }
)
