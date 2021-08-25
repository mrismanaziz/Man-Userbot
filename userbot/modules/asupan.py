# 🍀 © @tofik_dn
# ⚠️ Do not remove credits

import requests

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.asupan$")
async def _(event):
    try:
        response = requests.get("https://api-tede.herokuapp.com/api/asupan/ptl").json()
        await event.client.send_file(event.chat_id, response["url"])
        await event.delete()
    except Exception:
        await event.edit("**Tidak bisa menemukan video asupan.**")


@register(outgoing=True, pattern=r"^\.wibu$")
async def _(event):
    try:
        response = requests.get("https://api-tede.herokuapp.com/api/asupan/wibu").json()
        await event.client.send_file(event.chat_id, response["url"])
        await event.delete()
    except Exception:
        await event.edit("**Tidak bisa menemukan video wibu.**")


@register(outgoing=True, pattern=r"^\.chika$")
async def _(event):
    try:
        response = requests.get("https://api-tede.herokuapp.com/api/chika").json()
        await event.client.send_file(event.chat_id, response["url"])
        await event.delete()
    except Exception:
        await event.edit("**Tidak bisa menemukan video chikakiku.**")


CMD_HELP.update(
    {
        "asupan": "**Plugin : **`asupan`\
        \n\n  •  **Syntax :** `.asupan`\
        \n  •  **Function : **Untuk Mengirim video asupan secara random.\
        \n\n  •  **Syntax :** `.wibu`\
        \n  •  **Function : **Untuk Mengirim video wibu secara random.\
        \n\n  •  **Syntax :** `.chika`\
        \n  •  **Function : **Untuk Mengirim video chikakiku secara random.\
    "
    }
)
