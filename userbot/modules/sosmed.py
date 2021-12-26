# Port by Koala 🐨/@manuskarakitann
# Nyenyenye bacot

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.utils import edit_delete, edit_or_reply, man_cmd


@man_cmd(pattern="sosmed ?(.*)")
async def insta(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(event, "`Balas Ke Link Untuk Download.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await edit_delete(event, "`Mohon Berikan Link yang ingin di download...`")
        return
    chat = "@SaveAsbot"
    if reply_message.sender.bot:
        await edit_or_reply(event, "`Processing...`")
        return
    xx = await edit_or_reply(event, "`Processing Download...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        if response.text.startswith("Forward"):
            await xx.edit("Forward Private .")
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
            )
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client(functions.messages.DeleteHistoryRequest(peer=chat, max_id=0))
            await event.delete()


@man_cmd(pattern="dez(?: |$)(.*)")
async def DeezLoader(event):
    if event.fwd_from:
        return
    dlink = event.pattern_match.group(1)
    if ".com" not in dlink:
        await edit_delete(event, "`Mohon Berikan Link Deezloader yang ingin di download`")
    else:
        await edit_or_reply(event, "`Sedang Mendownload Lagu...`")
    chat = "@DeezLoadBot"
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message(dlink)
            details = await conv.get_response()
            song = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message(dlink)
            details = await conv.get_response()
            song = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(event.chat_id, song, caption=details.text)
        await event.delete()


CMD_HELP.update(
    {
        "sosmed": f"**Plugin : **`sosmed`\
        \n\n  •  **Syntax :** `{cmd}sosmed` <link>\
        \n  •  **Function : **Download Media Dari Pinterest / Tiktok / Instagram.\
        \n\n  •  **Syntax :** `{cmd}dez` <link>\
        \n  •  **Function : **Download Lagu Via Deezloader\
    "
    }
)
