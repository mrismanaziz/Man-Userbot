# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

import asyncio
from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import man_cmd


@man_cmd(pattern="cspam (.+)")
async def tmeme(e):
    cspam = str(e.pattern_match.group(1))
    message = cspam.replace(" ", "")
    await e.delete()
    for letter in message:
        await e.respond(letter)
    if BOTLOG_CHATID:
        await e.client.send_message(
            BOTLOG_CHATID, "#CSPAM\n" "TSpam was executed successfully"
        )


@man_cmd(pattern="wspam (.+)")
async def t_meme(e):
    wspam = str(e.pattern_match.group(1))
    message = wspam.split()
    await e.delete()
    for word in message:
        await e.respond(word)
    if BOTLOG_CHATID:
        await e.client.send_message(
            BOTLOG_CHATID, "#WSPAM\n" "WSpam was executed successfully"
        )


@man_cmd(pattern="spam (\d+) (.+)")
async def spammer(e):
    counter = int(e.pattern_match.group(1))
    spam_message = str(e.pattern_match.group(2))
    await e.delete()
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    if BOTLOG_CHATID:
        await e.client.send_message(
            BOTLOG_CHATID, "#SPAM\n" "Spam was executed successfully"
        )


@man_cmd(pattern="picspam (\d+) (.+)")
async def tiny_pic_spam(e):
    counter = int(e.pattern_match.group(1))
    link = str(e.pattern_match.group(2))
    await e.delete()
    for _ in range(1, counter):
        await e.client.send_file(e.chat_id, link)
    if BOTLOG_CHATID:
        await e.client.send_message(
            BOTLOG_CHATID, "#PICSPAM\n" "PicSpam was executed successfully"
        )


@man_cmd(pattern="delayspam (.*)")
async def spammer(e):
    spamDelay = float(e.pattern_match.group(1).split(" ", 2)[0])
    counter = int(e.pattern_match.group(1).split(" ", 2)[1])
    spam_message = str(e.pattern_match.group(1).split(" ", 2)[2])
    await e.delete()
    for _ in range(1, counter):
        await e.respond(spam_message)
        await sleep(spamDelay)
    if BOTLOG_CHATID:
        await e.client.send_message(
            BOTLOG_CHATID, "#DelaySPAM\n" "DelaySpam was executed successfully"
        )


CMD_HELP.update(
    {
        "spam": f"**Plugin : **`spam`\
        \n\n  •  **Syntax :** `{cmd}spam` <jumlah spam> <text>\
        \n  •  **Function : **Membanjiri teks dalam obrolan!! \
        \n\n  •  **Syntax :** `{cmd}cspam` <text>\
        \n  •  **Function : **Spam surat teks dengan huruf. \
        \n\n  •  **Syntax :** `{cmd}wspam` <text>\
        \n  •  **Function : **Spam kata teks demi kata. \
        \n\n  •  **Syntax :** `{cmd}picspam` <jumlah spam> <link image/gif>\
        \n  •  **Function : **Spam Foto Seolah-olah spam teks tidak cukup !! \
        \n\n  •  **Syntax :** `{cmd}delayspam` <detik> <jumlah spam> <text>\
        \n  •  **Function : **Spam surat teks dengan huruf. \
        \n\n  •  **NOTE : Spam dengan Risiko Anda sendiri**\
    "
    }
)
