# based on https://gist.github.com/wshanshan/c825efca4501a491447056849dd207d6
# Ported for ProjectAlf by Alfiananda P.A

import random

import numpy as np
from colour import Color
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import bash, edit_delete, edit_or_reply, man_cmd

bground = "black"


@man_cmd(pattern="(ascii|asciis)$")
async def _(event):
    if not event.reply_to_msg_id:
        return await edit_delete(event, "**Mohon Balas Ke Media..**")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await edit_delete(event, "`Balas Ke Gambar/Sticker/Video`")
    xx = await edit_or_reply(event, "`Sedang Mendownload Media..`")
    if reply_message.photo:
        IMG = await event.client.download_media(
            reply_message,
            "ascii.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await event.client.download_media(
            reply_message,
            "ASCII.tgs",
        )
        await bash("lottie_convert.py ASCII.tgs ascii.png")
        IMG = "ascii.png"
    elif reply_message.video:
        video = await event.client.download_media(
            reply_message,
            "ascii.mp4",
        )
        extractMetadata(createParser(video))
        await bash("ffmpeg -i ascii.mp4 -vframes 1 -an -s 480x360 -ss 1 ascii.png")
        IMG = "ascii.png"
    else:
        IMG = await event.client.download_media(
            reply_message,
            "ascii.png",
        )
    try:
        await xx.edit("`Sedang Dalam Proses..`")
        list = await random_color()
        color1 = list[0]
        color2 = list[1]
        bgcolor = bground
        await asciiart(IMG, color1, color2, bgcolor)
        cmd = event.pattern_match.group(1)
        if cmd == "asciis":
            await bash("cp ascii.png ascii.webp")
            ascii_file = "ascii.webp"
        else:
            ascii_file = "ascii.png"
        await event.client.send_file(
            event.chat_id,
            ascii_file,
            force_document=False,
            reply_to=event.reply_to_msg_id,
        )
        await event.delete()
        await bash("rm *.png *.webp *.mp4 *.tgs")
    except BaseException as e:
        await bash("rm *.png *.webp *.mp4 *.png")
        return await edit_or_reply(event, f"{e}")


async def asciiart(IMG, color1, color2, bgcolor):
    chars = np.asarray(list(" .,:irs?@9B&#"))
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    WCF = letter_height / letter_width
    img = Image.open(IMG)
    widthByLetter = round(img.size[0] * 0.15 * WCF)
    heightByLetter = round(img.size[1] * 0.15)
    S = (widthByLetter, heightByLetter)
    img = img.resize(S)
    img = np.sum(np.asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** 2.2 * (chars.size - 1)
    lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")
    nbins = len(lines)
    colorRange = list(Color(color1).range_to(Color(color2), nbins))
    newImg_width = letter_width * widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
    draw = ImageDraw.Draw(newImg)
    leftpadding = 0
    y = 0
    for lineIdx, line in enumerate(lines):
        color = colorRange[lineIdx]
        draw.text((leftpadding, y), line, color.hex, font=font)
        y += letter_height
    IMG = newImg.save("ascii.png")
    return IMG


# this is from userge
async def random_color():
    return [
        "#" + "".join(random.choice("0123456789ABCDEF") for k in range(6))
        for i in range(2)
    ]


@man_cmd(pattern="asciibg(?: |$)(.*)")
async def _(event):
    BG = event.pattern_match.group(1)
    if BG.isnumeric():
        return await edit_or_reply(event, "`Mohon Masukkan Warna Bukan Angka`")
    if not BG:
        return await edit_or_reply(event, "`Mohon Masukkan Background Dari Ascii`")
    global bground
    bground = BG
    await edit_or_reply(event, f"`Berhasil Setel Background Dari Ascii Ke` **{BG}**")


CMD_HELP.update(
    {
        "ascii": f"**Plugin : **`ascii`\
        \n\n  •  **Syntax :** `{cmd}ascii`\
        \n  •  **Function : **Buat Ascii Art Dari Media.\
        \n\n  •  **Syntax :** `{cmd}asciis`\
        \n  •  **Function : **Sama Tapi Unggah Hasilnya Sebagai Sticker.\
        \n\n  •  **Syntax :** `{cmd}asciibg` <color>\
        \n  •  **Function : **Untuk Mengubah Warna Background Dari Modul Ascii Contoh `.asciibg black`.\
    "
    }
)
