# Man - UserBot
# Copyright (c) 2022 Man-Userbot
# Credits: @mrismanaziz || https://github.com/mrismanaziz
#
# This file is a part of < https://github.com/mrismanaziz/Man-Userbot/ >
# t.me/SharingUserbot & t.me/Lunatic0de

from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import BLACKLIST_CHAT
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, man_cmd


@man_cmd(pattern="kickme$", allow_sudo=False)
async def kickme(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**Perintah ini Dilarang digunakan di Group ini**"
        )
    user = await event.client.get_me()
    await edit_or_reply(event, f"`{user.first_name} has left this group, bye!!`")
    await event.client.kick_participant(event.chat_id, "me")


@man_cmd(pattern="kikme$", allow_sudo=False)
async def kikme(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**Perintah ini Dilarang digunakan di Group ini**"
        )
    await edit_or_reply(event, "**GC NYA JELEK GOBLOK KELUAR DULU AH CROTT** 🥴")
    await event.client.kick_participant(event.chat_id, "me")


@man_cmd(pattern="leaveall$", allow_sudo=False)
async def kickmeall(event):
    Man = await edit_or_reply(event, "`Global Leave from group chats...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await event.client(LeaveChannelRequest(chat))
            except BaseException:
                er += 1
    await Man.edit(
        f"**Berhasil Keluar dari {done} Group, Gagal Keluar dari {er} Group**"
    )


CMD_HELP.update(
    {
        "kickme": f"**Plugin : **`kickme`\
        \n\n  •  **Syntax :** `{cmd}kickme`\
        \n  •  **Function : **Keluar grup dengan menampilkan pesan Master has left this group, bye!!\
        \n\n  •  **Syntax :** `{cmd}kikme`\
        \n  •  **Function : **Keluar grup dengan menampilkan pesan GC NYA JELEK GOBLOK KELUAR DULU AH CROTT 🥴\
        \n\n  •  **Syntax :** `{cmd}leaveall`\
        \n  •  **Function : **Keluar dari semua grup telegram yang anda gabung.\
    "
    }
)
