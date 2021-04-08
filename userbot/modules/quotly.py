import random
from asyncio.exceptions import TimeoutError

import requests
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register

if 1 == 1:
    strings = {
        "name": "Quotes",
        "api_token_cfg_doc": "API Key/Token for Quotes.",
        "api_url_cfg_doc": "API URL for Quotes.",
        "colors_cfg_doc": "Username colors",
        "default_username_color_cfg_doc": "Default color for the username.",
        "no_reply": "You didn't reply to a message.",
        "no_template": "You didn't specify the template.",
        "delimiter": "</code>, <code>",
        "server_error": "Server error. Please report to developer.",
        "invalid_token": "You've set an invalid token, get it from `http://antiddos.systems`.",
        "unauthorized": "You're unauthorized to do this.",
        "not_enough_permissions": "Wrong template. You can use only the default one.",
        "templates": "Available Templates: <code>{}</code>",
        "cannot_send_stickers": "`Anda Tidak Bisa Mengirim Pesan Ke Obrolan Ini.`",
        "admin": "admin",
        "creator": "creator",
        "hidden": "hidden",
        "channel": "Channel",
    }

    config = {
        "api_url": "http://api.antiddos.systems",
        "username_colors": [
            "#fb6169",
            "#faa357",
            "#b48bf2",
            "#85de85",
            "#62d4e3",
            "#65bdf3",
            "#ff5694",
        ],
        "default_username_color": "#b48bf2",
    }


@register(outgoing=True, pattern=r"^\.q")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Mohon Balas Ke Pesan```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Mohon Balas Ke Pesan```")
    chat = "@QuotLyBot"
    if reply_message.sender.bot:
        return await qotli.edit("```Mohon Balas Ke Pesan```")
    await qotli.edit("```Sedang Memproses Sticker, Mohon Menunggu```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1031952739)
                )
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply(
                    "```Harap Jangan Blockir @QuotLyBot Buka Blokir Lalu Coba Lagi```"
                )
            if response.text.startswith("Hi!"):
                await qotli.edit(
                    "```Mohon Menonaktifkan Pengaturan Privasi Forward Anda```"
                )
            else:
                await qotli.delete()
                await bot.forward_messages(qotli.chat_id, response.message)
                await bot.send_read_acknowledge(qotli.chat_id)
                """ - cleanup chat after completed - """
                await qotli.client.delete_messages(conv.chat_id, [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()


@register(outgoing=True, pattern="^.xquote(?: |$)(.*)")
async def quote_search(event):
    if event.fwd_from:
        return
    await event.edit("`Sedang Memproses...`")
    search_string = event.pattern_match.group(1)
    input_url = "https://bots.shrimadhavuk.me/Telegram/GoodReadsQuotesBot/?q={}".format(
        search_string
    )
    headers = {"USER-AGENT": "Uniborg"}
    try:
        response = requests.get(input_url, headers=headers).json()
    except BaseException:
        response = None
    if response is not None:
        result = (
            random.choice(response).get("input_message_content").get("message_text")
        )
    else:
        result = None
    if result:
        await event.edit(result.replace("<code>", "`").replace("</code>", "`"))
    else:
        await event.edit("`Tidak Ada Hasil Yang Ditemukan`")


CMD_HELP.update(
    {
        "quotly": "**Plugin : **`quotly`\
        \n\n  •  **Syntax :** `.q`\
        \n  •  **Function : **Membuat pesan mu menjadi sticker.\
        \n\n  •  **Syntax :** `.xquote`\
        \n  •  **Function : **Membuat pesan mu menjadi sticker.\
    "
    }
)
