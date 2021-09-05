# Copyright (C) 2021 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import time

from prettytable import PrettyTable

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils import _format, edit_delete, edit_or_reply, humanbytes, media_type

TYPES = [
    "Photo",
    "Audio",
    "Video",
    "Document",
    "Sticker",
    "Gif",
    "Voice",
    "Round Video",
]


def weird_division(n, d):
    return n / d if d else 0


@register(outgoing=True, pattern=r"^\.chatfs(?: |$)(.*)")
async def _(event):  # sourcery no-metrics
    "Shows you the complete media/file summary of the that group"
    entity = event.chat_id
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            entity = int(input_str)
        except ValueError:
            entity = input_str
    starttime = int(time.monotonic())
    x = PrettyTable()
    totalcount = totalsize = msg_count = 0
    x.title = "File Summary"
    x.field_names = ["Media", "Count", "File size"]
    largest = "   <b>Largest Size</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event,
            f"<b>Error : </b><code>{e}</code>",
            time=5,
            parse_mode="HTML",
        )

    if type(chatdata).__name__ == "Channel":
        if chatdata.username:
            link = f"<a href='t.me/{chatdata.username}'>{chatdata.title}</a>"
        else:
            link = chatdata.title
    else:
        link = f"<a href='tg://user?id={chatdata.id}'>{chatdata.first_name}</a>"
    event = await edit_or_reply(
        event,
        f"<b>Menghitung ukuran File dari group </b><code>{link}</code>\n<b>Harap Tunggu Ini mungkin memakan waktu yang lama tergantung pada jumlah pesan grup</b>",
        parse_mode="HTML",
    )
    media_dict = {
        m: {"file_size": 0, "count": 0, "max_size": 0, "max_file_link": ""}
        for m in TYPES
    }
    async for message in event.client.iter_messages(entity=entity, limit=None):
        msg_count += 1
        media = media_type(message)
        if media is not None:
            media_dict[media]["file_size"] += message.file.size
            media_dict[media]["count"] += 1
            if message.file.size > media_dict[media]["max_size"]:
                media_dict[media]["max_size"] = message.file.size
                if type(chatdata).__name__ == "Channel":
                    media_dict[media][
                        "max_file_link"
                    ] = f"https://t.me/c/{chatdata.id}/{message.id}"  # pylint: disable=line-too-long
                else:
                    media_dict[media][
                        "max_file_link"
                    ] = f"tg://openmessage?user_id={chatdata.id}&message_id={message.id}"  # pylint: disable=line-too-long
            totalsize += message.file.size
            totalcount += 1
    for mediax in TYPES:
        x.add_row(
            [
                mediax,
                media_dict[mediax]["count"],
                humanbytes(media_dict[mediax]["file_size"]),
            ]
        )
        if media_dict[mediax]["count"] != 0:
            largest += f"  •  <b><a href='{media_dict[mediax]['max_file_link']}'>{mediax}</a>  : </b><code>{humanbytes(media_dict[mediax]['max_size'])}</code>\n"
    endtime = int(time.monotonic())
    if endtime - starttime >= 120:
        runtime = str(round(((endtime - starttime) / 60), 2)) + " minutes"
    else:
        runtime = str(endtime - starttime) + " seconds"
    avghubytes = humanbytes(weird_division(totalsize, totalcount))
    avgruntime = (
        str(round((weird_division((endtime - starttime), totalcount)) * 1000, 2))
        + " ms"
    )
    totalstring = f"<b>Total Files :</b> <code>{totalcount}</code>\n<b>Total File Size :</b> <code>{humanbytes(totalsize)}</code>\n<b>Avg. File Size :</b> <code>{avghubytes}</code>\n"

    runtimestring = f"<b>Runtime :</b> <code>{runtime}</code>\
                        \n<b>Runtime per file :</b> <code>{avgruntime}</code>\
                        \n"
    line = "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
    result = f"<b>Group : {link}</b>\n\n"
    result += f"<b>Total Messages:</b><code> {msg_count}</code>\n"
    result += "<b>File Summary : </b>\n"
    result += f"<code>{x}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await event.edit(result, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.userfs(?: |$)(.*)")
async def _(event):  # sourcery no-metrics
    "Shows you the complete media/file summary of the that user in that group."
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if reply and input_str:
        try:
            entity = int(input_str)
        except ValueError:
            entity = input_str
        userentity = reply.sender_id
    elif reply:
        entity = event.chat_id
        userentity = reply.sender_id
    elif input_str:
        entity = event.chat_id
        try:
            userentity = int(input_str)
        except ValueError:
            userentity = input_str
    else:
        entity = event.chat_id
        userentity = event.sender_id
    starttime = int(time.monotonic())
    x = PrettyTable()
    totalcount = totalsize = msg_count = 0
    x.title = "File Summary"
    x.field_names = ["Media", "Count", "File size"]
    largest = "   <b>Largest Size</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>Error : </b><code>{e}</code>", 5, parse_mode="HTML"
        )

    try:
        userdata = await event.client.get_entity(userentity)
    except Exception as e:
        return await edit_delete(
            event,
            f"<b>Error : </b><code>{e}</code>",
            time=5,
            parse_mode="HTML",
        )

    if type(chatdata).__name__ == "Channel":
        if chatdata.username:
            link = f"<a href='t.me/{chatdata.username}'>{chatdata.title}</a>"
        else:
            link = chatdata.title
    else:
        link = f"<a href='tg://user?id={chatdata.id}'>{chatdata.first_name}</a>"
    event = await edit_or_reply(
        event,
        f"<b>Menghitung ukuran File yang dikirim </b>{_format.htmlmentionuser(userdata.first_name,userdata.id)}<b> di Grup </b><code>{link}</code>\n<b>Harap Tunggu Ini mungkin memakan waktu yang lama tergantung pada jumlah pesan grup</b>",
        parse_mode="HTML",
    )

    media_dict = {
        m: {"file_size": 0, "count": 0, "max_size": 0, "max_file_link": ""}
        for m in TYPES
    }
    async for message in event.client.iter_messages(
        entity=entity, limit=None, from_user=userentity
    ):
        msg_count += 1
        media = media_type(message)
        if media is not None:
            media_dict[media]["file_size"] += message.file.size
            media_dict[media]["count"] += 1
            if message.file.size > media_dict[media]["max_size"]:
                media_dict[media]["max_size"] = message.file.size
                if type(chatdata).__name__ == "Channel":
                    media_dict[media][
                        "max_file_link"
                    ] = f"https://t.me/c/{chatdata.id}/{message.id}"
                else:
                    media_dict[media][
                        "max_file_link"
                    ] = f"tg://openmessage?user_id={chatdata.id}&message_id={message.id}"
            totalsize += message.file.size
            totalcount += 1
    for mediax in TYPES:
        x.add_row(
            [
                mediax,
                media_dict[mediax]["count"],
                humanbytes(media_dict[mediax]["file_size"]),
            ]
        )
        if media_dict[mediax]["count"] != 0:
            largest += f"  •  <b><a href='{media_dict[mediax]['max_file_link']}'>{mediax}</a>  : </b><code>{humanbytes(media_dict[mediax]['max_size'])}</code>\n"
    endtime = int(time.monotonic())
    if endtime - starttime >= 120:
        runtime = str(round(((endtime - starttime) / 60), 2)) + " minutes"
    else:
        runtime = str(endtime - starttime) + " seconds"
    avghubytes = humanbytes(weird_division(totalsize, totalcount))
    avgruntime = (
        str(round((weird_division((endtime - starttime), totalcount)) * 1000, 2))
        + " ms"
    )
    totalstring = f"<b>Total Files :</b> <code>{totalcount}</code>\n<b>Total File Size :</b> <code>{humanbytes(totalsize)}</code>\n<b>Avg. File Size :</b> <code>{avghubytes}\\\x1f \n</code>"

    runtimestring = f"<b>Runtime :</b> <code>{runtime}</code>\
                    \n<b>Runtime Per File :</b> <code>{avgruntime}</code>\
                    \n"
    line = "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
    result = f"<b>Group : {link}\nUser : {_format.htmlmentionuser(userdata.first_name,userdata.id)}</b>\n\n"
    result += f"<b>Total Messages:</b> <code>{msg_count}</code>\n"
    result += "<b>File Summary : </b>\n"
    result += f"<code>{x}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await event.edit(result, parse_mode="HTML", link_preview=False)


CMD_HELP.update(
    {
        "file-summary": "**Plugin : **`file-summery`\
        \n\n  •  **Syntax :** `.chatfs` <username/id>\
        \n  •  **Function : **Untuk Menampilkan ringkasan media/file lengkap dari grup itu\
        \n\n  •  **Syntax :** `.userfs` <reply/username/id>\
        \n  •  **Function : **Untuk Menampilkan ringkasan media/file lengkap dari anggota group tersebut.\
        \n\n  •  **NOTE :** Untuk sekarang terbatas pada 10.000 terakhir di grup yang Anda gunakan\
    "
    }
)
