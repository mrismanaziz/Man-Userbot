# UniBorg (telegram userbot)
# Copyright (C) 2020 The Authors
# Ported from UniBorg by AnggaR96s

import os
from shutil import rmtree
from time import time

from deezloader import Login
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from requests import get
from telethon.tl.types import DocumentAttributeAudio

from userbot import CMD_HELP, DEEZER_ARL_TOKEN, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

if not TEMP_DOWNLOAD_DIRECTORY.endswith("/"):
    TEMP_DOWNLOAD_DIRECTORY += "/"


@register(outgoing=True, pattern=r"^\.deezloader (.*) (flac|320|256|128)")
async def deeznuts(event):
    if DEEZER_ARL_TOKEN is None:
        return await event.edit("**Set** `DEEZER_ARL_TOKEN` **first.**")

    try:
        loader = Login(DEEZER_ARL_TOKEN)
    except Exception as e:
        return await event.edit(f"**Error:** `{e}`")

    try:
        link = get(event.pattern_match.group(1)).url
    except BaseException:
        return await event.edit("**Error: Invalid link provided.**")

    quality = {"flac": "FLAC", "320": "MP3_320", "256": "MP3_256", "128": "MP3_128"}
    quality = quality[event.pattern_match.group(2)]

    temp_dl_path = os.path.join(TEMP_DOWNLOAD_DIRECTORY, str(time()))
    if not os.path.exists(temp_dl_path):
        os.makedirs(temp_dl_path)

    await event.edit("`Downloading...`")

    if "spotify" in link:
        if "track" in link:
            try:
                track = loader.download_trackspo(
                    link,
                    output=temp_dl_path,
                    quality=quality,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                )
            except Exception as e:
                return await event.edit(f"**Error:** `{e}`")
            await event.edit("`Uploading...`")
            await upload_track(track, event)
            rmtree(temp_dl_path)
            return await event.delete()

        if "album" in link:
            try:
                album = loader.download_albumspo(
                    link,
                    output=temp_dl_path,
                    quality=quality,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False,
                )
            except Exception as e:
                return await event.edit(f"**Error:** `{e}`")
            await event.edit("`Uploading...`")
            for track in album:
                await upload_track(track, event)
            rmtree(temp_dl_path)
            return await event.delete()

    if "deezer" in link:
        if "track" in link:
            try:
                track = loader.download_trackdee(
                    link,
                    output=temp_dl_path,
                    quality=quality,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                )
            except Exception as e:
                return await event.edit(f"**Error:** `{e}`")
            await event.edit("`Uploading...`")
            await upload_track(track, event)
            rmtree(temp_dl_path)
            return await event.delete()

        if "album" in link:
            try:
                album = loader.download_albumdee(
                    link,
                    output=temp_dl_path,
                    quality=quality,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False,
                )
            except Exception as e:
                return await event.edit(f"**Error:** `{e}`")
            await event.edit("`Uploading...`")
            for track in album:
                await upload_track(track, event)
            rmtree(temp_dl_path)
            return await event.delete()

    await event.edit("**Syntax error!\nRead** `.help deezloader`**.**")


async def upload_track(track_location, message):
    metadata = extractMetadata(createParser(track_location))
    duration = 0
    title = ""
    performer = ""
    if metadata.has("duration"):
        duration = metadata.get("duration").seconds
    if metadata.has("title"):
        title = metadata.get("title")
    if metadata.has("artist"):
        performer = metadata.get("artist")

    document_attributes = [
        DocumentAttributeAudio(
            duration=duration,
            voice=False,
            title=title,
            performer=performer,
            waveform=None,
        )
    ]

    if title and performer:
        track = f"{performer} - {title}"
    else:
        track = str(os.path.basename(track_location).rsplit(".", 1)[0])

    await message.edit(f"**Uploading...\nTrack:** {track}")

    await message.client.send_file(
        message.chat_id,
        track_location,
        caption=os.path.basename(track_location),
        force_document=False,
        supports_streaming=True,
        allow_cache=False,
        attributes=document_attributes,
    )
    os.remove(track_location)


CMD_HELP.update(
    {
        "deezloader": "**Plugin : **`deezloader`\
        \n\n  •  **Syntax :** `.deezloader` <spotify/deezer link> <quality>\
        \n  •  **Function : **Download  musik menggunakan Deezloader.\
        \n\n  •  **Available qualities:** `flac`, `320`, `256`, `128`\
    "
    }
)
