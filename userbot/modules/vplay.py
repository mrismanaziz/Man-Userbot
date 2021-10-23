import asyncio

from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from userbot import bot, call_py
from userbot.events import man_cmd
from userbot.utils.queues.vqueues import QUEUE, add_to_queue, clear_queue


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "youtube-dl",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@bot.on(man_cmd(outgoing=True, pattern=r"vplay(?:\s|$)([\s\S]*)"))
async def video_c(m):
    title = m.pattern_match.group(1)
    replied = await m.get_reply_message()
    chat_id = m.chat_id
    if replied:
        if replied.video or replied.document:
            huehue = await replied.edit("`Downloading`")
            dl = await replied.download()
            link = replied.link
            if len(m.title) < 2:
                Q = 720
            else:
                pq = m.text.split(maxsplit=1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "**Hanya Mengijinkan Resolusi** `720p`, `480p`, `360p`\n**Sekarang Streaming di 720p**"
                    )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.edit(f"**Ditambahkan Ke antrian Ke** `#{pos}`")
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.edit(
                    f"**Memulai Memutar Video ▶** \n**🎧 Judul** : [{songname}]({link}) \n**💬 Chat ID** : `{chat_id}`",
                    link_preview=False,
                )
        else:
            if not title:
                return await m.edit("**Silahkan Masukan Judul Video**")
            else:
                huehue = await m.reply("`Searching...`")
                query = m.text.split(maxsplit=1)[1]
                search = ytsearch(query)
                Q = 720
                hmmm = HighQualityVideo()
                if search == 0:
                    await huehue.edit(
                        "**Tidak Menemukan Video untuk Keyword yang Diberikan**"
                    )
                else:
                    songname = search[0]
                    url = search[1]
                    hm, ytlink = await ytdl(url)
                    if hm == 0:
                        await huehue.edit(f"**ERROR YTDL**\n\n`{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await huehue.edit(f"**Ditambahkan Ke antrian Ke** `#{pos}`")
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await huehue.edit(
                                    f"**Memulai Memutar Video ▶** \n**🎧 Judul** : [{songname}]({url}) \n**💬 Chat ID** : `{chat_id}`",
                                    link_preview=False,
                                )
                            except Exception as ep:
                                await huehue.edit(f"`{ep}`")

    else:
        if not title:
            return await m.edit("**Silahkan Masukan Judul Video**")
        else:
            huehue = await m.edit("`Searching...`")
            query = m.text.split(maxsplit=1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(
                    "**Tidak Menemukan Video untuk Keyword yang Diberikan**"
                )
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**ERROR YTDL**\n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.edit(f"**Ditambahkan Ke antrian Ke** `#{pos}`")
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.edit(
                                f"**Memulai Memutar Video ▶** \n**🎧 Judul** : [{songname}]({url}) \n**💬 Chat ID** : `{chat_id}`",
                                link_preview=False,
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@bot.on(man_cmd(outgoing=True, pattern="vend$"))
async def vend(m):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.edit("**Menghentikan Streaming**")
        except Exception as e:
            await m.edit(f"**ERROR**\n`{e}`")
    else:
        await m.edit("**Tidak Sedang Memutar Streaming**")


@bot.on(man_cmd(outgoing=True, pattern="vpause$"))
async def vpause(m):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.edit("**Paused Streaming**")
        except Exception as e:
            await m.edit(f"**ERROR**\n`{e}`")
    else:
        await m.edit("**Tidak Sedang Memutar Streaming**")


@bot.on(man_cmd(outgoing=True, pattern="vresume$"))
async def vresume(m):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.edit("**Resumed Streaming ▶**")
        except Exception as e:
            await m.edit(f"**ERROR**\n`{e}`")
    else:
        await m.edit("**Tidak Sedang Memutar Streaming**")
