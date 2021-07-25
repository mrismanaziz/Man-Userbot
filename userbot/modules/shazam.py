# Copyright (C) 2021 @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.shazam(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await event.edit("**Mohon balas ke pesan audio**")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                await event.edit("`Mengidentifikasi lagu...`")
                start_msg = await conv.send_message("/start")
                await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await event.edit(
                        "Terjadi Error saat mengidentifikasi lagu. Coba gunakan pesan audio yang panjangnya 5-10 detik."
                    )
                await event.edit("`Tunggu sebentar...`")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("**Mohon Buka blokir @auddbot dan coba lagi**")
                return
            namem = f"**Nama Lagu : **`{result.text.splitlines()[0]}`\
        \n\n**Details : **__{result.text.splitlines()[2]}__"
            await event.edit(namem)
            await event.client.delete_messages(
                conv.chat_id, [start_msg.id, send_audio.id, check.id, result.id]
            )
    except TimeoutError:
        return await event.edit(
            "**ERROR: @auddbot tidak merespon silahkan coba lagi nanti**"
        )


CMD_HELP.update(
    {
        "shazam": "**Plugin : **`shazam`\
        \n\n  •  **Syntax :** `.shazam` <reply ke voice/audio>\
        \n  •  **Function : **Untuk mencari Judul lagu dengan menggunakan file audio via @auddbot \
    "
    }
)
