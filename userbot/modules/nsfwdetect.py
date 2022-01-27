# Copyright (C) 2020  @deleteduser420 <https://github.com/code-rgb>
# ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import os

import requests

from userbot import CMD_HELP, DEEP_AI
from userbot.utils import edit_delete, edit_or_reply, man_cmd


@man_cmd(pattern="detect$")
async def detect(event):
    if DEEP_AI is None:
        return await edit_delete(
            event,
            "**Tambahkan VAR** `DEEP_AI` **dan ambil Api Key di web https://deepai.org/**",
            120,
        )
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "**Mohon Reply ke gambar atau stiker!**", 90)
    manevent = await edit_or_reply(event, "**MenDownload file untuk diperiksa...**")
    media = await event.client.download_media(reply)
    if not media.endswith(("png", "jpg", "webp")):
        return await edit_delete(event, "**Mohon Reply ke gambar atau stiker!**", 90)
    manevent = await edit_or_reply(event, "**Detecting NSFW limit...**")
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": DEEP_AI},
    )
    os.remove(media)
    if "status" in r.json():
        return await edit_delete(manevent, r.json()["status"])
    r_json = r.json()["output"]
    pic_id = r.json()["id"]
    percentage = r_json["nsfw_score"] * 100
    detections = r_json["detections"]
    link = f"https://api.deepai.org/job-view-file/{pic_id}/inputs/image.jpg"
    result = f"<b>Detected Nudity :</b>\n<a href='{link}'>>>></a> <code>{percentage:.3f}%</code>\n\n"
    if detections:
        for parts in detections:
            name = parts["name"]
            confidence = int(float(parts["confidence"]) * 100)
            result += f"<b>• {name}:</b>\n   <code>{confidence} %</code>\n"
    await edit_or_reply(
        manevent,
        result,
        link_preview=False,
        parse_mode="HTML",
    )


CMD_HELP.update(
    {
        "nsfw": "**Plugin : **`nsfw`\
        \n\n  •  **Syntax :** `.detect` <reply media>\
        \n  •  **Function : **Untuk mendeteksi konten 18+ dengan gambar balasan.\
    "
    }
)
