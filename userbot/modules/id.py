# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

from PIL import Image, ImageDraw, ImageFont

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.id$")
async def image_maker(event):
    replied_user = await event.get_reply_message()
    await event.client.download_profile_photo(
        replied_user.from_id, file="user.png", download_big=True
    )
    user_photo = Image.open("user.png")
    id_template = Image.open("userbot/resources/FrameID.png")
    user_photo = user_photo.resize((989, 1073))
    id_template.paste(user_photo, (1229, 573))
    position = (2473, 481)
    draw = ImageDraw.Draw(id_template)
    color = "rgb(23, 43, 226)"  # red color
    font = ImageFont.truetype("userbot/resources/fontx.ttf", size=200)
    draw.text(
        position,
        replied_user.sender.first_name.replace("\u2060", ""),
        fill=color,
        font=font,
    )
    id_template.save("user_id.png")
    await event.edit("`Membuat ID Card..`")
    await event.client.send_message(
        event.chat_id,
        "Generated User ID",
        reply_to=event.message.reply_to_msg_id,
        file="user_id.png",
        force_document=False,
        silent=True,
    )
    await event.delete()


CMD_HELP.update(
    {
        "id": "**Plugin : **`id`\
        \n\n  •  **Syntax :** `.id`\
        \n  •  **Function : **Balas ke pengguna untuk menghasilkan Kartu ID.\
    "
    }
)
