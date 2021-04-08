# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.purge$")
async def fastpurger(purg):
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count += 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        return await purg.edit("`Mohon Balas Ke Pesan`")

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        f"`Berhasil Menghapus Kenangan`\
        \nJumlah Pesan Yang Dihapus {str(count)} Pesan",
    )
    """
    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "Berhasil Menghapus Pesan" + str(count) + " Pesan Berhasil  Dibersihkan.")
    """
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern=r"^\.purgeme")
async def purgeme(delme):
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Berhasil Menghapus Kenangan,` " + str(count) + " `Kenangan Telah Dihapus`",
    )
    """
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "`Telah Menghapus Pesan,` " + str(count) + " Pesan Telah Dihapus `")
    """
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern=r"^\.del$")
async def delete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            """
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "`Berhasil Menghapus Pesan `")
            """
        except rpcbaseerrors.BadRequestError:
            await delme.edit("`Tidak Bisa Menghapus Pesan`")
            """
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "`Tidak Bisa Menghapus Pesan`")
            """


@register(outgoing=True, pattern=r"^\.edit")
async def editer(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i += 1
    """
    if BOTLOG:
        await edit.client.send_message(BOTLOG_CHATID,
                                       "`Berhasil Mengedit Pesan`")
   """


@register(outgoing=True, pattern=r"^\.sd")
async def selfdestruct(destroy):
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    """
    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID,
                                          "`SD Berhasil Dilakukan`")
    """


CMD_HELP.update(
    {
        "purge": "**Plugin : **`Menghapus Kenangan Chat`\
        \n\n  •  **Syntax :** `.purge`\
        \n  •  **Function : **Membersihkan semua pesan mulai dari pesan yang dibalas.\
        \n\n  •  **Syntax :** `.purgeme` <angka>\
        \n  •  **Function : **Menghapus jumlah pesan anda, yang mau anda hapus.\
        \n\n  •  **Syntax :** `.del`\
        \n  •  **Function : **Menghapus pesan, balas ke pesan.\
        \n\n  •  **Syntax :** `.edit <pesan baru>`\
        \n  •  **Function : **Ganti pesan terakhir Anda dengan <pesan baru>.\
        \n\n  •  **Syntax :** `.sd` <x> <pesan>\
        \n  •  **Function : **Membuat pesan yang hancur sendiri dalam x detik. detik di bawah 100 untuk menghindari bot Anda akan sleep.\
    "
    }
)
