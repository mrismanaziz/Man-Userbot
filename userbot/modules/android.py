# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import asyncio
import math
import os
import re
import time

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from requests import get

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.utils import (
    chrome,
    human_to_bytes,
    humanbytes,
    man_cmd,
    md5,
    time_formatter,
)

GITHUB = "https://github.com"
DEVICES_DATA = (
    "https://raw.githubusercontent.com/androidtrackers/"
    "certified-android-devices/master/by_device.json"
)


@man_cmd(pattern="magisk$")
async def magisk(request):
    """magisk latest releases"""
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/beta.json",
        "Canary": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/canary.json",
    }
    releases = "**Latest Magisk Releases :**\n"
    async with ClientSession() as ses:
        for name, release_url in magisk_dict.items():
            async with ses.get(release_url) as resp:
                data = await resp.json(content_type="text/plain")
                version = data["magisk"]["version"]
                version_code = data["magisk"]["versionCode"]
                note = data["magisk"]["note"]
                url = data["magisk"]["link"]
                releases += (
                    f"**{name}** - __v{version} ({version_code})__ : "
                    f"[APK]({url}) | [Note]({note})\n"
                )
    await request.edit(releases)


@man_cmd(pattern=r"device(?: |$)(\S*)")
async def device_info(request):
    """get android device basic info from its codename"""
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text
    else:
        return await request.edit("`Usage: .device <codename> / <model>`")
    try:
        found = get(DEVICES_DATA).json()[device]
    except KeyError:
        reply = f"`Couldn't find info about {device}!`\n"
    else:
        reply = f"Search results for {device}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = device
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**Codename**: `{codename}`\n"
                f"**Model**: {model}\n\n"
            )
    await request.edit(reply)


@man_cmd(pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    """search for android codename"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await request.edit("`Usage: .codename <brand> <device>`")
    found = [
        i
        for i in get(DEVICES_DATA).json()
        if i["brand"].lower() == brand and device in i["name"].lower()
    ]
    if len(found) > 8:
        found = found[:8]
    if found:
        reply = f"Search results for {brand.capitalize()} {device.capitalize()}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = item["device"]
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**Codename**: `{codename}`\n"
                f"**Model**: {model}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await request.edit(reply)


@man_cmd(pattern="pixeldl(?: |$)(.*)")
async def download_api(dl):
    await dl.edit("`Collecting information...`")
    URL = dl.pattern_match.group(1)
    URL_MSG = await dl.get_reply_message()
    if URL:
        pass
    elif URL_MSG:
        URL = URL_MSG.text
    else:
        await dl.edit("`Empty information...`")
        return
    if not re.findall(r"\bhttps?://download.*pixelexperience.*\.org\S+", URL):
        await dl.edit("`Invalid information...`")
        return
    driver = await chrome()
    await dl.edit("`Getting information...`")
    driver.get(URL)
    error = driver.find_elements_by_class_name("swal2-content")
    if len(error) > 0 and error[0].text == "File Not Found.":
        await dl.edit(f"`FileNotFoundError`: {URL} is not found.")
        return
    datas = driver.find_elements_by_class_name("download__meta")
    """ - enumerate data to make sure we download the matched version - """
    md5_origin = None
    i = None
    for index, value in enumerate(datas):
        for data in value.text.split("\n"):
            if data.startswith("MD5"):
                md5_origin = data.split(":")[1].strip()
                i = index
                break
        if md5_origin is not None and i is not None:
            break
    if md5_origin is None and i is None:
        await dl.edit("`There is no match version available...`")
    file_name = URL.split("/")[-2] if URL.endswith("/") else URL.split("/")[-1]
    file_path = TEMP_DOWNLOAD_DIRECTORY + file_name
    download = driver.find_elements_by_class_name("download__btn")[i]
    download.click()
    await dl.edit("`Starting download...`")
    file_size = human_to_bytes(download.text.split(None, 2)[-1].strip("()"))
    display_message = None
    complete = False
    start = time.time()
    while not complete:
        if os.path.isfile(file_path + ".crdownload"):
            try:
                downloaded = os.stat(file_path + ".crdownload").st_size
                status = "Downloading"
            except OSError:  # Rare case
                await asyncio.sleep(1)
                continue
        elif os.path.isfile(file_path):
            downloaded = os.stat(file_path).st_size
            file_size = downloaded
            status = "Checking"
        else:
            await asyncio.sleep(0.3)
            continue
        diff = time.time() - start
        percentage = downloaded / file_size * 100
        speed = round(downloaded / diff, 2)
        eta = round((file_size - downloaded) / speed)
        prog_str = "`{0}` | [{1}{2}] `{3}%`".format(
            status,
            "".join("●" for i in range(math.floor(percentage / 10))),
            "".join("○" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        current_message = (
            "`[DOWNLOAD]`\n\n"
            f"`{file_name}`\n"
            f"`Status`\n{prog_str}\n"
            f"`{humanbytes(downloaded)} of {humanbytes(file_size)}"
            f" @ {humanbytes(speed)}`\n"
            f"`ETA` -> {time_formatter(eta)}"
        )
        if (
            round(diff % 15.00) == 0
            and display_message != current_message
            or (downloaded == file_size)
        ):
            await dl.edit(current_message)
            display_message = current_message
        if downloaded == file_size:
            if not os.path.isfile(file_path):  # Rare case
                await asyncio.sleep(1)
                continue
            MD5 = await md5(file_path)
            if md5_origin == MD5:
                complete = True
            else:
                await dl.edit("`Download corrupt...`")
                os.remove(file_path)
                driver.quit()
                return
    await dl.respond(f"`{file_name}`\n\n" f"Successfully downloaded to `{file_path}`.")
    await dl.delete()
    driver.quit()
    return


@man_cmd(pattern=r"specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    """Mobile devices specifications"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await request.edit("`Usage: .specs <brand> <device>`")
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml"
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.edit(f"`{brand} is unknown brand!`")
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.edit(f"`can't find {device}!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n**" + info.title.text.split("-")[0].strip() + "**\n\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await request.edit(reply)


@man_cmd(pattern=r"twrp(?: |$)(\S*)")
async def twrp(request):
    """get android device twrp"""
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        return await request.edit("`Usage: .twrp <codename>`")
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        return await request.edit(reply)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.edit(reply)


CMD_HELP.update(
    {
        "android": f"**Plugin : **`android`\
        \n\n  •  **Syntax :** `{cmd}magisk`\
        \n  •  **Function : **Dapatkan rilis Magisk terbaru \
        \n\n  •  **Syntax :** `{cmd}device <codename>`\
        \n  •  **Function : **Dapatkan info tentang nama kode atau model perangkat android. \
        \n\n  •  **Syntax :** `{cmd}codename <brand> <device>`\
        \n  •  **Function : **Cari nama kode perangkat android. \
        \n\n  •  **Syntax :** `{cmd}pixeldl` **<download.pixelexperience.org>**\
        \n  •  **Function : **Unduh ROM pengalaman piksel ke server bot pengguna Anda. \
        \n\n  •  **Syntax :** `{cmd}specs <brand> <device>`\
        \n  •  **Function : **Dapatkan info spesifikasi perangkat. \
        \n\n  •  **Syntax :** `{cmd}twrp <codename>`\
        \n  •  **Function : **Dapatkan unduhan twrp terbaru untuk perangkat android. \
    "
    }
)
