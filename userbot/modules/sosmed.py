# Port by Koala 🐨/@manuskarakitann
# Nyenyenye bacot

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.sosmed ?(.*)")
async def insta(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Balas Ke Link Untuk Download.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`Mohon Berikan Link yang ingin di download...`")
        return
    chat = "@SaveAsbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("`Processing...`")
        return
    await event.edit("`Processing Download...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("`Mohon Unblock dulu` @SaveAsbot'u ")
            return
        if response.text.startswith("Forward"):
            await event.edit("Forward Private .")
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"**Support** @sharinguserbot",
            )
            await event.client.send_read_acknowledge(conv.chat_id)
            await bot(functions.messages.DeleteHistoryRequest(peer=chat, max_id=0))
            await event.delete()


@register(outgoing=True, pattern="^.dez(?: |$)(.*)")
async def DeezLoader(event):
    if event.fwd_from:
        return
    dlink = event.pattern_match.group(1)
    if ".com" not in dlink:
        await event.edit("`Mohon Berikan Link Deezloader yang ingin di download`")
    else:
        await event.edit("`Sedang Mendownload Lagu...`")
    chat = "@DeezLoadBot"
    async with bot.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message(dlink)
            details = await conv.get_response()
            song = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("@DeezLoadBot'Unblok Dulu La Asu.")
            return
        await bot.send_file(event.chat_id, song, caption=details.text)


CMD_HELP.update(
    {
        "sosmed": "**Plugin : **`sosmed`\
        \n\n  •  **Syntax :** `.sosmed` <link>`\
        \n  •  **Function : **Download Media Dari Pinterest / Tiktok / Instagram.\
        \n\n  •  **Syntax :** `.dez` <link>\
        \n  •  **Function : **Download Lagu Via Deezloader\
    "
    }
)
