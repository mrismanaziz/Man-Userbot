# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

import asyncio
import re

from telethon import utils as ut
from telethon.tl import types

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.modules.sql_helper.filter_sql import (
    add_filter,
    get_all_filters,
    remove_all_filters,
    remove_filter,
)
from userbot.utils import man_cmd
from userbot.utils.tools import eod

DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


global last_triggered_filters
last_triggered_filters = {}


@man_cmd(incoming=True)
async def on_snip(event):
    global last_triggered_filters
    name = event.raw_text
    if event.chat_id in last_triggered_filters:
        if name in last_triggered_filters[event.chat_id]:
            return False
    snips = get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                else:
                    media = None
                event.message.id
                if event.reply_to_msg_id:
                    event.reply_to_msg_id
                await event.reply(snip.reply, file=media)
                if event.chat_id not in last_triggered_filters:
                    last_triggered_filters[event.chat_id] = []
                last_triggered_filters[event.chat_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                last_triggered_filters[event.chat_id].remove(name)


@man_cmd(pattern="filter(?:\s|$)([\s\S]*)")
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        snip = {"type": TYPE_TEXT, "text": msg.message or ""}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = ut.get_input_photo(msg.media.photo)
                snip["type"] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = ut.get_input_document(msg.media.document)
                snip["type"] = TYPE_DOCUMENT
            if media:
                snip["id"] = media.id
                snip["hash"] = media.access_hash
                snip["fr"] = media.file_reference
        add_filter(
            event.chat_id,
            name,
            snip["text"],
            snip["type"],
            snip.get("id"),
            snip.get("hash"),
            snip.get("fr"),
        )
        await eod(event, f"**Berhasil Menambahkan Filter** `{name}")
    else:
        await eod(
            event, f"Balas pesan dengan `{cmd}filter keyword` untuk menyimpan filter"
        )


@man_cmd(pattern="filters$")
async def on_snip_list(event):
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "**✥ Daftar Filter Yang Aktif Disini:** \n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 {a_snip.keyword} \n"
    else:
        OUT_STR = "**Tidak Ada Filter Apapun Disini.**"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Daftar Filter Yang Aktif Disini",
                reply_to=event,
            )
            await event.delete()
    else:
        await eod(event, OUT_STR)


@man_cmd(pattern="stop(?:\s|$)([\s\S]*)")
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    try:
        remove_filter(event.chat_id, name)
        await eod(event, f"**Berhasil Menghapus Filter** `{name}`")
    except Exception as e:
        await eod(event, f"**ERROR:** `{e}`")


@man_cmd(pattern="rmallfilters$")
async def on_all_snip_delete(event):
    remove_all_filters(event.chat_id)
    await eor(event, f"**Berhasil Menghapus Semua Filter dalam obrolan ini**")


CMD_HELP.update(
    {
        "filter": f"**Plugin : **`filter`\
        \n\n  •  **Syntax :** `{cmd}filters`\
        \n  •  **Function : **Melihat filter userbot yang aktif di obrolan.\
        \n\n  •  **Syntax :** `{cmd}filter` <keyword> <balasan> atau balas ke pesan ketik `.filter` <keyword>\
        \n  •  **Function : **Membuat filter di obrolan, Bot Akan Membalas Jika Ada Yang Menyebut 'keyword' yang dibuat. Bisa dipakai ke media/sticker/vn/file.\
        \n\n  •  **Syntax :** `{cmd}stop` <keyword>\
        \n  •  **Function : **Untuk Nonaktifkan Filter.\
        \n\n  •  **Syntax :** `{cmd}rmallfilters`\
        \n  •  **Function : **Menghapus semua filter yang ada di grup.\
    "
    }
)
