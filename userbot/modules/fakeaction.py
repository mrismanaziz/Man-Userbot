# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# @SharingUserbot

import asyncio

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"ftyping(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai Pengetikan Palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"faudio(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai merekam audio palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "record-audio"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fvideo(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai merekam video palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "record-video"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fgame(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai Bermain Game Palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "game"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fround(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai merekam video message palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "record-round"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fphoto(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai Mengirim Photo Palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "photo"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fdocument(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai Mengirim Document Palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "document"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"flocation(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai Share Lokasi Palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "location"):
        await asyncio.sleep(t)


@bot.on(man_cmd(outgoing=True, pattern=r"fcontact(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Masukan jumlah detik yang benar`")
    await event.edit(f"**Memulai Mengirim Contact Palsu Selama** `{t}` **detik.**")
    await asyncio.sleep(3)
    await event.delete()
    async with event.client.action(event.chat_id, "contact"):
        await asyncio.sleep(t)


CMD_HELP.update(
    {
        "fakeaction": f"**Plugin :** `fakeaction`\
        \n\n  •  **Syntax :** `{cmd}ftyping`  <jumlah detik>\
        \n  •  **Function :** Menampilkan Pengetikan Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}faudio` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Merekam suara Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fvideo` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Merekam Video Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fround` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Merekam Live Video Round Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fgame` <jumlah detik>\
        \n  •  **Function :** Menampilkan sedang bermain game Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fphoto` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Mengirim Photo Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fdocument` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Mengirim Document/File Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}flocation` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Share Lokasi Palsu dalam obrolan\
        \n\n  •  **Syntax :** `{cmd}fcontact` <jumlah detik>\
        \n  •  **Function :** Menampilkan Tindakan Share Contact Palsu dalam obrolan\
    "
    }
)
