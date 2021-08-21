# Copyright (C) 2021 Man-Userbot
# Created by mrismanaziz
# FROM <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.short(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    msg_link = await event.get_reply_message()
    d_link = event.pattern_match.group(1)

    if msg_link:
        d_link = msg_link.text
        await event.edit("`Shortening replied link...`")
    elif "https" not in d_link:
        await event.edit(
            "**Masukkan link, pastikan dimulai dengan** `http://` **atau** `https://`"
        )
    else:
        await event.edit("`Shortening link...`")
    chat = "@ShortUrlBot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                bot_reply = await conv.get_response()
                msg = await conv.send_message(d_link)
                response = await conv.get_response()
                url = await conv.get_response()
                sponser = await conv.get_response()
                """- jangan spam notif -"""
                await bot.send_read_acknowledge(conv.chat_id)
                await event.edit(response.text)
            except YouBlockedUserError:
                await event.edit("**Unblock @ShortUrlBot dan coba lagi**")
                return
            await event.client.send_message(event.chat_id, url)
            await event.client.delete_messages(
                conv.chat_id,
                [msg_start.id, response.id, msg.id, bot_reply.id, sponser.id, url.id],
            )
            await event.delete()
    except TimeoutError:
        return await event.edit(
            "**ERROR: @ShortUrlBot tidak merespon silahkan coba lagi nanti**"
        )


CMD_HELP.update(
    {
        "shortlink": "**Plugin : **`shortlink`\
        \n\n  •  **Syntax :** `.short` <url/reply link>\
        \n  •  **Function : **Untuk menyimpelkan link url menjadi pendek menggunakan @ShortUrlBot\
    "
    }
)
