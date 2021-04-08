# Copyright (C) 2020 Aidil Aryanto.
# DeeezLoad Ported from UniBorg by AnggaR96s
# All rights reserved.

import asyncio
import glob
import os
import shutil
import subprocess
import time

import deezloader
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pylast import User
from selenium import webdriver
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo

from userbot import (
    CMD_HELP,
    DEEZER_ARL_TOKEN,
    GOOGLE_CHROME_BIN,
    LASTFM_USERNAME,
    TEMP_DOWNLOAD_DIRECTORY,
    bot,
    lastfm,
)
from userbot.events import register
from userbot.utils import progress

os.system("rm -rf *.mp3")


def bruh(name):
    os.system("instantmusic -q -s " + name)


@register(outgoing=True, pattern=r"^\.song (.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Sedang Mencari Lagu Anda....`")
    elif reply.message:
        query = reply.message
        await event.edit("`Sedang Mencari Lagu Anda....`")
    else:
        await event.edit("`Apa Yang Harus Saya Cari`")
        return

    getmusic(str(query), "320k")
    l = glob.glob("*.mp3")
    loa = l[0]
    img_extensions = ["webp", "jpg", "jpeg", "webp"]
    img_filenames = [
        fn_img
        for fn_img in os.listdir()
        if any(fn_img.endswith(ext_img) for ext_img in img_extensions)
    ]
    thumb_image = img_filenames[0]
    await event.edit("`Sedang Mengunggah Lagu Anda....`")
    c_time = time.time()
    await event.client.send_file(
        event.chat_id,
        loa,
        force_document=True,
        thumb=thumb_image,
        allow_cache=False,
        caption=query,
        reply_to=reply_to_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]", loa)
        ),
    )
    await event.delete()
    os.system("rm -rf *.mp3")
    os.remove(thumb_image)
    subprocess.check_output("rm -rf *.mp3", shell=True)


async def getmusicvideo(cat):
    video_link = ""
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    command = 'youtube-dl -f "[filesize<50M]" --merge-output-format mp4 ' + video_link
    os.system(command)


def getmusic(get, DEFAULT_AUDIO_QUALITY):
    search = get

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    html = requests.get(
        "https://www.youtube.com/results?search_query=" + search, headers=headers
    ).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "/watch?v=" in link.get("href"):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get("href")
            break

    video_link = "http://www.youtube.com/" + video_link
    command = (
        "youtube-dl --write-thumbnail --extract-audio --audio-format mp3 --audio-quality "
        + DEFAULT_AUDIO_QUALITY
        + " "
        + video_link
    )
    os.system(command)


async def getmusic(cat):
    video_link = ""
    search = cat
    driver = await chrome()
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    command = f'youtube-dl --write-thumbnail --extract-audio --audio-format mp3 --audio-quality "320k" {video_link}'
    os.system(command)


def getmusicvideo(cat):
    search = cat
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    html = requests.get(
        "https://www.youtube.com/results?search_query=" + search, headers=headers
    ).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "/watch?v=" in link.get("href"):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get("href")
            break
    video_link = "http://www.youtube.com/" + video_link
    command = 'youtube-dl -f "[filesize<50M]" --merge-output-format mp4 ' + video_link
    os.system(command)


@register(outgoing=True, pattern=r"^\.musik (.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Mohon Menunggu, Sedang Mencari Musik Anda `")
    elif reply.message:
        query = reply.message
        await event.edit("`Telah Mendapatkan Musik, Sedang Mengunggah.....`")
    else:
        await event.edit("`Apa Yang Seharusnya Saya Temukan? `")
        return

    await getmusic(str(query))
    l = glob.glob("*.mp3")
    loa = l[0]
    metadata = extractMetadata(createParser(loa))
    duration = 0
    if metadata.has("duration"):
        duration = metadata.get("duration").seconds
    performer = loa.split("-")[0][0:-1]
    title = loa.split("-")[1][1:]
    img_extensions = ["webp", "jpg", "jpeg", "webp"]
    img_filenames = [
        fn_img
        for fn_img in os.listdir()
        if any(fn_img.endswith(ext_img) for ext_img in img_extensions)
    ]
    thumb_image = img_filenames[0]
    await event.edit("`Pengunggahan Berhasil Dilakukan `")
    c_time = time.time()
    await event.client.send_file(
        event.chat_id,
        loa,
        attributes=[
            DocumentAttributeAudio(duration=duration, title=title, performer=performer)
        ],
        thumb=thumb_image,
        allow_cache=False,
        caption=query,
        reply_to=reply_to_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]", loa)
        ),
    )
    await event.delete()
    os.system("rm -rf *.mp3")
    os.remove(thumb_image)
    subprocess.check_output("rm -rf *.mp3", shell=True)


@register(outgoing=True, pattern=r"^\.net (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit("`Terjadi Kesalahan.`")
        artist = playing.get_artist()
        song = playing.get_title()
    else:
        artist = event.pattern_match.group(2)
        song = event.pattern_match.group(3)
    track = str(artist) + " - " + str(song)
    chat = "@WooMaiBot"
    link = f"/netease {track}"
    await event.edit("`Sedang Mencari...`")
    try:
        async with bot.conversation(chat) as conv:
            await asyncio.sleep(2)
            await event.edit("`Memproses... Mohon Menunggu`")
            try:
                msg = await conv.send_message(link)
                response = await conv.get_response()
                respond = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("`Mohon Unblock @WooMaiBot Dan Coba Lagi`")
                return
            await event.edit("`Mengirim Musik Anda.....`")
            await asyncio.sleep(3)
            await bot.send_file(event.chat_id, respond)
        await event.client.delete_messages(
            conv.chat_id, [msg.id, response.id, respond.id]
        )
        await event.delete()
    except TimeoutError:
        return await event.edit("`Sedang Error`")


@register(outgoing=True, pattern=r"^\.vsong(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Mohon Menunggu, Sedang Mencari Video Anda....`")
    elif reply.message:
        query = reply.message
        await event.edit("`Mohon Menunggu, Sedang Mencari Video Anda....`")
    else:
        await event.edit("`Apa Yang Harus Saya Temukan?`")
        return
    getmusicvideo(query)
    l = glob.glob(("*.mp4")) + glob.glob(("*.mkv")) + glob.glob(("*.webm"))
    if l:
        await event.edit("`Yaps.. Saya Menemukannya...`")
    else:
        await event.edit(f"Maaf..! Saya Tidak Menemukan Apapun Pencarian `{query}`")
    loa = l[0]
    metadata = extractMetadata(createParser(loa))
    duration = 0
    width = 0
    height = 0
    if metadata.has("duration"):
        duration = metadata.get("duration").seconds
    if metadata.has("width"):
        width = metadata.get("width")
    if metadata.has("height"):
        height = metadata.get("height")
    await event.edit("`Mengunggah Video.. Mohon Menunggu..`")
    os.system("cp *mp4 thumb.mp4")
    os.system("ffmpeg -i thumb.mp4 -vframes 1 -an -s 480x360 -ss 5 thumb.jpg")
    thumb_image = "thumb.jpg"
    c_time = time.time()
    await event.client.send_file(
        event.chat_id,
        loa,
        force_document=False,
        thumb=thumb_image,
        allow_cache=False,
        caption=query,
        supports_streaming=True,
        reply_to=reply_to_id,
        attributes=[
            DocumentAttributeVideo(
                duration=duration,
                w=width,
                h=height,
                round_message=False,
                supports_streaming=True,
            )
        ],
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]", loa)
        ),
    )
    await event.delete()
    os.remove(thumb_image)
    os.system("rm -rf *.mkv")
    os.system("rm -rf *.mp4")
    os.system("rm -rf *.webm")


@register(outgoing=True, pattern=r"^\.smd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Mendapatkan Musik Anda```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit("`Mendownload Musik Anda, Mohon Menunggu Beberapa Saat...`")
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=752979930)
            )
            msg = await bot.send_message(chat, link)
            respond = await response
            res = conv.wait_event(
                events.NewMessage(incoming=True, from_users=752979930)
            )
            r = await res
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply(
                "```Mohon Unblock @SpotifyMusicDownloaderBot Dan Coba Lagi```"
            )
            return
        await bot.forward_messages(event.chat_id, respond.message)
    await event.client.delete_messages(conv.chat_id, [msg.id, r.id, respond.id])
    await event.delete()


@register(pattern=r"^/deez (.+?|) (FLAC|MP3\_320|MP3\_256|MP3\_128)")
async def _(event):
    if event.fwd_from:
        return

    strings = {
        "name": "DeezLoad",
        "arl_token_cfg_doc": "Token ARL untuk Deezer",
        "invalid_arl_token": "Harap setel variabel yang diperlukan untuk modul ini",
        "wrong_cmd_syntax": "Bruh, sekarang saya pikir seberapa jauh kita harus melangkah. tolong hentikan Sesi saya ð¥º",
        "server_error": "Mengalami kesalahan teknis.",
        "processing": "`Sedang Mendownload....`",
        "uploading": "`Mengunggah.....`",
    }

    ARL_TOKEN = DEEZER_ARL_TOKEN

    if ARL_TOKEN is None:
        await event.edit(strings["invalid_arl_token"])
        return

    try:
        loader = deezloader.Login(ARL_TOKEN)
    except Exception as er:
        await event.edit(str(er))
        return

    temp_dl_path = os.path.join(TEMP_DOWNLOAD_DIRECTORY, str(time.time()))
    if not os.path.exists(temp_dl_path):
        os.makedirs(temp_dl_path)

    required_link = event.pattern_match.group(1)
    required_qty = event.pattern_match.group(2)

    await event.edit(strings["Memproses"])

    if "spotify" in required_link:
        if "track" in required_link:
            required_track = loader.download_trackspo(
                required_link,
                output=temp_dl_path,
                quality=required_qty,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
            )
            await event.edit(strings["Uploading"])
            await upload_track(required_track, event)
            shutil.rmtree(temp_dl_path)

        elif "album" in required_link:
            reqd_albums = loader.download_albumspo(
                required_link,
                output=temp_dl_path,
                quality=required_qty,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=False,
            )
            for required_track in reqd_albums:
                await event.edit(strings["Uploading"])
                await upload_track(required_track, event)
            shutil.rmtree(temp_dl_path)

    elif "deezer" in required_link:
        if "track" in required_link:
            required_track = loader.download_trackdee(
                required_link,
                output=temp_dl_path,
                quality=required_qty,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
            )
            await upload_track(required_track, event)
            await event.edit(strings["Uploading"])
            shutil.rmtree(temp_dl_path)
            await event.delete()

        elif "album" in required_link:
            reqd_albums = loader.download_albumdee(
                required_link,
                output=temp_dl_path,
                quality=required_qty,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True,
                zips=False,
            )
            for required_track in reqd_albums:
                await event.edit(strings["Uploading"])
                await upload_track(required_track, event)
            shutil.rmtree(temp_dl_path)
            await event.delete()

    else:
        await event.edit(strings["wrong_cmd_syntax"])


async def upload_track(track_location, message):
    metadata = extractMetadata(createParser(track_location))
    duration = 0
    title = ""
    performer = ""
    if metadata.has("durasi"):
        duration = metadata.get("durasi").seconds
    if metadata.has("judul"):
        title = metadata.get("judul")
    if metadata.has("judul"):
        performer = metadata.get("artis")
    document_attributes = [
        DocumentAttributeAudio(
            duration=duration,
            voice=False,
            title=title,
            performer=performer,
            waveform=None,
        )
    ]
    supports_streaming = True
    force_document = False
    caption_rts = os.path.basename(track_location)
    c_time = time.time()
    await message.client.send_file(
        message.chat_id,
        track_location,
        caption=caption_rts,
        force_document=force_document,
        supports_streaming=supports_streaming,
        allow_cache=False,
        reply_to=message.message.id,
        attributes=document_attributes,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, message, c_time, "[UPLOAD]")
        ),
    )
    os.remove(track_location)


CMD_HELP.update(
    {
        "getmusic": "**Plugin : **`getmusic`\
        \n\n  •  **Syntax :** `.net <Artis - Judul Lagu>`\
        \n  •  **Function : **Download Musik Dari @WooHaiBot\
        \n\n  •  **Syntax :** `.vsong <Artis - Judul Lagu>`\
        \n  •  **Function : **Mencari dan mengunggah video clip.\
        \n\n  •  **Syntax :** `.smd <Artis - Judul Lagu>`\
        \n  •  **Function : **Mendownload musik dari Spotify\
        \n\n  •  **Syntax :** `.deez (spotify/link deezer)`\
        \n  •  **Function : **Download musik dari deezer.\
        \n  •  **Format :** `FLAC`, `MP3_320`, `MP3_256`, `MP3_128`.\
    "
    }
)
