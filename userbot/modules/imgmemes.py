"""  Some Modules Imported by @Nitesh_231 :) & Again @heyworld roks *_* """
import asyncio
import os
import re

import requests
from html_telegraph_poster.upload_images import upload_image
from PIL import Image, ImageDraw, ImageFont
from telegraph import exceptions, upload_file
from validators.url import url
from wget import download

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    os.remove(image)
    return "temp.jpg"


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


async def threats(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phss(uplded, input, name):
    web = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={uplded}&text={input}&username={name}"
    ).json()
    alf = web.get("message")
    uri = url(alf)
    if not uri:
        return "check syntax once more"
    with open("alf.png", "wb") as f:
        f.write(requests.get(alf).content)
    img = Image.open("alf.png").convert("RGB")
    img.save("alf.jpg", "jpeg")
    return "alf.jpg"


async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.jpg", "jpeg")
    return "gpx.jpg"


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.jpg", "jpeg")
    return "gpx.jpg"


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def moditweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi"
    ).json()
    sandy = r.get("message")
    caturl = url(sandy)
    if not caturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(sandy).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def tweets(text1, text2):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.jpg", "jpeg")
    return "gpx.jpg"


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    return user_obj


async def purge():
    try:
        os.system("rm *.png *.webp")
    except OSError:
        pass


@register(outgoing=True, pattern=r"^\.trump(?: |$)(.*)")
async def trump(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`Send you text to trump so he can tweet.`")
            return
    await event.edit("`Requesting trump to tweet...`")
    text = deEmojify(text)
    img = await trumptweet(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(pattern="^.modi(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("Send you text to modi so he can tweet.")
            return
    await event.edit("Requesting modi to tweet...")
    text = deEmojify(text)
    file = await moditweet(text)
    await event.client.send_file(event.chat_id, file, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"^\.cmm(?: |$)(.*)")
async def cmm(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`Give text for to write on banner!`")
            return
    await event.edit("`Your banner is under creation wait a sec...`")
    text = deEmojify(text)
    img = await changemymind(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"^\.kanna(?: |$)(.*)")
async def kanna(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`What should kanna write give text!`")
            return
    await event.edit("`Kanna is writing your text...`")
    text = deEmojify(text)
    img = await kannagen(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"\.tweet(?: |$)(.*)")
async def tweet(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await event.edit("`What should i tweet? Give your username and tweet!`")
                return
        else:
            await event.edit("What should i tweet? Give your username and tweet!`")
            return
    if "." in text:
        username, text = text.split(".")
    else:
        await event.edit("`What should i tweet? Give your username and tweet!`")
    await event.edit(f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    img = await tweets(text, username)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(pattern="^.threat(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await threats(file)
    await event.delete()
    await bot.send_file(event.chat_id, file, reply_to=replied)


@register(pattern="^.trash(?: |$)(.*)", outgoing=True)
async def nekobot(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await trash(file)
    await event.delete()
    await bot.send_file(event.chat_id, file, reply_to=replied)


@register(pattern="^.trap(?: |$)(.*)", outgoing=True)
async def nekobot(e):
    input_str = e.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "|" in input_str:
        text1, text2 = input_str.split("|")
    else:
        await e.edit(
            "Balas Ke Gambar Atau Sticker Lalu Ketik `.trap (Nama Orang Yang Di Trap)|(Nama Trap)`"
        )
        return
    replied = await e.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await e.edit("reply to a supported media file")
        return
    if replied.media:
        await e.edit("passing to telegraph...")
    else:
        await e.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await e.edit("the replied file size is not supported it must me below 5 mb")
            os.remove(download_location)
            return
        await e.edit("generating image..")
    else:
        await e.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await e.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    file = f"https://telegra.ph{response[0]}"
    file = await trap(text1, text2, file)
    await e.delete()
    await bot.send_file(e.chat_id, file, reply_to=replied)


# Ported by @AshSTR


@register(outgoing=True, pattern="^.fgs ((.*) ; (.*))")
async def FakeGoogleSearch(event):
    """ Get a user-customised google search meme! """
    input_str = event.pattern_match.group(1)
    if input_str is None:
        await event.edit("No input found!", del_in=5)
        return
    if ";" in input_str:
        search, result = input_str.split(";", 1)
    else:
        await event.edit("Invalid Input! Check help for more info!", del_in=5)
        return

    await event.edit("Connecting to `https://www.google.com/` ...")
    await asyncio.sleep(2)
    img = "https://i.imgur.com/wNFr5X2.jpg"
    r = download(img)
    photo = Image.open(r)
    drawing = ImageDraw.Draw(photo)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font1 = ImageFont.truetype("userbot/utils/styles/ProductSans-BoldItalic.ttf", 20)
    font2 = ImageFont.truetype("userbot/utils/styles/ProductSans-Light.ttf", 23)
    drawing.text((450, 258), result, fill=blue, font=font1)
    drawing.text((270, 37), search, fill=black, font=font2)
    photo.save("downloads/test.jpg")
    reply = event.pattern_match.group(2)
    await event.delete()
    reply_id = event.pattern_match.group(3) if reply else None
    await event.client.send_file(
        event.chat_id, "downloads/test.jpg", reply_to_message_id=reply_id
    )
    os.remove("downloads/test.jpg")


@register(outgoing=True, pattern=r"^\.ph(?: |$)(.*)")
async def phcomment(event):
    try:
        await event.edit("`Processing..`")
        text = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        if reply:
            user = await get_user_from_event(event)
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            text = text if text else str(reply.message)
        elif text:
            user = await bot.get_me()
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            text = text
        else:
            return await event.edit("`Give text..`")
        try:
            photo = await event.client.download_profile_photo(
                user.id,
                str(user.id) + ".png",
                download_big=False,
            )
            uplded = upload_image(photo)
        except BaseException:
            uplded = "https://telegra.ph/file/7d110cd944d54f72bcc84.jpg"
    except BaseException as e:
        await purge()
        return await event.edit(f"`Error: {e}`")
    img = await phss(uplded, text, name)
    try:
        await event.client.send_file(
            event.chat_id,
            img,
            reply_to=event.reply_to_msg_id,
        )
    except BaseException:
        await purge()
        return await event.edit("`Reply message has no text!`")
    await event.delete()
    await purge()


CMD_HELP.update(
    {
        "imgmeme": "**Plugin : **`imgmeme`\
        \n\n  •  **Syntax :** `.fgs`\
        \n  •  **Function : **Meme dari search google yang di bisa custom user!\
        \n  •  **Example  : **`.fgs [Teks Atas] ; [Teks Bawah]`\
        \n\n  •  **Syntax :** `.trump`\
        \n  •  **Function : **Membuat Tweet dari akun twitter Donald Trump\
        \n\n  •  **Syntax :** `.modi` <text>\
        \n  •  **Function : **Membuat Tweet dari akun twitter @narendramodi\
        \n\n  •  **Syntax :** `.cmm` <text>\
        \n  •  **Function : **Membuat meme change my mind\
        \n\n  •  **Syntax :** `.kanna` <text>\
        \n  •  **Function : **Membuat meme tulisan dari nana anime bawa kertas\
        \n\n  •  **Syntax :** `.ph` <text>\
        \n  •  **Function : **Membuat Tweet dari website pornhub\
        \n\n  •  **Syntax :** `.threat` <text> (sambil reply media foto/sticker)\
        \n  •  **Function : **Membuat meme 3 hoax terbesar\
        \n\n  •  **Syntax :** `.trash` <text> (sambil reply media foto/sticker)\
        \n  •  **Function : **Membuat meme list sampah\
        \n\n  •  **Syntax :** `.trap` <text> (sambil reply media foto/sticker)\
        \n  •  **Function : **Membuat meme trapcard\
        \n\n  •  **Syntax :** `.tweet`\
        \n  •  **Function : **Membuat Tweet dari akun twitter\
        \n  •  **Example  : **.tweet @mrismanaziz.ganteng (harus pake . [titik])\
    "
    }
)
