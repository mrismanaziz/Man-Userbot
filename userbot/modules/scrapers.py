# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# thanks to the owner of X-tra-Telegram for tts fix
#
# Recode by @mrismanaziz
# FROM Man-Userbot
# t.me/SharingUserbot
#
""" Userbot module containing various scrapers. """

import asyncio
import io
import json
import os
import re
import shutil
import time
from asyncio import get_event_loop, sleep
from glob import glob
from re import findall, match

import asyncurban
import barcode
import emoji
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from requests import get
from search_engine_parser import BingSearch, GoogleSearch, YahooSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError
from telethon.tl.types import (
    DocumentAttributeAudio,
    DocumentAttributeVideo,
    MessageMediaPhoto,
)
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from userbot import CMD_HANDLER as cmd
from userbot import (
    CMD_HELP,
    LOGS,
    OCR_SPACE_API_KEY,
    REM_BG_API_KEY,
    TEMP_DOWNLOAD_DIRECTORY,
    bot,
)
from userbot.modules.upload_download import get_video_thumb
from userbot.utils import (
    chrome,
    edit_delete,
    edit_or_reply,
    googleimagesdownload,
    man_cmd,
    options,
    progress,
)
from userbot.utils.FastTelethon import upload_file

TTS_LANG = "id"
TRT_LANG = "id"


async def ocr_space_file(
    filename, overlay=False, api_key=OCR_SPACE_API_KEY, language="eng"
):

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.json()


@man_cmd(pattern="img (.*)")
async def img_sampler(event):
    xx = await edit_or_reply(event, "`Sedang Mencari Gambar Yang Anda Cari...`")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 15
    response = googleimagesdownload()
    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await xx.delete()


@man_cmd(pattern="currency ([\d\.]+) ([a-zA-Z]+) ([a-zA-Z]+)")
async def moni(event):
    c_from_val = float(event.pattern_match.group(1))
    c_from = (event.pattern_match.group(2)).upper()
    c_to = (event.pattern_match.group(3)).upper()
    xx = await edit_or_reply(event, "`Processing...`")
    try:
        response = get(
            "https://api.frankfurter.app/latest",
            params={"from": c_from, "to": c_to},
        ).json()
    except Exception:
        return await edit_delete(xx, "**Error: API is down.**")
    if "error" in response:
        await edit_delete(
            xx,
            "**sepertinya ini  mata uang asing, yang tidak dapat saya konversi sekarang.**",
        )
        return
    c_to_val = round(c_from_val * response["rates"][c_to], 2)
    await xx.edit(f"**{c_from_val} {c_from} = {c_to_val} {c_to}**")


@man_cmd(pattern="google ([\s\S]*)")
async def gsearch(q_event):
    man = await edit_or_reply(q_event, "`Processing...`")
    match = q_event.pattern_match.group(1)
    page = re.findall(r"-p\d+", match)
    lim = re.findall(r"-l\d+", match)
    try:
        page = page[0]
        page = page.replace("-p", "")
        match = match.replace("-p" + page, "")
    except IndexError:
        page = 1
    try:
        lim = lim[0]
        lim = lim.replace("-l", "")
        match = match.replace("-l" + lim, "")
        lim = int(lim)
        if lim <= 0:
            lim = int(5)
    except IndexError:
        lim = 5
    smatch = match.replace(" ", "+")
    search_args = (str(smatch), int(page))
    gsearch = GoogleSearch()
    bsearch = BingSearch()
    ysearch = YahooSearch()
    try:
        gresults = await gsearch.async_search(*search_args)
    except NoResultsOrTrafficError:
        try:
            gresults = await bsearch.async_search(*search_args)
        except NoResultsOrTrafficError:
            try:
                gresults = await ysearch.async_search(*search_args)
            except Exception as e:
                return await edit_delete(man, f"**ERROR:**\n`{e}`", time=10)
    msg = ""
    for i in range(lim):
        if i > len(gresults["links"]):
            break
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉 [{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await edit_or_reply(
        man,
        "**Keyword Google Search:**\n`" + match + "`\n\n**Results:**\n" + msg,
        link_preview=False,
        aslink=True,
        linktext=f"**Hasil Pencarian untuk Keyword** `{match}` **adalah** :",
    )


@man_cmd(pattern="wiki (.*)")
async def wiki(wiki_q):
    match = wiki_q.pattern_match.group(1)
    xx = await edit_or_reply(wiki_q, "`Processing...`")
    try:
        summary(match)
    except DisambiguationError as error:
        await edit_delete(xx, f"Ditemukan halaman yang tidak ambigu.\n\n{error}")
        return
    except PageError as pageerror:
        await edit_delete(xx, f"Halaman tidak ditemukan.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        with open("output.txt", "w+") as file:
            file.write(result)
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            thumb="userbot/resources/logo.jpg",
            reply_to=wiki_q.id,
            caption="**Output terlalu besar, dikirim sebagai file**",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return
    await xx.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)


@man_cmd(pattern="ud (.*)")
async def _(event):
    if event.fwd_from:
        return
    xx = await edit_or_reply(event, "Processing...")
    word = event.pattern_match.group(1)
    urban = asyncurban.UrbanDictionary()
    try:
        mean = await urban.get_word(word)
        await xx.edit(
            "Text: **{}**\n\nBerarti: **{}**\n\nContoh: __{}__".format(
                mean.word, mean.definition, mean.example
            )
        )
    except asyncurban.WordNotFoundError:
        await xx.edit("Tidak ada hasil untuk **" + word + "**")


@man_cmd(pattern="tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    xx = await edit_or_reply(query, "`Processing...`")
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await edit_delete(
            xx, "**Berikan teks atau balas pesan untuk Text-to-Speech!**"
        )
    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        return await edit_delete(
            xx,
            "**Teksnya kosong.**\n"
            "Tidak ada yang tersisa untuk dibicarakan setelah pra-pemrosesan, pembuatan token, dan pembersihan.",
        )
    except ValueError:
        return await edit_delete(xx, "**Bahasa tidak didukung.**")
    except RuntimeError:
        return await edit_delete(xx, "**Error saat memuat kamus bahasa.**")
    tts = gTTS(message, lang=TTS_LANG)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang=TTS_LANG)
        tts.save("k.mp3")
    with open("k.mp3", "r"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
        os.remove("k.mp3")
        await xx.delete()


@man_cmd(pattern="tr(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    input_str = event.pattern_match.group(1)
    xx = await edit_or_reply(event, "`Processing...`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "id"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        return await edit_delete(xx, "**.tr <kode bahasa>** sambil reply ke pesan")
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = """**DITERJEMAHKAN** dari `{}` ke `{}`
{}""".format(
            translated.src, lan, after_tr_text
        )
        await xx.edit(output_str)
    except Exception as exc:
        await edit_delete(xx, str(exc))


@man_cmd(pattern=r"lang (tr|tts) (.*)")
async def lang(value):
    util = value.pattern_match.group(1).lower()
    xx = await edit_or_reply(value, "`Processing...`")
    if util == "tr":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await edit_delete(
                xx,
                f"**Kode Bahasa tidak valid !!**\n**Kode bahasa yang tersedia**:\n\n`{LANGUAGES}`",
            )
            return
    elif util == "tts":
        scraper = "Text to Speech"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await edit_delete(
                xx,
                f"**Kode Bahasa tidak valid!!**\n**Kode bahasa yang tersedia**:\n\n`{tts_langs()}`",
            )
            return
    await xx.edit(f"**Bahasa untuk** `{scraper}` **diganti menjadi** `{LANG.title()}`")


@man_cmd(pattern="yt (\d*) *(.*)")
async def yt_search(video_q):
    if video_q.pattern_match.group(1) != "":
        counter = int(video_q.pattern_match.group(1))
        if counter > 10:
            counter = int(10)
        if counter <= 0:
            counter = int(1)
    else:
        counter = int(5)
    query = video_q.pattern_match.group(2)
    if not query:
        await edit_delete(video_q, "`Masukkan keyword untuk dicari`")
    xx = await edit_or_reply(video_q, "`Processing...`")
    try:
        results = json.loads(YoutubeSearch(query, max_results=counter).to_json())
    except KeyError:
        return await edit_delete(
            xx, "`Pencarian Youtube menjadi lambat.\nTidak dapat mencari keyword ini!`"
        )
    output = f"**Pencarian Keyword:**\n`{query}`\n\n**Hasil:**\n\n"
    for i in results["videos"]:
        try:
            title = i["title"]
            link = "https://youtube.com" + i["url_suffix"]
            channel = i["channel"]
            duration = i["duration"]
            views = i["views"]
            output += f"🏷 **Judul:** [{title}]({link})\n⏱ **Durasi:** {duration}\n👀 {views}\n🖥 **Channel:** `{channel}`\n━━\n"
        except IndexError:
            break

    await xx.edit(output, link_preview=False)


@man_cmd(pattern="yt(audio|video( \d{0,4})?) (.*)")
async def download_video(v_url):
    dl_type = v_url.pattern_match.group(1).lower()
    reso = v_url.pattern_match.group(2)
    reso = reso.strip() if reso else None
    url = v_url.pattern_match.group(3)
    xx = await edit_or_reply(v_url, "`Preparing to download...`")
    s_time = time.time()
    video = False
    audio = False

    if "audio" in dl_type:
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "noprogress": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(
                TEMP_DOWNLOAD_DIRECTORY, str(s_time), "%(title)s.%(ext)s"
            ),
            "quiet": True,
            "logtostderr": False,
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "proxy": "",
            "extractor-args": "youtube:player_client=_music",
        }
        audio = True

    elif "video" in dl_type:
        quality = (
            f"bestvideo[height<={reso}]+bestaudio/best[height<={reso}]"
            if reso
            else "bestvideo+bestaudio/best"
        )
        opts = {
            "format": quality,
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "noprogress": True,
            "outtmpl": os.path.join(
                TEMP_DOWNLOAD_DIRECTORY, str(s_time), "%(title)s.%(ext)s"
            ),
            "logtostderr": False,
            "quiet": True,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
            "proxy": "",
            "extractor-args": "youtube:player_client=all",
        }
        video = True

    try:
        await xx.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        return await edit_delete(xx, f"`{DE}`")
    except ContentTooShortError:
        return await edit_delete(xx, "`The download content was too short.`")
    except GeoRestrictedError:
        return await edit_delete(
            xx,
            "`Video is not available from your geographic location "
            "due to geographic restrictions imposed by a website.`",
        )
    except MaxDownloadsReached:
        return await edit_delete(xx, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await edit_delete(xx, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await edit_delete(
            xx, "`Media is not available in the requested format.`"
        )
    except XAttrMetadataError as XAME:
        return await edit_delete(xx, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await edit_delete(xx, "`There was an error during info extraction.`")
    except Exception as e:
        return await edit_delete(xx, f"{str(type(e)): {e}}")
    c_time = time.time()
    if audio:
        await xx.edit(
            f"**Sedang Mengupload Lagu:**\n`{rip_data.get('title')}`"
            f"\nby **{rip_data.get('uploader')}**"
        )
        f_name = glob(os.path.join(TEMP_DOWNLOAD_DIRECTORY, str(s_time), "*.mp3"))[0]
        with open(f_name, "rb") as f:
            result = await upload_file(
                client=v_url.client,
                file=f,
                name=f_name,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(
                        d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp3"
                    )
                ),
            )

        thumb_image = [
            x
            for x in glob(os.path.join(TEMP_DOWNLOAD_DIRECTORY, str(s_time), "*"))
            if not x.endswith(".mp3")
        ][0]
        metadata = extractMetadata(createParser(f_name))
        duration = 0
        if metadata and metadata.has("duration"):
            duration = metadata.get("duration").seconds
        await v_url.client.send_file(
            v_url.chat_id,
            result,
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    title=rip_data.get("title"),
                    performer=rip_data.get("uploader"),
                )
            ],
            thumb=thumb_image,
        )
        await xx.delete()
    elif video:
        await xx.edit(
            f"**Sedang Mengupload Video:**\n`{rip_data.get('title')}`"
            f"\nby **{rip_data.get('uploader')}**"
        )
        f_path = glob(os.path.join(TEMP_DOWNLOAD_DIRECTORY, str(s_time), "*"))[0]
        # Noob way to convert from .mkv to .mp4
        if f_path.endswith(".mkv") or f_path.endswith(".webm"):
            base = os.path.splitext(f_path)[0]
            os.rename(f_path, base + ".mp4")
            f_path = glob(os.path.join(TEMP_DOWNLOAD_DIRECTORY, str(s_time), "*"))[0]
        f_name = os.path.basename(f_path)
        with open(f_path, "rb") as f:
            result = await upload_file(
                client=v_url.client,
                file=f,
                name=f_name,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, v_url, c_time, "Uploading..", f_name)
                ),
            )
        thumb_image = await get_video_thumb(f_path, "thumb.png")
        metadata = extractMetadata(createParser(f_path))
        duration = 0
        width = 0
        height = 0
        if metadata:
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
        await v_url.client.send_file(
            v_url.chat_id,
            result,
            thumb=thumb_image,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    supports_streaming=True,
                )
            ],
            caption=f"[{rip_data.get('title')}]({url})",
        )
        os.remove(thumb_image)
        await xx.delete()


@man_cmd(pattern="rbg(?: |$)(.*)")
async def kbg(remob):
    if REM_BG_API_KEY is None:
        await edit_delete(
            remob,
            "`Error: Remove.BG API key missing! Add it to environment vars or config.env.`",
        )
        return
    input_str = remob.pattern_match.group(1)
    message_id = remob.message.id
    if remob.reply_to_msg_id:
        message_id = remob.reply_to_msg_id
        reply_message = await remob.get_reply_message()
        xx = await edit_or_reply(remob, "`Processing...`")
        try:
            if isinstance(
                reply_message.media, MessageMediaPhoto
            ) or "image" in reply_message.media.document.mime_type.split("/"):
                downloaded_file_name = await remob.client.download_media(
                    reply_message, TEMP_DOWNLOAD_DIRECTORY
                )
                await xx.edit("`Removing background from this image..`")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await edit_delete(xx, "`Bagaimana cara menghapus latar belakang ini ?`")
        except Exception as e:
            await edit_delete(xx, str(e))
            return
    elif input_str:
        await edit_delete(
            xx, f"`Removing background from online image hosted at`\n{input_str}"
        )
        output_file_name = await ReTrieveURL(input_str)
    else:
        await edit_delete(xx, "`Saya butuh sesuatu untuk menghapus latar belakang.`")
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            await remob.client.send_file(
                remob.chat_id,
                remove_bg_image,
                force_document=True,
                reply_to=message_id,
            )
            await xx.delete()
    else:
        await edit_delete(
            xx,
            "**Error (Invalid API key, I guess ?)**\n`{}`".format(
                output_file_name.content.decode("UTF-8")
            ),
        )


# this method will call the API, and return in the appropriate format
# with the name provided.
async def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


async def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )


@man_cmd(pattern=r"ocr (.*)")
async def ocr(event):
    if not OCR_SPACE_API_KEY:
        return await edit_delete(
            event,
            "`Error: OCR.Space API key is missing! Add it to environment variables or config.env.`",
        )
    xx = await edit_or_reply(event, "`Processing...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY
    )
    test_file = await ocr_space_file(filename=downloaded_file_name, language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await edit_delete(
            xx, "`Tidak bisa membacanya.`\n`Saya rasa saya perlu kacamata baru.`"
        )
    else:
        await xx.edit(f"**Inilah yang bisa saya baca:**\n\n{ParsedText}")
    os.remove(downloaded_file_name)


@man_cmd(pattern="decode$")
async def parseqr(qr_e):
    downloaded_file_name = await qr_e.client.download_media(
        await qr_e.get_reply_message()
    )
    # parse the Official ZXing webpage to decode the QRCode
    command_to_exec = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + downloaded_file_name + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    os.remove(downloaded_file_name)
    if not t_response:
        LOGS.info(e_response)
        LOGS.info(t_response)
        return await edit_delete(qr_e, "Gagal untuk decode.")
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await qr_e.edit(qr_contents)


@man_cmd(pattern="barcode(?: |$)([\s\S]*)")
async def bq(event):
    xx = await edit_or_reply(event, "`Processing...`")
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") + "\r\n" for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        return edit_delete(xx, "SYNTAX: `.barcode <long text to include>`")

    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await event.client.send_file(event.chat_id, filename, reply_to=reply_msg_id)
        os.remove(filename)
    except Exception as e:
        return await edit_delete(xx, f"{e}")
    await xx.delete()


@man_cmd(pattern=r"makeqr(?: |$)([\s\S]*)")
async def make_qr(makeqr):
    input_str = makeqr.pattern_match.group(1)
    xx = await edit_or_reply(makeqr, "`Processing...`")
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = "".join(media.decode("UTF-8") + "\r\n" for media in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(
        makeqr.chat_id, "img_file.webp", reply_to=reply_msg_id
    )
    os.remove("img_file.webp")
    await xx.delete()


@man_cmd(pattern="ss (.*)")
async def capture(url):
    xx = await edit_or_reply(url, "`Processing...`")
    chrome_options = await options()
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.arguments.remove("--window-size=1920x1080")
    driver = await chrome(chrome_options=chrome_options)
    input_str = url.pattern_match.group(1)
    link_match = match(r"\bhttps?://.*\.\S+", input_str)
    if link_match:
        link = link_match.group()
    else:
        return await edit_delete(xx, "`I need a valid link to take screenshots from.`")
    driver.get(link)
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
        "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
        "document.documentElement.offsetWidth);"
    )
    driver.set_window_size(width + 125, height + 125)
    wait_for = height / 1000
    await xx.edit(
        "`Generating screenshot of the page...`"
        f"\n`Height of page = {height}px`"
        f"\n`Width of page = {width}px`"
        f"\n`Waiting ({int(wait_for)}s) for the page to load.`"
    )
    await sleep(int(wait_for))
    im_png = driver.get_screenshot_as_png()
    # saves screenshot of entire page
    driver.quit()
    message_id = url.message.id
    if url.reply_to_msg_id:
        message_id = url.reply_to_msg_id
    with io.BytesIO(im_png) as out_file:
        out_file.name = "screencapture.png"
        await xx.edit("`Uploading screenshot as file..`")
        await url.client.send_file(
            url.chat_id,
            out_file,
            caption=input_str,
            force_document=True,
            reply_to=message_id,
        )
        await xx.delete()


CMD_HELP.update(
    {
        "tts": f"**Plugin : **`tts`\
        \n\n  •  **Syntax :** `{cmd}tts` <text/reply>\
        \n  •  **Function : **Menerjemahkan teks ke ucapan untuk bahasa yang disetel. \
        \n\n  •  **NOTE :** Gunakan {cmd}lang tts <kode bahasa> untuk menyetel bahasa untuk tr **(Bahasa Default adalah bahasa Indonesia)**\
    "
    }
)


CMD_HELP.update(
    {
        "translate": f"**Plugin : **`Terjemahan`\
        \n\n  •  **Syntax :** `{cmd}tr` <text/reply>\
        \n  •  **Function : **Menerjemahkan teks ke bahasa yang disetel.\
        \n\n  •  **NOTE :** Gunakan {cmd}lang tr <kode bahasa> untuk menyetel bahasa untuk tr **(Bahasa Default adalah bahasa Indonesia)**\
    "
    }
)


CMD_HELP.update(
    {
        "removebg": "**Plugin : **`removebg`\
        \n\n  •  **Syntax :** `{cmd}rbg` <Tautan ke Gambar> atau balas gambar apa pun (Peringatan: tidak berfungsi pada stiker.)\
        \n  •  **Function : **Menghapus latar belakang gambar, menggunakan API remove.bg\
    "
    }
)


CMD_HELP.update(
    {
        "ocr": f"**Plugin : **`ocr`\
        \n\n  •  **Syntax :** `{cmd}ocr` <kode bahasa>\
        \n  •  **Function : **Balas gambar atau stiker untuk mengekstrak teks media tersebut.\
    "
    }
)


CMD_HELP.update(
    {
        "google": f"**Plugin : **`google`\
        \n\n  •  **Syntax :** `{cmd}google` <flags> <query>\
        \n  •  **Function : **Untuk Melakukan pencarian di google (default 5 hasil pencarian)\
        \n  •  **Flags :** `-l` **= Untuk jumlah hasil pencarian.**\
        \n  •  **Example :** `{cmd}google -l4 mrismanaziz` atau `{cmd}google mrismanaziz`\
    "
    }
)


CMD_HELP.update(
    {
        "wiki": f"**Plugin : **`wiki`\
        \n\n  •  **Syntax :** `{cmd}wiki` <query>\
        \n  •  **Function : **Melakukan pencarian di Wikipedia.\
    "
    }
)


CMD_HELP.update(
    {
        "barcode": f"**Plugin : **`barcode`\
        \n\n  •  **Syntax :** `{cmd}barcode` <content>\
        \n  •  **Function :** Buat Kode Batang dari konten yang diberikan.\
        \n\n  •  **Example :** `{cmd}barcode www.google.com`\
        \n\n  •  **Syntax :** `{cmd}makeqr` <content>\
        \n  •  **Function :** Buat Kode QR dari konten yang diberikan.\
        \n\n  •  **Example :** `{cmd}makeqr www.google.com`\
        \n\n  •  **NOTE :** Gunakan {cmd}decode <reply to barcode / qrcode> untuk mendapatkan konten yang didekodekan.\
    "
    }
)


CMD_HELP.update(
    {
        "image_search": f"**Plugin : **`image_search`\
        \n\n  •  **Syntax :** `{cmd}img` <search_query>\
        \n  •  **Function : **Melakukan pencarian gambar di Google dan menampilkan 15 gambar.\
    "
    }
)


CMD_HELP.update(
    {
        "ytdl": f"**Plugin : **`ytdl`\
        \n\n  •  **Syntax :** `{cmd}yt` <jumlah> <query>\
        \n  •  **Function : **Melakukan Pencarian YouTube. Dapat menentukan jumlah hasil yang dibutuhkan (default adalah 5)\
        \n\n  •  **Syntax :** `{cmd}ytaudio` <url>\
        \n  •  **Function : **Untuk Mendownload lagu dari YouTube dengan link.\
        \n\n  •  **Syntax :** `{cmd}ytvideo` <quality> <url>\
        \n  •  **Quality : **`144`, `240`, `360`, `480`, `720`, `1080`, `2160`\
        \n  •  **Function : **Untuk Mendownload video dari YouTube dengan link.\
        \n\n  •  **Syntax :** `{cmd}song` <nama lagu>\
        \n  •  **Function : **Untuk mendownload lagu dari youtube dengan nama lagu.\
        \n\n  •  **Syntax :** `{cmd}vsong` <nama lagu>\
        \n  •  **Function : **Untuk mendownload Video dari youtube dengan nama video.\
    "
    }
)


CMD_HELP.update(
    {
        "screenshot": f"**Plugin : **`screenshot`\
        \n\n  •  **Syntax :** `{cmd}ss` <url>\
        \n  •  **Function : **Mengambil tangkapan layar dari situs web dan mengirimkan tangkapan layar.\
        \n  •  **Example  : {cmd}ss http://www.google.com\
    "
    }
)


CMD_HELP.update(
    {
        "currency": f"**Plugin : **`currency`\
        \n\n  •  **Syntax :** `{cmd}currency` <amount> <from> <to>\
        \n  •  **Function : **Mengonversi berbagai mata uang untuk Anda.\
    "
    }
)


CMD_HELP.update(
    {
        "ud": f"**Plugin : **`Urban Dictionary`\
        \n\n  •  **Syntax :** `{cmd}ud` <query>\
        \n  •  **Function : **Melakukan pencarian di Urban Dictionary.\
    "
    }
)
