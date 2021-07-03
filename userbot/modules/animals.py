# Taken from
# https://github.com/AvinashReddy3108/PaperplaneRemix/blob/master/userbot/plugins/memes.py

# TG-UserBot - A modular Telegram UserBot script for Python.
# Copyright (C) 2019 Kandarp <https://github.com/kandnub>
#
# TG-UserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TG-UserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TG-UserBot.  If not, see <https://www.gnu.org/licenses/>.

import requests

from userbot import CMD_HELP
from userbot.events import register


@register(pattern=r"^\.shibe$", outgoing=True)
async def shibe(event):
    await event.edit("`Processing...`")
    response = requests.get("https://shibe.online/api/shibes").json()
    if not response:
        await event.edit("**Tidak bisa menemukan Anjing.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await event.delete()


@register(pattern=r"^\.cat$", outgoing=True)
async def cats(event):
    await event.edit("`Processing...`")
    response = requests.get("https://shibe.online/api/cats").json()
    if not response:
        await event.edit("**Tidak bisa menemukan kucing.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await event.delete()


CMD_HELP.update(
    {
        "animals": "**Plugin : **`animals`\
        \n\n  •  **Syntax :** `.cat`\
        \n  •  **Function : **Untuk Mengirim gambar kucing secara random.\
        \n\n  •  **Syntax :** `.shibe`\
        \n  •  **Function : **Untuk Mengirim gambar random dari anjing jenis Shiba.\
    "
    }
)
