# Copyright (C) 2020 Aidil Aryanto.
# All rights reserved.

import asyncio
import glob
import os
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pylast import User
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeVideo

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, LASTFM_USERNAME, lastfm
from userbot.utils import bash, chrome, edit_or_reply, man_cmd, progress
from userbot.utils.FastTelethon import upload_file


async def getmusic(cat):
    video_link = ""
    search = cat
    driver = await chrome()
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    command = f"yt-dlp -x --add-metadata --embed-thumbnail --no-progress --audio-format mp3 {video_link}"
    await bash(command)
    return video_link


async def getmusicvideo(cat):
    video_link = ""
    search = cat
    driver = await chrome()
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    command = (
        'yt-dlp -f "[filesize<50M]" --no-progress --merge-output-format mp4 '
        + video_link
    )
    await bash(command)


@man_cmd(pattern="song (.*)")
async def _(event):
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        xx = await edit_or_reply(event, "`Processing..`")
    elif reply.message:
        query = reply.message
        await xx.edit("`Tunggu..! Saya menemukan lagu Anda..`")
    else:
        await xx.edit("`Apa yang seharusnya saya temukan?`")
        return

    await getmusic(str(query))
    loa = glob.glob("*.mp3")[0]
    await xx.edit("`Yeah.. Mengupload lagu Anda..`")
    c_time = time.time()
    with open(loa, "rb") as f:
        result = await upload_file(
            client=event.client,
            file=f,
            name=loa,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "[UPLOAD]", loa)
            ),
        )
    await event.client.send_file(
        event.chat_id,
        result,
        allow_cache=False,
    )
    await event.delete()
    await bash("rm -rf *.mp3")


@man_cmd(pattern="vsong(?: |$)(.*)")
async def _(event):
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        xx = await edit_or_reply(event, "`Processing..`")
    elif reply:
        query = str(reply.message)
        await xx.edit("**Tunggu..! Saya menemukan lagu video Anda..**")
    else:
        await xx.edit("**Apa yang seharusnya saya temukan?**")
        return
    await getmusicvideo(query)
    l = glob.glob(("*.mp4")) + glob.glob(("*.mkv")) + glob.glob(("*.webm"))
    if l:
        await xx.edit("**Ya..! aku menemukan sesuatu..**")
    else:
        await xx.edit(
            f"**Maaf..! saya tidak dapat menemukan apa pun dengan** `{query}`"
        )
        return
    try:
        loa = l[0]
        metadata = extractMetadata(createParser(loa))
        duration = metadata.get("duration").seconds if metadata.has("duration") else 0
        width = metadata.get("width") if metadata.has("width") else 0
        height = metadata.get("height") if metadata.has("height") else 0
        await bash("cp *mp4 thumb.mp4")
        await bash("ffmpeg -i thumb.mp4 -vframes 1 -an -s 480x360 -ss 5 thumb.jpg")
        thumb_image = "thumb.jpg"
        c_time = time.time()
        with open(loa, "rb") as f:
            result = await upload_file(
                client=event.client,
                file=f,
                name=loa,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "[UPLOAD]", loa)
                ),
            )
        await event.client.send_file(
            event.chat_id,
            result,
            force_document=False,
            thumb=thumb_image,
            allow_cache=False,
            caption=query,
            supports_streaming=True,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    round_message=False,
                    supports_streaming=True,
                )
            ],
        )
        await xx.edit(f"**{query} Berhasil Diupload..!**")
        os.remove(thumb_image)
        await bash("rm *.mkv *.mp4 *.webm")
    except BaseException:
        os.remove(thumb_image)
        await bash("rm *.mkv *.mp4 *.webm")
        return


@man_cmd(pattern="smd (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit(
                "`Error: Tidak ada data scrobbling yang ditemukan.`"
            )
        artist = playing.get_artist()
        song = playing.get_title()
    else:
        artist = event.pattern_match.group(2)
        song = event.pattern_match.group(3)
    track = str(artist) + " - " + str(song)
    chat = "@SpotifyMusicDownloaderBot"
    try:
        await event.edit("`Getting Your Music...`")
        async with event.client.conversation(chat) as conv:
            await asyncio.sleep(2)
            await event.edit("`Downloading...`")
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=752979930)
                )
                msg = await event.client.send_message(chat, track)
                respond = await response
                res = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=752979930)
                )
                r = await res
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply(
                    "`Unblock `@SpotifyMusicDownloaderBot` dan coba lagi`"
                )
                return
            await event.client.forward_messages(event.chat_id, respond.message)
        await event.client.delete_messages(conv.chat_id, [msg.id, r.id, respond.id])
        await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@SpotifyMusicDownloaderBot` tidak merespons atau Lagu tidak ditemukan!.`"
        )


@man_cmd(pattern="net (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit(
                "`Error: Tidak ada scrobble saat ini yang ditemukan.`"
            )
        artist = playing.get_artist()
        song = playing.get_title()
    else:
        artist = event.pattern_match.group(2)
        song = event.pattern_match.group(3)
    track = str(artist) + " - " + str(song)
    chat = "@WooMaiBot"
    link = f"/netease {track}"
    await event.edit("`Searching...`")
    try:
        async with event.client.conversation(chat) as conv:
            await asyncio.sleep(2)
            await event.edit("`Processing...`")
            try:
                msg = await conv.send_message(link)
                response = await conv.get_response()
                respond = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("`Please unblock @WooMaiBot and try again`")
                return
            await event.edit("`Sending Your Music...`")
            await asyncio.sleep(3)
            await event.client.send_file(event.chat_id, respond)
        await event.client.delete_messages(
            conv.chat_id, [msg.id, response.id, respond.id]
        )
        await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@WooMaiBot` tidak merespons atau Lagu tidak ditemukan!.`"
        )


@man_cmd(pattern="mhb(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("`Masukkan link yang valid untuk mendownload`")
    else:
        await event.edit("`Processing...`")
    chat = "@MusicsHunterBot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                msg = await conv.send_message(d_link)
                details = await conv.get_response()
                song = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("`Unblock `@MusicsHunterBot` and retry`")
                return
            await event.client.send_file(event.chat_id, song, caption=details.text)
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, response.id, msg.id, details.id, song.id]
            )
            await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@MusicsHunterBot` tidak merespons atau Lagu tidak ditemukan!.`"
        )


CMD_HELP.update(
    {
        "getmusic": f"**Plugin : **`getmusic`\
        \n\n  •  **Syntax :** `{cmd}smd` <nama lagu>\
        \n  •  **Function : **Mendowload lagu dari bot @SpotifyMusicDownloaderBot\
        \n\n  •  **Syntax :** `{cmd}smd now`\
        \n  •  **Function : **Unduh penggunaan scrobble LastFM saat ini dari bot @SpotifyMusicDownloaderBot\
        \n\n  •  **Syntax :** `{cmd}net` <nama lagu>\
        \n  •  **Function : **Mendowload lagu dari bot @WooMaiBot\
        \n\n  •  **Syntax :** `{cmd}net now`\
        \n  •  **Function : **Unduh penggunaan scrobble LastFM saat ini dari bot @WooMaiBot\
        \n\n  •  **Syntax :** `{cmd}mhb` <Link Spotify/Deezer>\
        \n  •  **Function : **Mendowload lagu dari Spotify atau Deezer dari bot @MusicsHunterBot\
    "
    }
)
