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
from telethon.errors import PackShortNameOccupiedError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)
from telethon.utils import get_input_document

from userbot import BOT_USERNAME
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot import S_PACK_NAME as custompack
from userbot import tgbot
from userbot.modules.sql_helper.globals import addgvar, gvarstatus
from userbot.utils import edit_delete, edit_or_reply, man_cmd

KANGING_STR = [
    "Colong Sticker dulu yee kan",
    "Ini Sticker aku colong yaa DUARR!",
    "Waw Stickernya Bagus Nih...Colong Dulu Yekan..",
    "ehh, keren nih... gua colong ya stickernya...",
    "Boleh juga ni Sticker Colong ahh~",
]


@man_cmd(pattern="(?:tikel|kang)\s?(.)?")
async def kang(args):
    user = await args.client.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None

    if not message or not message.media:
        return await edit_delete(
            args, "**Silahkan Reply Ke Pesan Media Untuk Mencuri Sticker itu!**"
        )

    if isinstance(message.media, MessageMediaPhoto):
        xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
        photo = io.BytesIO()
        photo = await args.client.download_media(message.photo, photo)
    elif "image" in message.media.document.mime_type.split("/"):
        xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
        photo = io.BytesIO()
        await args.client.download_file(message.media.document, photo)
        if (
            DocumentAttributeFilename(file_name="sticker.webp")
            in message.media.document.attributes
        ):
            emoji = message.media.document.attributes[1].alt
            if emoji != "✨":
                emojibypass = True
    elif "tgsticker" in message.media.document.mime_type:
        xx = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
        await args.client.download_file(message.media.document, "AnimatedSticker.tgs")

        attributes = message.media.document.attributes
        for attribute in attributes:
            if isinstance(attribute, DocumentAttributeSticker):
                emoji = attribute.alt

        emojibypass = True
        is_anim = True
        photo = 1
    else:
        return await xx.edit("**File Tidak Didukung, Silahkan Reply ke Media Foto !**")
    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "✨"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                pack = int(splat[1])
            else:
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
            async with args.client.conversation("@Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"Sticker_u{u_id}_Ke{pack}"
                    packnick = f"{custom_packnick}"
                    await xx.edit(
                        "`Membuat Sticker Pack Baru "
                        + str(pack)
                        + " Karena Sticker Pack Sudah Penuh`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Gagal Memilih Pack.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        await args.client.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response()
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        await args.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await args.client.send_read_acknowledge(conv.chat_id)
                        return await xx.edit(
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
                    return await xx.edit(
                        "**Gagal Menambahkan Sticker, Gunakan @Stickers Bot Untuk Menambahkan Sticker Anda.**"
                    )
                await conv.send_message(emoji)
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
        else:
            await xx.edit("`Membuat Sticker Pack Baru`")
            async with args.client.conversation("@Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await xx.edit(
                        "**Gagal Menambahkan Sticker, Gunakan @Stickers Bot Untuk Menambahkan Sticker.**"
                    )
                await conv.send_message(emoji)
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                await args.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await args.client.send_read_acknowledge(conv.chat_id)

        await xx.edit(
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


@man_cmd(pattern="pkang(?:\\s|$)([\\s\\S]*)")
async def _(event):
    xnxx = await edit_or_reply(event, f"`{random.choice(KANGING_STR)}`")
    reply = await event.get_reply_message()
    query = event.text[7:]
    bot_ = BOT_USERNAME
    bot_un = bot_.replace("@", "")
    user = await event.client.get_me()
    OWNER_ID = user.id
    un = f"@{user.username}" if user.username else user.first_name
    un_ = user.username or OWNER_ID
    if not reply:
        return await edit_delete(
            xnxx, "**Mohon Balas sticker untuk mencuri semua Sticker Pack itu.**"
        )
    pname = f"{un} Sticker Pack" if query == "" else query
    if reply.media and reply.media.document.mime_type == "image/webp":
        tikel_id = reply.media.document.attributes[1].stickerset.id
        tikel_hash = reply.media.document.attributes[1].stickerset.access_hash
        got_stcr = await event.client(
            functions.messages.GetStickerSetRequest(
                stickerset=types.InputStickerSetID(id=tikel_id, access_hash=tikel_hash),
                hash=0,
            )
        )
        stcrs = []
        for sti in got_stcr.documents:
            inp = get_input_document(sti)
            stcrs.append(
                types.InputStickerSetItem(
                    document=inp,
                    emoji=(sti.attributes[1]).alt,
                )
            )
        try:
            gvarstatus("PKANG")
        except BaseException:
            addgvar("PKANG", "0")
        x = gvarstatus("PKANG")
        try:
            pack = int(x) + 1
        except BaseException:
            pack = 1
        await xnxx.edit(f"`{random.choice(KANGING_STR)}`")
        try:
            create_st = await tgbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=OWNER_ID,
                    title=pname,
                    short_name=f"man_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        except PackShortNameOccupiedError:
            await asyncio.sleep(1)
            await xnxx.edit("`Sedang membuat paket baru...`")
            pack += 1
            create_st = await tgbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=OWNER_ID,
                    title=pname,
                    short_name=f"man_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        await xnxx.edit(
            f"**Berhasil Mencuri Sticker Pack,** [Klik Disini](t.me/addstickers/{create_st.set.short_name}) **Untuk Melihat Pack anda**"
        )
    else:
        await xnxx.edit("**Berkas Tidak Didukung. Harap Balas ke stiker saja.**")


@man_cmd(pattern="stickerinfo$")
async def get_pack_info(event):
    if not event.is_reply:
        return await edit_delete(event, "**Mohon Balas Ke Sticker**")

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await edit_delete(
            event, "**Balas ke sticker untuk melihat detail pack**"
        )

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        xx = await edit_or_reply(event, "`Processing...`")
    except BaseException:
        return await edit_delete(xx, "**Ini bukan sticker, Mohon balas ke sticker.**")

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await edit_delete(xx, "**Ini bukan sticker, Mohon balas ke sticker.**")

    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            ),
            hash=0,
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

    await xx.edit(OUTPUT)


@man_cmd(pattern="delsticker ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(event, "**Mohon Reply ke Sticker yang ingin anda Hapus.**")
        return
    reply_message = await event.get_reply_message()
    chat = "@Stickers"
    if reply_message.sender.bot:
        await edit_delete(event, "**Mohon Reply ke Sticker.**")
        return
    xx = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=429000)
            )
            await conv.send_message("/delsticker")
            await conv.get_response()
            await asyncio.sleep(2)
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message("/delsticker")
            await conv.get_response()
            await asyncio.sleep(2)
            await event.client.forward_messages(chat, reply_message)
            response = await response
        if response.text.startswith(
            "Sorry, I can't do this, it seems that you are not the owner of the relevant pack."
        ):
            await xx.edit("**Maaf, Sepertinya Anda bukan Pemilik Sticker pack ini.**")
        elif response.text.startswith(
            "You don't have any sticker packs yet. You can create one using the /newpack command."
        ):
            await xx.edit("**Anda Tidak Memiliki Stiker untuk di Hapus**")
        elif response.text.startswith("Please send me the sticker."):
            await xx.edit("**Tolong Reply ke Sticker yang ingin dihapus**")
        elif response.text.startswith("Invalid pack selected."):
            await xx.edit("**Maaf Paket yang dipilih tidak valid.**")
        else:
            await xx.edit("**Berhasil Menghapus Stiker.**")


@man_cmd(pattern="editsticker ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(event, "**Mohon Reply ke Sticker dan Berikan emoji.**")
        return
    reply_message = await event.get_reply_message()
    emot = event.pattern_match.group(1)
    if reply_message.sender.bot:
        await edit_delete(event, "**Mohon Reply ke Sticker.**")
        return
    xx = await edit_or_reply(event, "`Processing...`")
    if emot == "":
        await xx.edit("**Silahkan Kirimkan Emot Baru.**")
    else:
        chat = "@Stickers"
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=429000)
                )
                await conv.send_message("/editsticker")
                await conv.get_response()
                await asyncio.sleep(2)
                await event.client.forward_messages(chat, reply_message)
                await conv.get_response()
                await asyncio.sleep(2)
                await conv.send_message(f"{emot}")
                response = await response
            except YouBlockedUserError:
                await event.client(UnblockRequest(chat))
                await conv.send_message("/editsticker")
                await conv.get_response()
                await asyncio.sleep(2)
                await event.client.forward_messages(chat, reply_message)
                await conv.get_response()
                await asyncio.sleep(2)
                await conv.send_message(f"{emot}")
                response = await response
            if response.text.startswith("Invalid pack selected."):
                await xx.edit("**Maaf Paket yang dipilih tidak valid.**")
            elif response.text.startswith(
                "Please send us an emoji that best describes your sticker."
            ):
                await xx.edit(
                    "**Silahkan Kirimkan emoji yang paling menggambarkan stiker Anda.**"
                )
            else:
                await xx.edit(
                    f"**Berhasil Mengedit Emoji Stiker**\n**Emoji Baru:** {emot}"
                )


@man_cmd(pattern="getsticker$")
async def sticker_to_png(sticker):
    if not sticker.is_reply:
        await edit_delete(sticker, "**Harap balas ke stiker**")
        return False
    img = await sticker.get_reply_message()
    if not img.document:
        await edit_delete(sticker, "**Maaf , Ini Bukan Sticker**")
        return False
    xx = await edit_or_reply(sticker, "`Berhasil Mengambil Sticker!`")
    image = io.BytesIO()
    await sticker.client.download_media(img, image)
    image.name = "sticker.png"
    image.seek(0)
    await sticker.client.send_file(
        sticker.chat_id, image, reply_to=img.id, force_document=True
    )
    await xx.delete()


@man_cmd(pattern="stickers ?([\s\S]*)")
async def cb_sticker(event):
    query = event.pattern_match.group(1)
    if not query:
        return await edit_delete(event, "**Masukan Nama Sticker Pack!**")
    xx = await edit_or_reply(event, "`Searching sticker packs...`")
    text = requests.get("https://combot.org/telegram/stickers?q=" + query).text
    soup = bs(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        return await edit_delete(xx, "**Tidak Dapat Menemukan Sticker Pack 🥺**")
    reply = f"**Keyword Sticker Pack:**\n {query}\n\n**Hasil:**\n"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            reply += f" •  [{packtitle}]({packlink})\n"
    await xx.edit(reply)


@man_cmd(pattern="itos$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(
            event, "sir this is not a image message reply to image message"
        )
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_delete(event, "sir, This is not a image ")
        return
    chat = "@buildstickerbot"
    xx = await edit_or_reply(event, "Membuat Sticker..")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164977173)
            )
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        if response.text.startswith("Hi!"):
            await xx.edit(
                "Can you kindly disable your forward privacy settings for good?"
            )
        else:
            await xx.delete()
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, response.message)
            await event.client.delete_message(event.chat_id, [msg.id, response.id])


@man_cmd(pattern="get$")
async def _(event):
    rep_msg = await event.get_reply_message()
    if not event.is_reply or not rep_msg.sticker:
        return await edit_delete(event, "**Harap balas ke stiker**")
    xx = await edit_or_reply(event, "`Mengconvert ke foto...`")
    foto = io.BytesIO()
    foto = await event.client.download_media(rep_msg.sticker, foto)
    im = Image.open(foto).convert("RGB")
    im.save("sticker.png", "png")
    await event.client.send_file(
        event.chat_id,
        "sticker.png",
        reply_to=rep_msg,
    )
    await xx.delete()
    remove("sticker.png")


CMD_HELP.update(
    {
        "stickers": f"**Plugin : **`stickers`\
        \n\n  •  **Syntax :** `{cmd}kang` atau `{cmd}tikel` [emoji]\
        \n  •  **Function : **Balas .kang Ke Sticker Atau Gambar Untuk Menambahkan Ke Sticker Pack Mu\
        \n\n  •  **Syntax :** `{cmd}kang` [emoji] atau `{cmd}tikel` [emoji]\
        \n  •  **Function : **Balas {cmd}kang emoji Ke Sticker Atau Gambar Untuk Menambahkan dan costum emoji sticker Ke Pack Mu\
        \n\n  •  **Syntax :** `{cmd}pkang` <nama sticker pack>\
        \n  •  **Function : **Balas {cmd}pkang Ke Sticker Untuk Mencuri semua sticker pack tersebut\
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
        \n  •  **Function : **Balas ke sticker untuk mendapatkan foto sticker\
        \n\n  •  **Syntax :** `{cmd}itos`\
        \n  •  **Function : **Balas ke foto untuk membuat foto menjadi sticker\
    "
    }
)
