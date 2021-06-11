# Copyright (C) UsergeTeam 2020
# Licensed under GPLv3
# Ported from Userge and refactored by @KenHV
# FROM Man-Userbot
# t.me/SharingUserbot

import asyncio
import os
import shlex
import textwrap
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


@register(outgoing=True, pattern=r"^\.mmf (.*)")
async def memify(event):
    reply_msg = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    await event.edit("**Sedang Memperoses...**")

    if not reply_msg:
        return await event.edit("**Balas ke pesan yang berisi media!**")

    if not reply_msg.media:
        return await event.edit("**Balas ke image/sticker/gif/video!**")

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    input_file = await event.client.download_media(reply_msg, TEMP_DOWNLOAD_DIRECTORY)
    input_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, os.path.basename(input_file))

    if input_file.endswith(".tgs"):
        await event.edit("**Mengekstrak Frame pertama...**")
        converted_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "meme.webp")
        cmd = f"lottie_convert.py --frame 0 {input_file} {converted_file}"
        await runcmd(cmd)
        os.remove(input_file)
        if not os.path.lexists(converted_file):
            return await event.edit("**Tidak dapat menguraikan stiker animasi ini.**")
        input_file = converted_file

    elif input_file.endswith(".mp4"):
        await event.edit("**Mengekstrak Frame pertama...**")
        converted_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "meme.png")
        await take_screen_shot(input_file, 0, converted_file)
        os.remove(input_file)
        if not os.path.lexists(converted_file):
            return await event.edit("**Tidak Dapat Mengurai Video ini.**")
        input_file = converted_file

    await event.edit("**Menambahkan Teks...**")
    try:
        final_image = await add_text_img(input_file, input_str)
    except Exception as e:
        return await event.edit(f"**Terjadi kesalahan:**\n`{e}`")
    await event.client.send_file(
        entity=event.chat_id, file=final_image, reply_to=reply_msg
    )
    await event.delete()
    os.remove(final_image)
    os.remove(input_file)


async def add_text_img(image_path, text):
    font_size = 12
    stroke_width = 1

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="userbot/utils/styles/FontLord.ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "memify.webp")
    img.save(final_image, **img_info)
    return final_image


async def runcmd(cmd: str) -> tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """take a screenshot"""
    ttl = duration // 2
    thumb_image_path = path or os.path.join(
        TEMP_DOWNLOAD_DIRECTORY, f"{os.path.basename(video_file)}.png"
    )
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    err = (await runcmd(command))[1]
    return thumb_image_path if os.path.exists(thumb_image_path) else err


CMD_HELP.update(
    {
        "memify": "**Plugin : **`memify`\
        \n\n  •  **Syntax :** `.mmf` Teks Atas ; Teks Bawah\
        \n  •  **Function :** Balas Ke Sticker/Gambar/Gif, Gambar akan Di ubah jadi teks meme yang di tentukan\
        \n\n  •  **NOTE :** Jika itu video, teks akan diedit di frame pertama.\
    "
    }
)
