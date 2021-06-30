# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#

import asyncio
import io
import os

from PIL import Image

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.convert ?(foto|sound|gif|voice|photo|mp3)? ?(.*)")
async def cevir(event):
    botman = event.pattern_match.group(1)
    try:
        if len(botman) < 1:
            await event.edit(
                "**Perintah tidak diketahui! ketik** `.help convert` **bila butuh bantuan**"
            )
            return
    except BaseException:
        await event.edit(
            "**Perintah tidak diketahui! ketik** `.help convert` **bila butuh bantuan**"
        )
        return

    if botman in ["foto", "photo"]:
        rep_msg = await event.get_reply_message()

        if not event.is_reply or not rep_msg.sticker:
            await event.edit("**Harap balas ke stiker.**")
            return
        await event.edit("`Mengconvert ke foto...`")
        foto = io.BytesIO()
        foto = await event.client.download_media(rep_msg.sticker, foto)

        im = Image.open(foto).convert("RGB")
        im.save("sticker.png", "png")
        await event.client.send_file(
            event.chat_id,
            "sticker.png",
            reply_to=rep_msg,
        )

        await event.delete()
        os.remove("sticker.png")
    elif botman in ["sound", "voice"]:
        EFEKTLER = ["bengek", "robot", "jedug", "fast", "echo"]

        efekt = event.pattern_match.group(2)

        if len(efekt) < 1:
            await event.edit(
                "**Efek yang Anda tentukan tidak ditemukan!**\n**Efek yang dapat Anda gunakan:** bengek/robot/jedug/fast/echo`"
            )
            return

        rep_msg = await event.get_reply_message()

        if not event.is_reply or not (rep_msg.voice or rep_msg.audio):
            await event.edit("**Harap balas ke file Audio.**")
            return

        await event.edit("`Applying effect...`")
        if efekt in EFEKTLER:
            indir = await rep_msg.download_media()
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[efekt]} output.mp3"
            )
            await ses.communicate()
            await event.client.send_file(
                event.chat_id,
                "output.mp3",
                reply_to=rep_msg,
            )

            await event.delete()
            os.remove(indir)
            os.remove("output.mp3")
        else:
            await event.edit(
                "**Efek yang Anda tentukan tidak ditemukan!**\n**Efek yang dapat Anda gunakan:** bengek/robot/jedug/fast/echo`"
            )
    elif botman == "gif":
        rep_msg = await event.get_reply_message()

        if (
            not event.is_reply
            or not rep_msg.video
            and rep_msg.document.mime_type != "application/x-tgsticker"
        ):
            await event.edit("**Harap balas ke Video!**")
            return

        await event.edit("`Mengconvert ke gif...`")
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg)
        if rep_msg.document.mime_type == "application/x-tgsticker":
            print(f"lottie_convert.py '{video}' out.gif")
            gif = await asyncio.create_subprocess_shell(
                f"lottie_convert.py '{video}' out.gif"
            )
        else:
            gif = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{video}' -filter_complex 'fps=20,scale=320:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse' out.gif"
            )
        await gif.communicate()
        await event.edit("`Uploading Gif...`")

        try:
            await event.client.send_file(
                event.chat_id,
                "out.gif",
                reply_to=rep_msg,
            )
        except BaseException:
            await event.edit("**Saya tidak bisa mengubahnya menjadi gif 🥺**")
            await event.delete()
            os.remove("out.gif")
            os.remove(video)
        finally:
            await event.delete()
            os.remove("out.gif")
            os.remove(video)
    elif botman == "mp3":
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.video:
            await event.edit("**Harap balas ke Video!**")
            return
        await event.edit("`Mengconvert ke sound...`")
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(
            f"ffmpeg -y -i '{video}' -vn -b:a 128k -c:a libmp3lame out.mp3"
        )
        await gif.communicate()
        await event.edit("`Uploading Sound...`")

        try:
            await event.client.send_file(
                event.chat_id,
                "out.mp3",
                reply_to=rep_msg,
            )
        except BaseException:
            os.remove(video)
            return await event.edit("**Tidak dapat mengconvert ke audio! 🥺**")

        await event.delete()
        os.remove("out.mp3")
        os.remove(video)
    else:
        await event.edit(
            "**Perintah tidak diketahui! ketik** `.help convert` **bila butuh bantuan**"
        )
        return


CMD_HELP.update(
    {
        "convert": "**Plugin : **`core`\
        \n\n  •  **Syntax :** `.convert foto`\
        \n  •  **Function : **Untuk Mengconvert sticker ke foto\
        \n\n  •  **Syntax :** `.convert mp3`\
        \n  •  **Function : **Untuk Mengconvert dari video ke file mp3\
        \n\n  •  **Syntax :** `.convert gif`\
        \n  •  **Function : **Untuk Mengconvert video ke gif\
        \n\n  •  **Syntax :** `.convert audio`\
        \n  •  **Function : **Untuk Menambahkan efek suara jadi berskin\
        \n  •  **List Efek : `bengek`, `jedug`, `echo`, `robot`\
    "
    }
)
