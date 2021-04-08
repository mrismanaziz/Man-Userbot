# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
# thanks to anishsk

from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.lock ?(.*)")
async def locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = True
        what = "Pesan"
    elif input_str == "media":
        media = True
        what = "Media"
    elif input_str == "sticker":
        sticker = True
        what = "Sticker"
    elif input_str == "gif":
        gif = True
        what = "GIF"
    elif input_str == "game":
        gamee = True
        what = "Game"
    elif input_str == "inline":
        ainline = True
        what = "Inline Bot"
    elif input_str == "poll":
        gpoll = True
        what = "Poll"
    elif input_str == "invite":
        adduser = True
        what = "Invite"
    elif input_str == "pin":
        cpin = True
        what = "Pin"
    elif input_str == "info":
        changeinfo = True
        what = "Info"
    elif input_str == "all":
        msg = True
        media = True
        sticker = True
        gif = True
        gamee = True
        ainline = True
        gpoll = True
        adduser = True
        cpin = True
        changeinfo = True
        what = "Semuanya"
    else:
        if not input_str:
            await event.edit("`Mohon Maaf, Apa Yang Harus Saya Kunci?`")
            return
        else:
            await event.edit(f"`Jenis Yang Mau Anda Kunci Tidak Valid` `{input_str}`")
            return

    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights)
        )
        await event.edit(f"`Master Telah Mengunci {what} Untuk Obrolan Ini!!`")
    except BaseException as e:
        await event.edit(
            f"`Apakah Master Mempunyai Izin Melakukan Itu Disini?`\n**Kesalahan:** {str(e)}"
        )
        return


@register(outgoing=True, pattern=r"^.unlock ?(.*)")
async def rem_locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = False
        what = "Pesan"
    elif input_str == "media":
        media = False
        what = "Media"
    elif input_str == "sticker":
        sticker = False
        what = "Sticker"
    elif input_str == "gif":
        gif = False
        what = "GIF"
    elif input_str == "game":
        gamee = False
        what = "Game"
    elif input_str == "inline":
        ainline = False
        what = "Inline"
    elif input_str == "poll":
        gpoll = False
        what = "Poll"
    elif input_str == "invite":
        adduser = False
        what = "Invite"
    elif input_str == "pin":
        cpin = False
        what = "Pin"
    elif input_str == "info":
        changeinfo = False
        what = "Info"
    elif input_str == "all":
        msg = False
        media = False
        sticker = False
        gif = False
        gamee = False
        ainline = False
        gpoll = False
        adduser = False
        cpin = False
        changeinfo = False
        what = "Semuanya"
    else:
        if not input_str:
            await event.edit("`Apa Yang Harus Saya Buka?`")
            return
        else:
            await event.edit(
                f"`Jenis Kunci Yang Mau Anda Buka Tidak Valid` `{input_str}`"
            )
            return

    unlock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(
                peer=peer_id, banned_rights=unlock_rights
            )
        )
        await event.edit(f"`Master Telah Membuka Kunci {what} Untuk Obrolan Ini!!`")
    except BaseException as e:
        await event.edit(
            f"`Apakah Master Mempunyai Izin Melakukan Itu Disini?`\n**Kesalahan:** {str(e)}"
        )
        return


CMD_HELP.update(
    {
        "locks": "**Plugin : **`locks`\
        \n\n  •  **Syntax :** `.lock` <all atau Jenis lock>\
        \n  •  **Function : **Memungkinkan anda Mengunci beberapa jenis pesan dalam obrolan.\
        \n\n  •  **Syntax :** `.unlock` <all atau Jenis lock>\
        \n  •  **Function : **Untuk membuka kunci, beberapa jenis pesan dalam obrolan.\
        \n\n  •  **Jenis pesan yang bisa dikunci atau dibuka adalah:**\
        \n  •  `all, msg, media, sticker, gif, game, inline, poll, invite, pin, info`\
        \n\n  •  **Contoh :** `.lock msg` atau `.unlock msg`\
    "
    }
)
