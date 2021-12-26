# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import os

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.utils import edit_delete, edit_or_reply, man_cmd


@man_cmd(pattern="kamuii(:? |$)([1-8])?")
async def _(fry):
    xx = await edit_or_reply(fry, "`Mengaktifkan Kekuatan Supersaya...`")
    level = fry.pattern_match.group(2)
    if fry.fwd_from:
        return
    if not fry.reply_to_msg_id:
        await edit_delete(xx, "**Silahkan Balas Ke Media Foto**")
        return
    reply_message = await fry.get_reply_message()
    if not reply_message.media:
        await edit_delete(xx, "**Gambar tidak di dukung**")
        return
    if reply_message.sender.bot:
        await edit_delete(xx, "**Mohon Balas Ke Media**")
        return
    chat = "@image_deepfrybot"
    message_id_to_reply = fry.message.reply_to_msg_id
    async with fry.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/deepfry {level}"
                msg_level = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
            response = await conv.get_response()
            await fry.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await fry.client(UnblockRequest(chat))
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/deepfry {level}"
                msg_level = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
            response = await conv.get_response()
            await fry.client.send_read_acknowledge(conv.chat_id)
        if response.text.startswith("Forward"):
            await xx.edit("**Silahkan Matikan Setelan Privasi Forward**")
        else:
            downloaded_file_name = await fry.client.download_media(
                response.media, TEMP_DOWNLOAD_DIRECTORY
            )
            await fry.client.send_file(
                fry.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply,
            )
            try:
                msg_level
            except NameError:
                await fry.client.delete_messages(conv.chat_id, [msg.id, response.id])
            else:
                await fry.client.delete_messages(
                    conv.chat_id, [msg.id, response.id, r.id, msg_level.id]
                )
    await fry.delete()
    return os.remove(downloaded_file_name)


CMD_HELP.update(
    {
        "kamuii": f"**Plugin : **`kamuii`\
        \n\n  •  **Syntax :** `{cmd}kamuii` atau `{cmd}kamuii` [level(1-8)]\
        \n  •  **Function : **Untuk mengubah foto/sticker menjadi penyok.\
    "
    }
)
