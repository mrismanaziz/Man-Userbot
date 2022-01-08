# Copyright (C) 2020 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.utils import get_display_name

from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, LOGS
from userbot.modules.sql_helper.globals import addgvar, gvarstatus
from userbot.utils import edit_delete, edit_or_reply, man_cmd
from userbot.utils.tools import media_type


async def unsavegif(event, spammer):
    try:
        await event.client(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=spammer.media.document.id,
                    access_hash=spammer.media.document.access_hash,
                    file_reference=spammer.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception as e:
        LOGS.info(f"{e}")


async def spam_function(event, spammer, xnxx, sleeptimem, sleeptimet, DelaySpam=False):
    counter = int(xnxx[0])
    if len(xnxx) == 2:
        spam_message = str(xnxx[1])
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await spammer.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and spammer.media:
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            spammer = await event.client.send_file(
                event.chat_id, spammer, caption=spammer.text
            )
            await unsavegif(event, spammer)
            await asyncio.sleep(sleeptimem)
        if BOTLOG_CHATID:
            if DelaySpam is not True:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#SPAM\n"
                        + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#SPAM\n"
                        + f"Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) with {counter} times with below message",
                    )
            elif event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message with delay {sleeptimet} seconds",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) with {counter} times with below message with delay {sleeptimet} seconds",
                )

            spammer = await event.client.send_file(BOTLOG_CHATID, spammer)
            await unsavegif(event, spammer)
        return
    elif event.reply_to_msg_id and spammer.text:
        spam_message = spammer.text
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    else:
        return
    if DelaySpam is not True:
        if BOTLOG_CHATID:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat  with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
    elif BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                + f"`{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                + f"`{spam_message}`",
            )


@man_cmd(pattern="spam ([\s\S]*)")
async def nyespam(event):
    spammer = await event.get_reply_message()
    xnxx = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    try:
        counter = int(xnxx[0])
    except Exception:
        return await edit_delete(
            event,
            "**Gunakan sintaks yang tepat untuk spam. Ketik** `.help spam` **bila butuh bantuan.**",
        )
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, spammer, xnxx, sleeptimem, sleeptimet)


@man_cmd(pattern="sspam$")
async def stickerpack_spam(event):
    reply = await event.get_reply_message()
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await edit_delete(
            event,
            "**Balas stiker apa pun untuk mengirim semua stiker dalam paket itu**",
        )
    try:
        stickerset_attr = reply.document.attributes[1]
        xyz = await edit_or_reply(event, "`Mengambil detail Sticker Pack...`")
    except BaseException:
        await edit_delete(event, "**Ini bukan stiker. Silahkan Reply ke stiker.")
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                types.InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await edit_delete(
            xyz,
            "**Stiker ini bukan bagian dari sticker pack mana pun jadi saya tidak bisa kang paket stiker ini coba kang untuk stiker ini**",
        )
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    addgvar("spamwork", True)
    for m in reqd_sticker_set.documents:
        if gvarstatus("spamwork") is None:
            return
        await event.client.send_file(event.chat_id, m)
        await asyncio.sleep(0.7)
    if BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#STICKERPACK_SPAM\n"
                + f"Sticker Pack Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with pack ",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#STICKERPACK_SPAM\n"
                + f"Sticker Pack Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with pack",
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


@man_cmd(pattern="cspam ([\s\S]*)")
async def tmeme(event):
    cspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = cspam.replace(" ", "")
    await event.delete()
    addgvar("spamwork", True)
    for letter in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(letter)
    if BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with : `{message}`",
            )


@man_cmd(pattern="wspam ([\s\S]*)")
async def tmeme(event):
    wspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = wspam.split()
    await event.delete()
    addgvar("spamwork", True)
    for word in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(word)
    if BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with : `{message}`",
            )


@man_cmd(pattern="(delayspam|dspam) ([\s\S]*)")
async def dlyspam(event):
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await edit_delete(
            event,
            "**Gunakan sintaks yang tepat untuk delayspam. Ketik** `.help spam` **bila butuh bantuan.**",
        )
    xnxx = input_str[1:]
    try:
        int(xnxx[0])
    except Exception:
        return await edit_delete(
            event,
            "**Gunakan sintaks yang tepat untuk delayspam. Ketik** `.help spam` **bila butuh bantuan.**",
        )
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, reply, xnxx, sleeptimem, sleeptimet, DelaySpam=True)


CMD_HELP.update(
    {
        "spam": f"**Plugin : **`spam`\
        \n\n  •  **Syntax :** `{cmd}spam` <jumlah spam> <text>\
        \n  •  **Function : **Membanjiri teks dalam obrolan!!\
        \n\n  •  **Syntax :** `{cmd}cspam` <text>\
        \n  •  **Function : **Spam surat teks dengan huruf.\
        \n\n  •  **Syntax :** `{cmd}sspam` <reply sticker>\
        \n  •  **Function : **Spam sticker dari Seluruh isi Sticker Pack.\
        \n\n  •  **Syntax :** `{cmd}wspam` <text>\
        \n  •  **Function : **Spam kata teks demi kata.\
        \n\n  •  **Syntax :** `{cmd}picspam` <jumlah spam> <link image/gif>\
        \n  •  **Function : **Spam Foto Seolah-olah spam teks tidak cukup !!\
        \n\n  •  **Syntax :** `{cmd}delayspam` <detik> <jumlah spam> <text>\
        \n  •  **Function : **Spam surat teks dengan huruf.\
        \n\n  •  **NOTE : Spam dengan Risiko Anda sendiri**\
    "
    }
)
