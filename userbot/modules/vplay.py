import asyncio

from pytgcalls import StreamType
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from pytgcalls.types.stream import StreamAudioEnded
from youtubesearchpython import VideosSearch

from userbot import bot, call_py
from userbot.events import man_cmd
from userbot.utils.queues.vqueues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
    pop_an_item,
)


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            songname = r["title"][:35] + "..." if len(r["title"]) > 34 else r["title"]
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


async def skip_item(chat_id, h):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    try:
        x = int(h)
        songname = chat_queue[x][0]
        chat_queue.pop(x)
        return songname
    except Exception as e:
        print(e)
        return 0


async def skip_current_song(chat_id):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    if len(chat_queue) == 1:
        await call_py.leave_group_call(chat_id)
        clear_queue(chat_id)
        return 1
    else:
        songname = chat_queue[1][0]
        url = chat_queue[1][1]
        link = chat_queue[1][2]
        type = chat_queue[1][3]
        Q = chat_queue[1][4]
        if type == "Audio":
            await call_py.change_stream(
                chat_id,
                AudioPiped(
                    url,
                ),
            )
        elif type == "Video":
            if Q == 720:
                hm = HighQualityVideo()
            elif Q == 480:
                hm = MediumQualityVideo()
            elif Q == 360:
                hm = LowQualityVideo()
            await call_py.change_stream(
                chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
            )
        pop_an_item(chat_id)
        return [songname, link, type]


@bot.on(man_cmd(outgoing=True, pattern=r"vplay(?:\s|$)([\s\S]*)"))
async def video_c(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat_id = event.chat_id
    if (
        replied
        and not replied.video
        and not replied.document
        and not title
        or not replied
        and not title
    ):
        return await event.edit("**Silahkan Masukan Judul Video**")
    elif replied and not replied.video and not replied.document:
        huehue = await event.reply("`Searching...`")
        query = event.text.split(maxsplit=1)[1]
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
            elif chat_id in QUEUE:
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

    elif replied:
        huehue = await replied.edit("`Downloading`")
        dl = await replied.download_media()
        if len(event.text.split()) < 2:
            Q = 720
        else:
            pq = event.text.split(maxsplit=1)[1]
            Q = int(pq)
        if replied.video or replied.document:
            songname = "Telegram Video Player..."
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, "Video", Q)
            await huehue.edit(f"**Ditambahkan Ke antrian Ke** `#{pos}`")
        else:
            if Q == 360:
                hmmm = LowQualityVideo()
            elif Q == 480:
                hmmm = MediumQualityVideo()
            elif Q == 720:
                hmmm = HighQualityVideo()
            await call_py.join_group_call(
                chat_id,
                AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                stream_type=StreamType().pulse_stream,
            )
            add_to_queue(chat_id, songname, dl, "Video", Q)
            await huehue.edit(
                f"**Sedang Memutar Video ▶**\n**💬 Chat ID** : `{chat_id}`",
                link_preview=False,
            )
    else:
        huehue = await event.edit("`Searching...`")
        query = event.text.split(maxsplit=1)[1]
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
            elif chat_id in QUEUE:
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
async def vend(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await event.edit("**Menghentikan Streaming**")
        except Exception as e:
            await event.edit(f"**ERROR**\n`{e}`")
    else:
        await event.edit("**Tidak Sedang Memutar Streaming**")


@bot.on(man_cmd(outgoing=True, pattern="vskip$"))
async def skip(event):
    chat_id = event.chat_id
    if len(event.text.split()) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await event.edit("**Tidak Sedang Memutar Streaming**")
        elif op == 1:
            await event.edit("`Antrian Kosong, Meninggalkan Obrolan Suara...`")
        else:
            await event.edit(
                f"**⏭ Melewati Video** \n**🎧 Sekarang Memutar** - [{op[0]}]({op[1]}) | `{op[2]}`",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        OP = "**Menghapus Video Berikut Dari Antrian:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await skip_item(chat_id, x)
                    if hm != 0:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await event.edit(OP)


@bot.on(man_cmd(outgoing=True, pattern="vpause$"))
async def vpause(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await event.edit("**Paused Streaming**")
        except Exception as e:
            await event.edit(f"**ERROR**\n`{e}`")
    else:
        await event.edit("**Tidak Sedang Memutar Streaming**")


@bot.on(man_cmd(outgoing=True, pattern="vresume$"))
async def vresume(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await event.edit("**Resumed Streaming ▶**")
        except Exception as e:
            await event.edit(f"**ERROR**\n`{e}`")
    else:
        await event.edit("**Tidak Sedang Memutar Streaming**")


@bot.on(man_cmd(outgoing=True, pattern="vplaylist$"))
async def playlist(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await event.edit(
                f"**🎧 SEDANG MEMUTAR:**\n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview=False,
            )
        else:
            QUE = f"**🎧 SEDANG MEMUTAR:**\n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ PLAYLIST:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
            await event.edit(QUE, link_preview=False)
    else:
        await event.edit("**Tidak Sedang Memutar Streaming**")


@call_py.on_stream_end()
async def on_end_handler(_, u: Update):
    if isinstance(u, StreamAudioEnded):
        chat_id = u.chat_id
        print(chat_id)
        op = await skip_current_song(chat_id)
        if op == 1:
            await bot.send_message(
                chat_id, "`Antrian Kosong, Meninggalkan Obrolan Suara...`"
            )
        else:
            await bot.send_message(
                chat_id,
                f"**🎧 Sedang Memutar** \n[{op[0]}]({op[1]}) | `{op[2]}`",
                link_preview=False,
            )
