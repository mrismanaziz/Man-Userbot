# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Thanks to @kandnub, for this awesome module !!
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for reverse searching stickers and images on Google """

import io
import os
import shutil
import urllib

import requests
from bs4 import BeautifulSoup
from PIL import Image

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.utils import edit_delete, edit_or_reply, googleimagesdownload, man_cmd

opener = urllib.request.build_opener()
useragent = (
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/80.0.3987.149 Mobile Safari/537.36"
)
opener.addheaders = [("User-agent", useragent)]


@man_cmd(pattern="reverse(?: |$)(\d*)")
async def okgoogle(img):
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    message = await img.get_reply_message()
    if not message or not message.media:
        return await edit_delete(img, "**Reply ke foto atau stiker.**")
    photo = io.BytesIO()
    await bot.download_media(message, photo)
    if not photo:
        return await edit_delete(img, "**Gagal mendownload gambar.**")
    xx = await edit_or_reply(img, "`Processing...`")
    try:
        image = Image.open(photo)
    except OSError:
        return await xx.edit("`sexuality tidak didukung, kemungkinan besar.`")
    name = "okgoogle.png"
    image.save(name, "PNG")
    image.close()
    # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
    searchUrl = "https://www.google.com/searchbyimage/upload"
    multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers["Location"]
    if response == 400:
        return await xx.edit("`Google menyuruhku pergi.`")
    await xx.edit(
        "**Image successfully uploaded to Google. Maybe.**"
        "\n**Parsing source now. Maybe.**"
    )
    os.remove(name)
    match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
    guess = str(match["best_guess"])
    imgspage = match["similar_images"]
    if not guess and not imgspage:
        return await xx.edit("`Tidak dapat menemukan apa pun untuk si jelek.`")
    try:
        counter = int(img.pattern_match.group(1))
    except BaseException:
        counter = int(3)
    counter = int(10) if counter > 10 else counter
    counter = int(3) if counter < 0 else counter
    if counter == 0:
        return await xx.edit(
            f"**Best match:** `{guess}`\
                              \n\n[Visually similar images]({fetchUrl})\
                              \n\n[Results for {guess}]({imgspage})"
        )
    await xx.edit(
        f"**Best match:** `{guess}`\
                   \n\n[Visually similar images]({fetchUrl})\
                   \n\n[Results for {guess}]({imgspage})\
                   \n\n**Fetching images...**"
    )
    response = googleimagesdownload()
    # creating list of arguments
    arguments = {
        "keywords": guess,
        "limit": counter,
        "format": "png",
        "no_directory": "no_directory",
    }
    try:
        paths = response.download(arguments)
    except Exception as e:
        return await xx.edit(
            f"**Best match:** `{guess}`\
                              \n\n[Visually similar images]({fetchUrl})\
                              \n\n[Results for {guess}]({imgspage})\
                              \n\n**Error:** `{e}`**.**"
        )
    lst = paths[0][guess]
    await img.client.send_file(
        entity=img.chat_id,
        file=lst,
        reply_to=img,
    )
    await xx.edit(
        f"**Best match:** `{guess}`\
                   \n\n[Visually similar images]({fetchUrl})\
                   \n\n[Results for {guess}]({imgspage})"
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))


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

    results["best_guess"] = results["best_guess"][12:]
    return results


CMD_HELP.update(
    {
        "reverse": f"**Plugin : **`reverse`\
        \n\n  •  **Syntax :** `{cmd}reverse` <jumlah>\
        \n  •  **Function : **Balas gambar/stiker untuk melakukan pencarian terbalik di google/\
        \n\n  •  **NOTE :** Hasil Reverse dapat ditentukan, defaultnya adalah 3. Jika penghitung adalah 0, hanya info dan tautan yang akan diberikan. Bot mungkin saja gagal mengunggah gambar jika hasil yang di minta terlalu banyak.\
    "
    }
)
