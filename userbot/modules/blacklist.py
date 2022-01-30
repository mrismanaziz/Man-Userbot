# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

# port to userbot from uniborg by @keselekpermen69


import io
import re

import userbot.modules.sql_helper.blacklist_sql as sql
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, man_cmd, man_handler


@man_handler()
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.reply(
                    "`Anda Tidak Punya Izin Untuk Menghapus Pesan Disini`"
                )
                await sleep(1)
                await reply.delete()
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break


@man_cmd(pattern="addbl(?: |$)(.*)")
async def on_add_black_list(addbl):
    text = addbl.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    for trigger in to_blacklist:
        sql.add_to_blacklist(addbl.chat_id, trigger.lower())
    await edit_or_reply(
        addbl, "`Menambahkan Kata` **{}** `Ke Blacklist Untuk Obrolan Ini`".format(text)
    )


@man_cmd(pattern="listbl(?: |$)(.*)")
async def on_view_blacklist(listbl):
    all_blacklisted = sql.get_chat_blacklist(listbl.chat_id)
    OUT_STR = "Blacklists in the Current Chat:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"`{trigger}`\n"
    else:
        OUT_STR = "**Tidak Ada Blacklist Dalam Obrolan Ini.**"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await listbl.client.send_file(
                listbl.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Blacklist Dalam Obrolan Ini",
                reply_to=listbl,
            )
            await listbl.delete()
    else:
        await edit_or_reply(listbl, OUT_STR)


@man_cmd(pattern="rmbl(?: |$)(.*)")
async def on_delete_blacklist(rmbl):
    text = rmbl.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(sql.rm_from_blacklist(rmbl.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    if not successful:
        await rmbl.edit("**{}** `Tidak Ada Di Blacklist`".format(text))
    else:
        await rmbl.edit("`Berhasil Menghapus` **{}** `Di Blacklist`".format(text))


CMD_HELP.update(
    {
        "blacklist": f"**Plugin : **`blacklist`\
        \n\n  •  **Syntax :** `{cmd}listbl`\
        \n  •  **Function : **Melihat daftar blacklist yang aktif di obrolan.\
        \n\n  •  **Syntax :** `{cmd}addbl` <kata>\
        \n  •  **Function : **Memasukan pesan ke blacklist 'kata blacklist'.\
        \n\n  •  **Syntax :** `{cmd}rmbl` <kata>\
        \n  •  **Function : **Menghapus kata blacklist.\
    "
    }
)
