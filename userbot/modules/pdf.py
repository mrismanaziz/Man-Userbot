# Copyright (C) 2021 Man-Userbot
# Created by mrismanaziz
# FROM <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="pdf(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await edit_or_reply(event, "**Mohon Reply ke teks apa pun**")
    reply_message = await event.get_reply_message()
    chat = "@office2pdf_bot"
    xx = await edit_or_reply(event, "`Mengubah menjadi PDF...`")
    try:
        async with event.client.conversation(chat) as conv:
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
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.client(UnblockRequest(chat))
                return await xx.edit(
                    "**Silahkan Unblock @office2pdf_bot dan coba lagi**"
                )
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
            await xx.delete()
    except TimeoutError:
        return await xx.edit(
            "**ERROR: @office2pdf_bot tidak merespon, coba lagi nanti**"
        )


CMD_HELP.update(
    {
        "pdf": f"**Plugin : **`pdf`\
        \n\n  •  **Syntax :** `{cmd}pdf` <reply text>\
        \n  •  **Function : **Untuk Mengconvert teks menjadi file PDF menggunakan @office2pdf_bot\
    "
    }
)
