# Man - UserBot
# Copyright (c) 2022 Man-Userbot
# Credits: @mrismanaziz || https://github.com/mrismanaziz
# Thanks To @tofik_dn || https://github.com/tofikdn
#
# This file is a part of < https://github.com/mrismanaziz/Man-Userbot/ >
# t.me/SharingUserbot & t.me/Lunatic0de

from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from telethon.tl import types
from telethon.utils import get_display_name

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, PLAY_PIC, QUEUE_PIC, call_py
from userbot.core.vcbot import (
    CHAT_TITLE,
    gen_thumb,
    skip_current_song,
    skip_item,
    ytdl,
    ytsearch,
)
from userbot.core.vcbot.queues import QUEUE, add_to_queue, clear_queue, get_queue
from userbot.utils import edit_delete, edit_or_reply, man_cmd


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


@man_cmd(pattern="play(?:\s|$)([\s\S]*)", group_only=True)
async def vc_play(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat = await event.get_chat()
    titlegc = chat.title
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.audio
        and not replied.voice
        and not title
        or not replied
        and not title
    ):
        return await edit_or_reply(event, "**Silahkan Masukan Judul Lagu**")
    elif replied and not replied.audio and not replied.voice or not replied:
        botman = await edit_or_reply(event, "`Searching...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await botman.edit(
                "**Tidak Dapat Menemukan Lagu** Coba cari dengan Judul yang Lebih Spesifik"
            )
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            videoid = search[4]
            titlegc = chat.title
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, videoid, ctitle)
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await botman.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                caption = f"💡 **Lagu Ditambahkan Ke antrian »** `#{pos}`\n\n**🏷 Judul:** [{songname}]({url})\n**⏱ Durasi:** `{duration}`\n🎧 **Atas permintaan:** {from_user}"
                await botman.delete()
                await event.client.send_file(
                    chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            ytlink,
                            HighQualityAudio(),
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                    caption = f"🏷 **Judul:** [{songname}]({url})\n**⏱ Durasi:** `{duration}`\n💡 **Status:** `Sedang Memutar`\n🎧 **Atas permintaan:** {from_user}"
                    await botman.delete()
                    await event.client.send_file(
                        chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                    )
                except AlreadyJoinedError:
                    await call_py.leave_group_call(chat_id)
                    clear_queue(chat_id)
                    await botman.edit(
                        "**ERROR:** `Karena akun sedang berada di obrolan suara`\n\n• Silahkan Coba Play lagi"
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await botman.edit(f"`{ep}`")

    else:
        botman = await edit_or_reply(event, "📥 **Sedang Mendownload**")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if replied.audio:
            songname = "Telegram Music Player"
        elif replied.voice:
            songname = "Voice Note"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            caption = f"💡 **Lagu Ditambahkan Ke antrian »** `#{pos}`\n\n**🏷 Judul:** [{songname}]({link})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
            await event.client.send_file(
                chat_id, QUEUE_PIC, caption=caption, reply_to=event.reply_to_msg_id
            )
            await botman.delete()
        else:
            try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                        HighQualityAudio(),
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                caption = f"🏷 **Judul:** [{songname}]({link})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Sedang Memutar Lagu`\n🎧 **Atas permintaan:** {from_user}"
                await event.client.send_file(
                    chat_id, PLAY_PIC, caption=caption, reply_to=event.reply_to_msg_id
                )
                await botman.delete()
            except AlreadyJoinedError:
                await call_py.leave_group_call(chat_id)
                clear_queue(chat_id)
                await botman.edit(
                    "**ERROR:** `Karena akun sedang berada di obrolan suara`\n\n• Silahkan Coba Play lagi"
                )
            except Exception as ep:
                clear_queue(chat_id)
                await botman.edit(f"`{ep}`")


@man_cmd(pattern="vplay(?:\s|$)([\s\S]*)", group_only=True)
async def vc_vplay(event):
    title = event.pattern_match.group(1)
    replied = await event.get_reply_message()
    chat = await event.get_chat()
    titlegc = chat.title
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.video
        and not replied.document
        and not title
        or not replied
        and not title
    ):
        return await edit_or_reply(event, "**Silahkan Masukan Judul Video**")
    if replied and not replied.video and not replied.document:
        xnxx = await edit_or_reply(event, "`Searching...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit(
                "**Tidak Dapat Menemukan Video** Coba cari dengan Judul yang Lebih Spesifik"
            )
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            videoid = search[4]
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, videoid, ctitle)
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                caption = f"💡 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n**🏷 Judul:** [{songname}]({url})\n**⏱ Durasi:** `{duration}`\n🎧 **Atas permintaan:** {from_user}"
                await xnxx.delete()
                await event.client.send_file(
                    chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            ytlink,
                            HighQualityAudio(),
                            hmmm,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    await xnxx.edit(
                        f"**🏷 Judul:** [{songname}]({url})\n**⏱ Durasi:** `{duration}`\n💡 **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}",
                        link_preview=False,
                    )
                except AlreadyJoinedError:
                    await call_py.leave_group_call(chat_id)
                    clear_queue(chat_id)
                    await xnxx.edit(
                        "**ERROR:** `Karena akun sedang berada di obrolan suara`\n\n• Silahkan Coba Play lagi"
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await xnxx.edit(f"`{ep}`")

    elif replied:
        xnxx = await edit_or_reply(event, "📥 **Sedang Mendownload**")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if len(event.text.split()) < 2:
            RESOLUSI = 720
        else:
            pq = event.text.split(maxsplit=1)[1]
            RESOLUSI = int(pq)
        if replied.video or replied.document:
            songname = "Telegram Video Player"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
            caption = f"💡 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n**🏷 Judul:** [{songname}]({link})\n**👥 Chat ID:** `{chat_id}`\n🎧 **Atas permintaan:** {from_user}"
            await event.client.send_file(
                chat_id, QUEUE_PIC, caption=caption, reply_to=event.reply_to_msg_id
            )
            await xnxx.delete()
        else:
            if RESOLUSI == 360:
                hmmm = LowQualityVideo()
            elif RESOLUSI == 480:
                hmmm = MediumQualityVideo()
            elif RESOLUSI == 720:
                hmmm = HighQualityVideo()
            try:
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        hmmm,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
                caption = f"🏷 **Judul:** [{songname}]({link})\n**👥 Chat ID:** `{chat_id}`\n💡 **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}"
                await xnxx.delete()
                await event.client.send_file(
                    chat_id, PLAY_PIC, caption=caption, reply_to=event.reply_to_msg_id
                )
            except AlreadyJoinedError:
                await call_py.leave_group_call(chat_id)
                clear_queue(chat_id)
                await xnxx.edit(
                    "**ERROR:** `Karena akun sedang berada di obrolan suara`\n\n• Silahkan Coba Play lagi"
                )
            except Exception as ep:
                clear_queue(chat_id)
                await xnxx.edit(f"`{ep}`")
    else:
        xnxx = await edit_or_reply(event, "`Searching...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit("**Tidak Menemukan Video untuk Keyword yang Diberikan**")
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            videoid = search[4]
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, videoid, ctitle)
            hm, ytlink = await ytdl(url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                caption = f"💡 **Video Ditambahkan Ke antrian »** `#{pos}`\n\n🏷 **Judul:** [{songname}]({url})\n**⏱ Durasi:** `{duration}`\n🎧 **Atas permintaan:** {from_user}"
                await xnxx.delete()
                await event.client.send_file(
                    chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            ytlink,
                            HighQualityAudio(),
                            hmmm,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Video", RESOLUSI)
                    caption = f"🏷 **Judul:** [{songname}]({url})\n**⏱ Durasi:** `{duration}`\n💡 **Status:** `Sedang Memutar Video`\n🎧 **Atas permintaan:** {from_user}"
                    await xnxx.delete()
                    await event.client.send_file(
                        chat_id, thumb, caption=caption, reply_to=event.reply_to_msg_id
                    )
                except AlreadyJoinedError:
                    await call_py.leave_group_call(chat_id)
                    clear_queue(chat_id)
                    await xnxx.edit(
                        "**ERROR:** `Karena akun sedang berada di obrolan suara`\n\n• Silahkan Coba Play lagi"
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await xnxx.edit(f"`{ep}`")


@man_cmd(pattern="end$", group_only=True)
async def vc_end(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await edit_or_reply(event, "**Menghentikan Streaming**")
        except Exception as e:
            await edit_delete(event, f"**ERROR:** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@man_cmd(pattern="skip(?:\s|$)([\s\S]*)", group_only=True)
async def vc_skip(event):
    chat_id = event.chat_id
    if len(event.text.split()) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await edit_delete(event, "**Tidak Sedang Memutar Streaming**")
        elif op == 1:
            await edit_delete(event, "antrian kosong, meninggalkan obrolan suara", 10)
        else:
            await edit_or_reply(
                event,
                f"**⏭ Melewati Lagu**\n**🎧 Sekarang Memutar** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**Menghapus Lagu Berikut Dari Antrian:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await skip_item(chat_id, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.edit(DELQUE)


@man_cmd(pattern="pause$", group_only=True)
async def vc_pause(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dijeda**")
        except Exception as e:
            await edit_delete(event, f"**ERROR:** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@man_cmd(pattern="resume$", group_only=True)
async def vc_resume(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await edit_or_reply(event, "**Streaming Dilanjutkan**")
        except Exception as e:
            await edit_or_reply(event, f"**ERROR:** `{e}`")
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@man_cmd(pattern=r"volume(?: |$)(.*)", group_only=True)
async def vc_volume(event):
    query = event.pattern_match.group(1)
    me = await event.client.get_me()
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    chat_id = event.chat_id
    if not admin and not creator:
        return await edit_delete(event, f"**Maaf {me.first_name} Bukan Admin 👮**", 30)

    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(query))
            await edit_or_reply(
                event, f"**Berhasil Mengubah Volume Menjadi** `{query}%`"
            )
        except Exception as e:
            await edit_delete(event, f"**ERROR:** `{e}`", 30)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@man_cmd(pattern="playlist$", group_only=True)
async def vc_playlist(event):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await edit_or_reply(
                event,
                f"**🎧 Sedang Memutar:**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview=False,
            )
        else:
            PLAYLIST = f"**🎧 Sedang Memutar:**\n**• [{chat_queue[0][0]}]({chat_queue[0][2]})** | `{chat_queue[0][3]}` \n\n**• Daftar Putar:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                PLAYLIST = PLAYLIST + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
            await edit_or_reply(event, PLAYLIST, link_preview=False)
    else:
        await edit_delete(event, "**Tidak Sedang Memutar Streaming**")


@call_py.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat_id = u.chat_id
    print(chat_id)
    await skip_current_song(chat_id)


@call_py.on_closed_voice_chat()
async def closedvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_left()
async def leftvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_kicked()
async def kickedvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


CMD_HELP.update(
    {
        "vcplugin": f"**Plugin : **`vcplugin`\
        \n\n  •  **Syntax :** `{cmd}play` <Judul Lagu/Link YT>\
        \n  •  **Function : **Untuk Memutar Lagu di voice chat group dengan akun kamu\
        \n\n  •  **Syntax :** `{cmd}vplay` <Judul Video/Link YT>\
        \n  •  **Function : **Untuk Memutar Video di voice chat group dengan akun kamu\
        \n\n  •  **Syntax :** `{cmd}end`\
        \n  •  **Function : **Untuk Memberhentikan video/lagu yang sedang putar di voice chat group\
        \n\n  •  **Syntax :** `{cmd}skip`\
        \n  •  **Function : **Untuk Melewati video/lagu yang sedang di putar\
        \n\n  •  **Syntax :** `{cmd}pause`\
        \n  •  **Function : **Untuk memberhentikan video/lagu yang sedang diputar\
        \n\n  •  **Syntax :** `{cmd}resume`\
        \n  •  **Function : **Untuk melanjutkan pemutaran video/lagu yang sedang diputar\
        \n\n  •  **Syntax :** `{cmd}volume` 1-200\
        \n  •  **Function : **Untuk mengubah volume (Membutuhkan Hak admin)\
        \n\n  •  **Syntax :** `{cmd}playlist`\
        \n  •  **Function : **Untuk menampilkan daftar putar Lagu/Video\
    "
    }
)
