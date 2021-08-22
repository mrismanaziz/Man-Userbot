# Copyright (C) 2021 Man-Userbot
# Created by mrismanaziz
# FROM <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.pdf(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await event.edit("**Mohon Reply ke teks apa pun**")
    reply_message = await event.get_reply_message()
    chat = "@office2pdf_bot"
    await event.edit("`Mengubah menjadi PDF...`")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                msg = await conv.send_message(reply_message)
                convert = await conv.send_message("/ready2conv")
                cnfrm = await conv.get_response()
                editfilename = await conv.send_message("Yes")
                enterfilename = await conv.get_response()
                filename = await conv.send_message("Man-Userbot")
                started = await conv.get_response()
                pdf = await conv.get_response()
                """- jangan spam notif -"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("**Unblock @office2pdf_bot dan coba lagi**")
                return
            await event.client.send_message(event.chat_id, pdf)
            await event.client.delete_messages(
                conv.chat_id,
                [
                    msg_start.id,
                    response.id,
                    msg.id,
                    started.id,
                    filename.id,
                    editfilename.id,
                    enterfilename.id,
                    cnfrm.id,
                    pdf.id,
                    convert.id,
                ],
            )
            await event.delete()
    except TimeoutError:
        return await event.edit(
            "**ERROR: @office2pdf_bot tidak merespon, coba lagi nanti**"
        )


CMD_HELP.update(
    {
        "pdf": "**Plugin : **`pdf`\
        \n\n  •  **Syntax :** `.pdf` <reply text>\
        \n  •  **Function : **Untuk Mengconvert teks menjadi file PDF menggunakan @office2pdf_bot\
    "
    }
)
