# Copyright (C) 2021 @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, edit_or_reply, man_cmd


@man_cmd(pattern="shazam(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await edit_delete(event, "**Mohon balas ke pesan audio**")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                xx = await edit_or_reply(event, "`Mengidentifikasi lagu...`")
                start_msg = await conv.send_message("/start")
                await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await xx.edit(
                        "Terjadi Error saat mengidentifikasi lagu. Coba gunakan pesan audio yang panjangnya 5-10 detik."
                    )
                await xx.edit("`Tunggu sebentar...`")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.client(UnblockRequest(chat))
                xx = await edit_or_reply(event, "`Mengidentifikasi lagu...`")
                start_msg = await conv.send_message("/start")
                await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await xx.edit(
                        "Terjadi Error saat mengidentifikasi lagu. Coba gunakan pesan audio yang panjangnya 5-10 detik."
                    )
                await xx.edit("`Tunggu sebentar...`")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            namem = f"**Nama Lagu : **`{result.text.splitlines()[0]}`\
        \n\n**Details : **__{result.text.splitlines()[2]}__"
            await xx.edit(namem)
            await event.client.delete_messages(
                conv.chat_id, [start_msg.id, send_audio.id, check.id, result.id]
            )
    except TimeoutError:
        return await edit_delete(
            event, "**ERROR: @auddbot tidak merespon silahkan coba lagi nanti**"
        )


CMD_HELP.update(
    {
        "shazam": f"**Plugin : **`shazam`\
        \n\n  •  **Syntax :** `{cmd}shazam` <reply ke voice/audio>\
        \n  •  **Function : **Untuk mencari Judul lagu dengan menggunakan file audio via @auddbot \
    "
    }
)
