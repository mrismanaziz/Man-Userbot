# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import asyncio
import io
import os
import re
import sys
import urllib
from os import environ, execle
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup
from PIL import Image

from userbot import (
    ALIVE_NAME,
    BOT_VER,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    UPSTREAM_REPO_BRANCH,
    bot,
)
from userbot.events import register
from userbot.utils import time_formatter

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.70 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit(
        "**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`"
    )


@register(outgoing=True, pattern=r"^\.sleep ([0-9]+)$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern=r"^\.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Mematikan Man-Userbot....`")
    await asyncio.sleep(7)
    await event.delete()
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#SHUTDOWN \n" "`Userbot Telah Dimatikan`"
        )
    await bot.disconnect()


@register(outgoing=True, pattern=r"^\.restart$")
async def killdabot(event):
    await event.edit("`Restarting Man-Userbot...`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#RESTARTBOT \n" "`Man-Userbot Telah Di Restart`"
        )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@register(outgoing=True, pattern=r"^\.readme$")
async def reedme(e):
    await e.edit(
        "Here's something for you to read :\n"
        "\n[Userbot Repo](https://github.com/mrismanaziz/Man-Userbot/blob/Man-Userbot/README.md)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Setup Guide - Google Drive](https://telegra.ph/How-To-Setup-GDrive-11-02)"
        "\n[Setup Guide - LastFM Module](https://telegra.ph/How-to-set-up-LastFM-module-for-Paperplane-userbot-11-02)"
        "\n[Video Tutorial - 576p](https://mega.nz/#!ErwCESbJ!1ZvYAKdTEfb6y1FnqqiLhHH9vZg4UB2QZNYL9fbQ9vs)"
        "\n[Video Tutorial - 1080p](https://mega.nz/#!x3JVhYwR!u7Uj0nvD8_CyyARrdKrFqlZEBFTnSVEiqts36HBMr-o)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)"
    )


@register(outgoing=True, pattern=r"^\.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        f"**Hey**, __I am using__ 🔥 **Man-Userbot** 🔥\n\n"
        f"      __Thanks For Using me__\n\n"
        f"✣ **Userbot Version :** `{BOT_VER}@{UPSTREAM_REPO_BRANCH}`\n"
        f"✣ **Group Support :** [Sharing Userbot](t.me/sharinguserbot)\n"
        f"✣ **Owner Repo :** [Risman](t.me/mrismanaziz)\n"
        f"✣ **Repo :** [Man-Userbot](https://github.com/mrismanaziz/Man-Userbot)\n"
    )


@register(outgoing=True, pattern="^.string$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        f"✥ **GET STRING SESSION TELEGRAM :** [KLIK DISINI](https://repl.it/@mrismanaziz/stringenSession?lite=1&outputonly=1)\n"
    )


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit("`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`",
        )


@register(outgoing=True, pattern=r"^.reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, Google search images and stickers. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await bot.download_media(message, photo)
    else:
        await img.edit("`Harap Balas Di Gambar`")
        return

    if photo:
        await img.edit("`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            await img.edit("`Gambar tidak di dukung`")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]

        if response != 400:
            await img.edit(
                "`Image successfully uploaded to Google. Maybe.`"
                "\n`Parsing source now. Maybe.`"
            )
        else:
            await img.edit("`Google told me to fuck off.`")
            return

        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]

        if guess and imgspage:
            await img.edit(f"[{guess}]({fetchUrl})\n\n`Looking for images...`")
        else:
            await img.edit("`Couldn't find anything for your uglyass.`")
            return

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(
                entity=await img.client.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await img.edit(
            f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})"
        )


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "best_guess": ""}

    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    return results


async def scam(results, lim):

    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")

    imglinks = []
    counter = 0

    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        if not counter >= int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks


@register(outgoing=True, pattern=r"^\.send (.*)")
async def send(event):
    await event.edit("`Processing...`")

    if not event.is_reply:
        return await event.edit("`Mohon Balas ke pesan!`")

    chat = event.pattern_match.group(1)
    try:
        chat = await event.client.get_entity(chat)
    except (TypeError, ValueError):
        return await event.edit("`Link yang diberikan tidak valid!`")

    message = await event.get_reply_message()

    await event.client.send_message(entity=chat, message=message)
    await event.edit(f"`Mengirim pesan ini ke` `{chat.title}``!`")


CMD_HELP.update(
    {
        "send": "**Plugin : **`send`\
        \n\n  •  **Syntax :** `.send`\
        \n  •  **Function : **Meneruskan pesan balasan ke obrolan tertentu tanpa tag Forwarded from. \
    "
    }
)

CMD_HELP.update(
    {
        "random": "**Plugin : **`random`\
        \n\n  •  **Syntax :** `.random`\
        \n  •  **Function : **Dapatkan item acak dari daftar item. \
    "
    }
)

CMD_HELP.update(
    {
        "sleep": "**Plugin : **`sleep`\
        \n\n  •  **Syntax :** `.sleep`\
        \n  •  **Function : **Biarkan Man-Userbot tidur selama beberapa detik \
    "
    }
)


CMD_HELP.update(
    {
        "repo": "**Plugin : **`Repository Man-Userbot`\
        \n\n  •  **Syntax :** `.repo`\
        \n  •  **Function : **Menampilan link Repository Man-Userbot\
        \n\n  •  **Syntax :** `.string`\
        \n  •  **Function : **Menampilan link String Man-Userbot\
    "
    }
)


CMD_HELP.update(
    {
        "readme": "**Plugin : **`Panduan Menggunakan userbot`\
        \n\n  •  **Syntax :** `.readme`\
        \n  •  **Function : **Menyediakan tautan untuk mengatur userbot dan modulnya\
    "
    }
)


CMD_HELP.update(
    {
        "restart": "**Plugin : **`Restart Man-Userbot`\
        \n\n  •  **Syntax :** `.restart`\
        \n  •  **Function : **Untuk Merestart userbot.\
    "
    }
)


CMD_HELP.update(
    {
        "shutdown": "**Plugin : **`shutdown`\
        \n\n  •  **Syntax :** `.shutdown`\
        \n  •  **Function : **Mematikan Userbot.\
    "
    }
)


CMD_HELP.update(
    {
        "raw": "**Plugin : **`raw`\
        \n\n  •  **Syntax :** `.raw`\
        \n  •  **Function : **Dapatkan data berformat seperti JSON terperinci tentang pesan yang dibalas.\
    "
    }
)


CMD_HELP.update(
    {
        "repeat": "**Plugin : **`repeat`\
        \n\n  •  **Syntax :** `.repeat`\
        \n  •  **Function : **Mengulangi teks untuk beberapa kali. Jangan bingung ini dengan spam tho.\
    "
    }
)
