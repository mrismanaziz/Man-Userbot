# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import io
import math
import random
import urllib.request
from os import remove

import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot import S_PACK_NAME as custompack
from userbot import bot
from userbot.events import man_cmd
from userbot.utils import edit_or_reply

KANGING_STR = [
    "Colong Sticker dulu yee kan",
    "Ini Sticker aku colong yaa DUARR!",
    "Waw Stickernya Bagus Nih...Colong Dulu Yekan..",
    "ehh, keren nih... gua colong ya stickernya...",
    "Boleh juga ni Sticker Colong ahh~",
]


@bot.on(man_cmd(outgoing=True, pattern=r"(?:tikel|kang)\s?(.)?"))
async def kang(args):
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None

    if not message or not message.media:
        return await args.edit("`Maaf , Saya Gagal Mengambil Sticker Ini!`")

    if isinstance(message.media, MessageMediaPhoto):
        await args.edit(f"`{random.choice(KANGING_STR)}`")
        photo = io.BytesIO()
        photo = await bot.download_media(message.photo, photo)
    elif "image" in message.media.document.mime_type.split("/"):
        await args.edit(f"`{random.choice(KANGING_STR)}`")
        photo = io.BytesIO()
        await bot.download_file(message.media.document, photo)
        if (
            DocumentAttributeFilename(file_name="sticker.webp")
            in message.media.document.attributes
        ):
            emoji = message.media.document.attributes[1].alt
            if emoji != "✨":
                emojibypass = True
    elif "tgsticker" in message.media.document.mime_type:
        await args.edit(f"`{random.choice(KANGING_STR)}`")
        await bot.download_file(message.media.document, "AnimatedSticker.tgs")

        attributes = message.media.document.attributes
        for attribute in attributes:
            if isinstance(attribute, DocumentAttributeSticker):
                emoji = attribute.alt

        emojibypass = True
        is_anim = True
        photo = 1
    else:
        return await args.edit("`File Tidak Didukung !`")
    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "✨"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # User sent both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # User wants to push into different pack, but is okay with
                # thonk as emote.
                pack = int(splat[1])
            else:
                # User sent just custom emote, wants to push to default
                # pack
                emoji = splat[1]

        u_id = user.id
        f_name = user.first_name
        packname = f"Sticker_u{u_id}_Ke{pack}"
        custom_packnick = f"{custompack}" or f"{f_name} Sticker Pack"
        packnick = f"{custom_packnick}"
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with bot.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"Sticker_u{u_id}_Ke{pack}"
                    packnick = f"{custom_packnick}"
                    await args.edit(
                        "`Membuat Sticker Pack Baru "
                        + str(pack)
                        + " Karena Sticker Pack Sudah Penuh`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Gagal Memilih Pack.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        return await args.edit(
                            "`Sticker ditambahkan ke pack yang berbeda !"
                            "\nIni pack yang baru saja dibuat!"
                            f"\nTekan [Sticker Pack](t.me/addstickers/{packname}) Untuk Melihat Sticker Pack",
                            parse_mode="md",
                        )
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await args.edit(
                        "**Gagal Menambahkan Sticker, Gunakan @Stickers Bot Untuk Menambahkan Sticker Anda.**"
                    )
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("`Membuat Sticker Pack Baru`")
            async with bot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await args.edit(
                        "**Gagal Menambahkan Sticker, Gunakan @Stickers Bot Untuk Menambahkan Sticker.**"
                    )
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)

        await args.edit(
            "** Sticker Berhasil Ditambahkan!**"
            f"\n        👻 **[KLIK DISINI](t.me/addstickers/{packname})** 👻\n**Untuk Menggunakan Stickers**",
            parse_mode="md",
        )


async def resize_photo(photo):
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if size1 > size2:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)

    return image


@bot.on(man_cmd(outgoing=True, pattern=r"stickerinfo$"))
async def get_pack_info(event):
    if not event.is_reply:
        return await event.edit("**Mohon Balas Ke Sticker**")

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await event.edit("**Balas ke sticker untuk melihat detail pack**")

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        await event.edit("`Processing...`")
    except BaseException:
        return await event.edit("**Ini bukan sticker, Mohon balas ke sticker.**")

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await event.edit("**Ini bukan sticker, Mohon balas ke sticker.**")

    get_stickerset = await bot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"➠ **Nama Sticker:** [{get_stickerset.set.title}](http://t.me/addstickers/{get_stickerset.set.short_name})\n"
        f"➠ **Official:** `{get_stickerset.set.official}`\n"
        f"➠ **Arsip:** `{get_stickerset.set.archived}`\n"
        f"➠ **Sticker Dalam Pack:** `{len(get_stickerset.packs)}`\n"
        f"➠ **Emoji Dalam Pack:** {' '.join(pack_emojis)}"
    )

    await event.edit(OUTPUT)


@bot.on(man_cmd(outgoing=True, pattern=r"delsticker ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("**Mohon Reply ke Sticker yang ingin anda Hapus.**")
        return
    reply_message = await event.get_reply_message()
    chat = "@Stickers"
    if reply_message.sender.bot:
        await edit_or_reply(event, "**Mohon Reply ke Sticker.**")
        return
    await event.edit("`Processing...`")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=429000)
            )
            await conv.send_message("/delsticker")
            await conv.get_response()
            await asyncio.sleep(2)
            await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("**Silahkan Buka Blokir @Stikers dan coba lagi**")
            return
        if response.text.startswith(
            "Sorry, I can't do this, it seems that you are not the owner of the relevant pack."
        ):
            await event.edit(
                "**Maaf, Sepertinya Anda bukan Pemilik Sticker pack ini.**"
            )
        elif response.text.startswith(
            "You don't have any sticker packs yet. You can create one using the /newpack command."
        ):
            await event.edit("**Anda Tidak Memiliki Stiker untuk di Hapus**")
        elif response.text.startswith("Please send me the sticker."):
            await event.edit("**Tolong Reply ke Sticker yang ingin dihapus**")
        elif response.text.startswith("Invalid pack selected."):
            await event.edit("**Maaf Paket yang dipilih tidak valid.**")
        else:
            await event.edit("**Berhasil Menghapus Stiker.**")


@bot.on(man_cmd(outgoing=True, pattern=r"editsticker ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("**Mohon Reply ke Sticker dan Berikan emoji.**")
        return
    reply_message = await event.get_reply_message()
    emot = event.pattern_match.group(1)
    if reply_message.sender.bot:
        await edit_or_reply(event, "**Mohon Reply ke Sticker.**")
        return
    await event.edit("`Processing...`")
    if emot == "":
        await event.edit("**Silahkan Kirimkan Emot Baru.**")
    else:
        chat = "@Stickers"
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=429000)
                )
                await conv.send_message("/editsticker")
                await conv.get_response()
                await asyncio.sleep(2)
                await bot.forward_messages(chat, reply_message)
                await conv.get_response()
                await asyncio.sleep(2)
                await conv.send_message(f"{emot}")
                response = await response
            except YouBlockedUserError:
                await event.reply("**Buka blokir @Stiker dan coba lagi**")
                return
            if response.text.startswith("Invalid pack selected."):
                await event.edit("**Maaf Paket yang dipilih tidak valid.**")
            elif response.text.startswith(
                "Please send us an emoji that best describes your sticker."
            ):
                await event.edit(
                    "**Silahkan Kirimkan emoji yang paling menggambarkan stiker Anda.**"
                )
            else:
                await event.edit(
                    f"**Berhasil Mengedit Emoji Stiker**\n**Emoji Baru:** {emot}"
                )


@bot.on(man_cmd(outgoing=True, pattern=r"getsticker$"))
async def sticker_to_png(sticker):
    if not sticker.is_reply:
        await sticker.edit("`NULL information to fetch...`")
        return False

    img = await sticker.get_reply_message()
    if not img.document:
        await sticker.edit("`Mohon Balas Ke Sticker`")
        return False

    try:
        img.document.attributes[1]
    except Exception:
        await sticker.edit("`Maaf , Ini Bukanlah Sticker`")
        return

    with io.BytesIO() as image:
        await sticker.client.download_media(img, image)
        image.name = "sticker.png"
        image.seek(0)
        try:
            await img.reply(file=image, force_document=True)
        except Exception:
            await sticker.edit("`Tidak Dapat Mengirim File...`")
        else:
            await sticker.delete()
    return


@bot.on(man_cmd(outgoing=True, pattern=r"stickers ?([\s\S]*)"))
async def cb_sticker(event):
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("**Masukan Nama Sticker Pack!**")
    await event.edit("`Searching sticker packs...`")
    text = requests.get("https://combot.org/telegram/stickers?q=" + query).text
    soup = bs(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        return await event.edit("**Tidak Dapat Menemukan Sticker Pack 🥺**")
    reply = f"**Keyword Sticker Pack:**\n {query}\n\n**Hasil:**\n"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            reply += f" •  [{packtitle}]({packlink})\n"
    await event.edit(reply)


CMD_HELP.update(
    {
        "stickers": f"**Plugin : **`stickers`\
        \n\n  •  **Syntax :** `{cmd}kang` atau `{cmd}tikel` [emoji]\
        \n  •  **Function : **Balas .kang Ke Sticker Atau Gambar Untuk Menambahkan Ke Sticker Pack Mu\
        \n\n  •  **Syntax :** `{cmd}kang` [emoji] atau `{cmd}tikel` [emoji]\
        \n  •  **Function : **Balas {cmd}kang emoji Ke Sticker Atau Gambar Untuk Menambahkan dan costum emoji sticker Ke Pack Mu\
        \n\n  •  **Syntax :** `{cmd}delsticker` <reply sticker>\
        \n  •  **Function : **Untuk Menghapus sticker dari Sticker Pack.\
        \n\n  •  **Syntax :** `{cmd}editsticker` <reply sticker> <emoji>\
        \n  •  **Function : **Untuk Mengedit emoji stiker dengan emoji yang baru.\
        \n\n  •  **Syntax :** `{cmd}stickerinfo`\
        \n  •  **Function : **Untuk Mendapatkan Informasi Sticker Pack.\
        \n\n  •  **Syntax :** `{cmd}stickers` <nama sticker pack >\
        \n  •  **Function : **Untuk Mencari Sticker Pack.\
        \n\n  •  **NOTE:** Untuk Membuat Sticker Pack baru Gunakan angka dibelakang `{cmd}kang`\
        \n  •  **CONTOH:** `{cmd}kang 2` untuk membuat dan menyimpan ke sticker pack ke 2\
    "
    }
)


CMD_HELP.update(
    {
        "sticker_v2": f"**Plugin : **`stickers`\
        \n\n  •  **Syntax :** `{cmd}getsticker`\
        \n  •  **Function : **Balas Ke Stcker Untuk Mendapatkan File 'PNG' Sticker.\
        \n\n  •  **Syntax :** `{cmd}get`\
        \n  •  **Function : **Balas ke sticker untuk mendapatkan file 'PNG' sticker\
        \n\n  •  **Syntax :** `{cmd}stoi`\
        \n  •  **Function : **Balas Ke Stcker Untuk Mendapatkan File 'PNG' Sticker.\
        \n\n  •  **Syntax :** `{cmd}itos`\
        \n  •  **Function : **Balas ke sticker atau gambar .itos untuk mengambil sticker bukan ke pack\
    "
    }
)
