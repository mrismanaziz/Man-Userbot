# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/Lunatic0de & t.me/SharingUserbot

import os
import random

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, edit_or_reply, man_cmd
from userbot.utils.misc import Carbon

from .vcplugin import vcmention

all_col = [
    "Black",
    "Navy",
    "DarkBlue",
    "MediumBlue",
    "Blue",
    "DarkGreen",
    "Green",
    "Teal",
    "DarkCyan",
    "DeepSkyBlue",
    "DarkTurquoise",
    "MediumSpringGreen",
    "Lime",
    "SpringGreen",
    "Aqua",
    "Cyan",
    "MidnightBlue",
    "DodgerBlue",
    "LightSeaGreen",
    "ForestGreen",
    "SeaGreen",
    "DarkSlateGray",
    "DarkSlateGrey",
    "LimeGreen",
    "MediumSeaGreen",
    "Turquoise",
    "RoyalBlue",
    "SteelBlue",
    "DarkSlateBlue",
    "MediumTurquoise",
    "Indigo  ",
    "DarkOliveGreen",
    "CadetBlue",
    "CornflowerBlue",
    "RebeccaPurple",
    "MediumAquaMarine",
    "DimGray",
    "DimGrey",
    "SlateBlue",
    "OliveDrab",
    "SlateGray",
    "SlateGrey",
    "LightSlateGray",
    "LightSlateGrey",
    "MediumSlateBlue",
    "LawnGreen",
    "Chartreuse",
    "Aquamarine",
    "Maroon",
    "Purple",
    "Olive",
    "Gray",
    "Grey",
    "SkyBlue",
    "LightSkyBlue",
    "BlueViolet",
    "DarkRed",
    "DarkMagenta",
    "SaddleBrown",
    "DarkSeaGreen",
    "LightGreen",
    "MediumPurple",
    "DarkViolet",
    "PaleGreen",
    "DarkOrchid",
    "YellowGreen",
    "Sienna",
    "Brown",
    "DarkGray",
    "DarkGrey",
    "LightBlue",
    "GreenYellow",
    "PaleTurquoise",
    "LightSteelBlue",
    "PowderBlue",
    "FireBrick",
    "DarkGoldenRod",
    "MediumOrchid",
    "RosyBrown",
    "DarkKhaki",
    "Silver",
    "MediumVioletRed",
    "IndianRed ",
    "Peru",
    "Chocolate",
    "Tan",
    "LightGray",
    "LightGrey",
    "Thistle",
    "Orchid",
    "GoldenRod",
    "PaleVioletRed",
    "Crimson",
    "Gainsboro",
    "Plum",
    "BurlyWood",
    "LightCyan",
    "Lavender",
    "DarkSalmon",
    "Violet",
    "PaleGoldenRod",
    "LightCoral",
    "Khaki",
    "AliceBlue",
    "HoneyDew",
    "Azure",
    "SandyBrown",
    "Wheat",
    "Beige",
    "WhiteSmoke",
    "MintCream",
    "GhostWhite",
    "Salmon",
    "AntiqueWhite",
    "Linen",
    "LightGoldenRodYellow",
    "OldLace",
    "Red",
    "Fuchsia",
    "Magenta",
    "DeepPink",
    "OrangeRed",
    "Tomato",
    "HotPink",
    "Coral",
    "DarkOrange",
    "LightSalmon",
    "Orange",
    "LightPink",
    "Pink",
    "Gold",
    "PeachPuff",
    "NavajoWhite",
    "Moccasin",
    "Bisque",
    "MistyRose",
    "BlanchedAlmond",
    "PapayaWhip",
    "LavenderBlush",
    "SeaShell",
    "Cornsilk",
    "LemonChiffon",
    "FloralWhite",
    "Snow",
    "Yellow",
    "LightYellow",
    "Ivory",
    "White",
]


@man_cmd(pattern="(rc|c)arbon")
async def crbn(event):
    from_user = vcmention(event.sender)
    xxxx = await edit_or_reply(event, "`Processing...`")
    te = event.text
    col = random.choice(all_col) if te[1] == "r" else "Grey"
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            os.remove(b)
        else:
            code = temp.message
    else:
        try:
            code = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await edit_delete(
                xxxx, "**Balas ke pesan atau file yang dapat dibaca**", 30
            )
    xx = await Carbon(code=code, file_name="carbon_man", backgroundColor=col)
    await xxxx.delete()
    await event.reply(
        f"**Carbonised by** {from_user}",
        file=xx,
    )


@man_cmd(pattern="ccarbon ?(.*)")
async def crbn(event):
    from_user = vcmention(event.sender)
    match = event.pattern_match.group(1).strip()
    if not match:
        return await edit_or_reply(
            event, "**Berikan Warna Custom untuk Membuat Carbon**"
        )
    msg = await edit_or_reply(event, "`Processing...`")
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            os.remove(b)
        else:
            code = temp.message
    else:
        try:
            match = match.split(" ", maxsplit=1)
            code = match[1]
            match = match[0]
        except IndexError:
            return await edit_delete(
                msg, "**Balas pesan atau file yang dapat dibaca**", 30
            )
    xx = await Carbon(code=code, backgroundColor=match)
    await msg.delete()
    await event.reply(
        f"**Carbonised by** {from_user}",
        file=xx,
    )


CMD_HELP.update(
    {
        "carbon": f"**Plugin : **`carbon`\
        \n\n  •  **Syntax :** `{cmd}carbon` <text/reply>\
        \n  •  **Function : **Carbonisasi teks dengan pengaturan default.\
        \n\n  •  **Syntax :** `{cmd}rcarbon` <text/reply>\
        \n  •  **Function : **Carbonisasi teks, dengan warna background acak.\
        \n\n  •  **Syntax :** `{cmd}ccarbon` <warna> <text/reply>\
        \n  •  **Function : **Carbonisasi teks, dengan warna background custom.\
    "
    }
)
