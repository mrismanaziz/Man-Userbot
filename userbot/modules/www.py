# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

import time
from datetime import datetime

from speedtest import Speedtest

from userbot import ALIVE_NAME, CMD_HELP, StartTime
from userbot.events import register
from userbot.utils import humanbytes


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern=r"^\.ping$")
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("**✣**")
    await pong.edit("**✣✣**")
    await pong.edit("**✣✣✣**")
    await pong.edit("**✣✣✣✣**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(
        f"**PONG𖣘𖣘~~~~**\n"
        f"✣ **Pinger** - `%sms`\n"
        f"✣ **Uptime -** `{uptime}` \n"
        f"**✦҈͜͡Owner :** `{ALIVE_NAME}`" % (duration)
    )


@register(outgoing=True, pattern=r"^\.xping$")
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`Pinging....`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(
        f"**PONG!! 🍭**\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration)
    )


@register(outgoing=True, pattern=r"^\.lping$")
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("**★ PING ★**")
    await pong.edit("**★★ PING ★★**")
    await pong.edit("**★★★ PING ★★★**")
    await pong.edit("**★★★★ PING ★★★★**")
    await pong.edit("**✦҈͜͡➳ PONG!**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(
        f"❃ **Ping !!** "
        f"`%sms` \n"
        f"❃ **Uptime -** "
        f"`{uptime}` \n"
        f"**✦҈͜͡➳ Master :** `{ALIVE_NAME}`" % (duration)
    )


@register(outgoing=True, pattern=r"^\.fping$")
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit(".                       /¯ )")
    await pong.edit(".                       /¯ )\n                      /¯  /")
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /"
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸"
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ "
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')"
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /"
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´"
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              ("
    )
    await pong.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  "
    )
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(
        f"**PONG!!🏓**\n"
        f"✣ **Pinger** - `%sms`\n"
        f"✣ **Uptime -** `{uptime}` \n"
        f"**✦҈͜͡Owner :** `{ALIVE_NAME}`" % (duration)
    )


@register(outgoing=True, pattern=r"^\.speedtest$")
async def speedtst(spd):
    """For .speedtest command, use SpeedTest to check server speeds."""
    await spd.edit("`Running speed test...`")

    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    msg = (
        f"**Started at {result['timestamp']}**\n\n"
        "**Client**\n"
        f"**ISP :** `{result['client']['isp']}`\n"
        f"**Country :** `{result['client']['country']}`\n\n"
        "**Server**\n"
        f"**Name :** `{result['server']['name']}`\n"
        f"**Country :** `{result['server']['country']}`\n"
        f"**Sponsor :** `{result['server']['sponsor']}`\n\n"
        f"**Ping :** `{result['ping']}`\n"
        f"**Upload :** `{humanbytes(result['upload'])}/s`\n"
        f"**Download :** `{humanbytes(result['download'])}/s`"
    )

    await spd.delete()
    await spd.client.send_file(
        spd.chat_id,
        result["share"],
        caption=msg,
        force_document=False,
    )


@register(outgoing=True, pattern=r"^\.pong$")
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    start = datetime.now()
    await pong.edit("`Sepong.....🏓`")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit("🏓 **Ping!**\n`%sms`" % (duration))


@register(outgoing=True, pattern=r"^\.usange(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(1)
    await typew.edit("`Getting Information...`")
    sleep(1)
    await typew.edit(
        "**Informasi Dyno Usage ★**:\n\n╭━━━━━━━━━━━━━━━━━━━━╮\n"
        f"-> `Penggunaan Dyno` **{ALIVE_NAME}**:\n"
        f" ❉ **10 Jam - "
        f"51 Menit - 0%**"
        "\n ◐━─━─━─━─━──━─━─━─━─━◐\n"
        "-> `Sisa Dyno Bulan Ini`:\n"
        f" ❉ **9989 Jam - 9948 Menit "
        f"- 99%**\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )


# @mixiologist


CMD_HELP.update(
    {
        "ping": "**Plugin : **`ping`\
        \n\n  •  **Syntax :** `.ping` ; `.lping` ; `.xping` ; `.kping` ; `.fping`\
        \n  •  **Function : **Untuk menunjukkan ping userbot.\
        \n\n  •  **Syntax :** `.pong`\
        \n  •  **Function : **Sama seperti perintah ping\
    "
    }
)


CMD_HELP.update(
    {
        "speedtest": "**Plugin : **`speedtest`\
        \n\n  •  **Syntax :** `.speedtest`\
        \n  •  **Function : **Untuk Mengetes kecepatan server userbot.\
    "
    }
)
