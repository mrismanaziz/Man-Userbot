# ReCode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, edit_or_reply, man_cmd


@man_cmd(pattern="q ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        return await edit_delete(event, "**Mohon Balas ke Pesan**")
    reply_message = await event.get_reply_message()
    warna = event.pattern_match.group(1)
    chat = "@QuotLyBot"
    xx = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            first = await conv.send_message(f"/qcolor {warna}")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            first = await conv.send_message(f"/qcolor {warna}")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await event.client.forward_messages(chat, reply_message)
            response = await response
        if response.text.startswith("Hi!"):
            await xx.edit("**Mohon Menonaktifkan Pengaturan Privasi Forward Anda**")
        else:
            await xx.delete()
            await event.client.send_file(event.chat_id, response.message)
    await event.client.delete_messages(
        conv.chat_id, [first.id, ok.id, second.id, response.id]
    )


CMD_HELP.update(
    {
        "quotly": f"**Plugin : **`quotly`\
        \n\n  •  **Syntax :** `{cmd}q` <warna>\
        \n  •  **Function : **Membuat pesan mu menjadi sticker bisa custom warna background.\
    "
    }
)
