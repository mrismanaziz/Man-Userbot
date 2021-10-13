# ReCode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd
from userbot.utils import edit_delete, edit_or_reply


@bot.on(man_cmd(outgoing=True, pattern=r"q ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(event, "**Mohon Balas ke Pesan**")
        return
    reply_message = await event.get_reply_message()
    warna = event.pattern_match.group(1)
    chat = "@QuotLyBot"
    await edit_or_reply(event, "`Processing...`")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            first = await conv.send_message(f"/qcolor {warna}")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("**Silahkan Unblock @QuotLyBot dan coba lagi!!**")
            return
        if response.text.startswith("Hi!"):
            await edit_or_reply(
                event, "**Mohon Menonaktifkan Pengaturan Privasi Forward Anda**"
            )
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
    await bot.delete_messages(conv.chat_id, [first.id, ok.id, second.id, response.id])


CMD_HELP.update(
    {
        "quotly": f"**Plugin : **`quotly`\
        \n\n  •  **Syntax :** `{cmd}q` <warna>\
        \n  •  **Function : **Membuat pesan mu menjadi sticker bisa custom warna background.\
    "
    }
)
