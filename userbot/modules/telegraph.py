# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register

telegraph = Telegraph()
r = telegraph.create_account(short_name="telegraph")
auth_url = r["auth_url"]


@register(outgoing=True, pattern=r"^\.tg (m|t)$")
async def telegraphs(graph):
    await graph.edit("`Processing...`")
    if not graph.text[0].isalpha() and graph.text[0] not in ("/", "#", "@", "!"):
        if graph.fwd_from:
            return
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        if graph.reply_to_msg_id:
            start = datetime.now()
            r_message = await graph.get_reply_message()
            input_str = graph.pattern_match.group(1)
            if input_str == "m":
                downloaded_file_name = await bot.download_media(
                    r_message, TEMP_DOWNLOAD_DIRECTORY
                )
                end = datetime.now()
                ms = (end - start).seconds
                await graph.edit(
                    "Di Download Ke {} Dalam {} Detik.".format(downloaded_file_name, ms)
                )
                try:
                    if downloaded_file_name.endswith((".webp")):
                        resize_image(downloaded_file_name)
                except AttributeError:
                    return await graph.edit("`Tidak Ada Media Yang Disediakan`")
                try:
                    start = datetime.now()
                    media_urls = upload_file(downloaded_file_name)
                except exceptions.TelegraphException as exc:
                    await graph.edit("ERROR: " + str(exc))
                    os.remove(downloaded_file_name)
                else:
                    end = datetime.now()
                    ms_two = (end - start).seconds
                    os.remove(downloaded_file_name)
                    await graph.edit(
                        "**Berhasil Mengunggah Ke** [Telegraph](https://telegra.ph{}).".format(
                            media_urls[0], (ms + ms_two)
                        ),
                        link_preview=True,
                    )
            elif input_str == "t":
                user_object = await bot.get_entity(r_message.from_id)
                title_of_page = user_object.first_name  # + " " + user_object.last_name
                # apparently, all Users do not have last_name field
                page_content = r_message.message
                if r_message.media:
                    if page_content != "":
                        title_of_page = page_content
                    downloaded_file_name = await bot.download_media(
                        r_message, TEMP_DOWNLOAD_DIRECTORY
                    )
                    m_list = None
                    with open(downloaded_file_name, "rb") as fd:
                        m_list = fd.readlines()
                    for m in m_list:
                        page_content += m.decode("UTF-8") + "\n"
                    os.remove(downloaded_file_name)
                page_content = page_content.replace("\n", "<br>")
                response = telegraph.create_page(
                    title_of_page, html_content=page_content
                )
                end = datetime.now()
                ms = (end - start).seconds
                await graph.edit(
                    "**Berhasil Mengunggah Ke** [Telegraph](https://telegra.ph/{}).".format(
                        response["path"], ms
                    ),
                    link_preview=True,
                )
        else:
            await graph.edit(
                "`Mohon Balas Ke Pesan, Untuk Mendapatkan Link Telegraph Permanen.`"
            )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CMD_HELP.update(
    {
        "telegraph": ">`.tg` <m|t>"
        "\nUsage: Mengunggah t(Teks) Atau m(Media) Ke Telegraph."
    }
)

CMD_HELP.update(
    {
        "telegraph": "**Plugin : **`telegraph`\
        \n\n  •  **Syntax :** `.tg` m\
        \n  •  **Function : **Mengunggah m(Media) Ke Telegraph.\
        \n\n  •  **Syntax :** `.tg` t\
        \n  •  **Function : **Mengunggah t(Teks) Ke Telegraph.\
    "
    }
)
