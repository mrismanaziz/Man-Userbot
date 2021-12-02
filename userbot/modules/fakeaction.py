# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# @SharingUserbot

import asyncio
import math
import time

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, extract_time, man_cmd


@man_cmd(
    pattern="f(typing|audio|contact|document|game|location|photo|round|sticker|video) ?(.*)"
)
async def _(e):
    act = e.pattern_match.group(1)
    t = e.pattern_match.group(2)
    if act in ["audio", "round", "video"]:
        act = "record-" + act
    if t.isdigit():
        t = int(t)
    elif t.endswith(("s", "h", "d", "m")):
        t = math.ceil((await extract_time(e, t)) - time.time())
    else:
        t = 60
    await edit_delete(e, f"**Memulai fake {act} selama** `{t}` **detik**", 3)
    async with e.client.action(e.chat_id, act):
        await asyncio.sleep(t)


CMD_HELP.update(
    {
        "fakeaction": f"**Plugin :** `fakeaction`\
        \n\n  •  **Syntax :** `{cmd}ftyping`  <jumlah detik>\
        \n  •  **Function :** Menampilkan Pengetikan Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}faudio` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Merekam suara Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fvideo` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Merekam Video Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fround` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Merekam Live Video Round Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fgame` <jumlah detik>\
        \n  •  **Function :** Menampilkan sedang bermain game Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fphoto` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Mengirim Photo Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fdocument` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Mengirim Document/File Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}flocation` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Share Lokasi Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fcontact` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Share Contact Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fsticker` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Memilih Sticker Palsu dalam obrolan\
    "
    }
)
