# imported from github.com/ravana69/PornHub to userbot by @heyworld
# please don't nuke my credits 😓
import asyncio
import logging
import os
import time
from datetime import datetime
from urllib.parse import quote

import bs4
import requests
from justwatch import JustWatch
from telethon import *
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, SUDO_USERS, TEMP_DOWNLOAD_DIRECTORY
from userbot.utils import edit_delete, edit_or_reply, man_cmd

normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


logger = logging.getLogger(__name__)
thumb_image_path = TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
name = "Profile Photos"


@man_cmd(pattern="app(?: |$)(.*)")
async def apk(e):
    xx = await edit_or_reply(e, "`Processing...`")
    try:
        app_name = e.pattern_match.group(1)
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += "<b>" + app_name + "</b>"
        app_details += (
            "\n\n<b>Developer :</b> <a href='" + app_dev_link + "'>" + app_dev + "</a>"
        )
        app_details += "\n<b>Rating :</b> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<b>Features :</b> <a href='" + app_link + "'>View in Play Store</a>"
        )
        app_details += "\n\n===> Support @Lunatic0de <==="
        await xx.edit(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await edit_delete(
            xx, "**Pencarian tidak ditemukan. Mohon masukkan** `Nama app yang valid`"
        )
    except Exception as err:
        await edit_delete(xx, "Exception Occured:- " + str(err))


@man_cmd(pattern="calc(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1)  # get input
    exp = "Given expression is " + input  # report back input
    xx = await edit_or_reply(event, "`Processing...`")
    # lazy workaround to add support for two digits
    final_input = tuple(input)
    term1part1 = final_input[0]
    term1part2 = final_input[1]
    term1 = str(term1part1) + str(term1part2)
    final_term1 = int(term1)
    operator = str(final_input[2])
    term2part1 = final_input[3]
    term2part2 = final_input[4]
    term2 = str(term2part1) + str(term2part2)
    final_term2 = int(term2)
    # actual calculations go here
    if input == "help":
        await xx.edit(
            "Syntax .calc <term1><operator><term2>\nFor eg .calc 02*02 or 99*99 (the zeros are important) (two terms and two digits max)"
        )
    elif operator == "*":
        await xx.edit("Solution -->\n" + exp + "\n" + str(final_term1 * final_term2))
    elif operator == "-":
        await xx.edit("Solution -->\n" + exp + "\n" + str(final_term1 - final_term2))
    elif operator == "+":
        await xx.edit("Solution -->\n" + exp + "\n" + str(final_term1 + final_term2))
    elif operator == "/":
        await xx.edit("Solution -->\n" + exp + "\n" + str(final_term1 / final_term2))
    elif operator == "%":
        await xx.edit("Solution -->\n" + exp + "\n" + str(final_term1 % final_term2))
    else:
        await xx.edit("**Ketik** `.help calc` **bila butuh bantuan**")


@man_cmd(pattern="xcd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    xx = await edit_or_reply(event, "`Processing...`")
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url, params={"action": "xkcd", "query": quote(input_str)}
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if r.ok:
        data = r.json()
        year = data.get("year")
        month = data["month"].zfill(2)
        day = data["day"].zfill(2)
        xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
        safe_title = data.get("safe_title")
        data.get("transcript")
        alt = data.get("alt")
        img = data.get("img")
        data.get("title")
        output_str = """[\u2060]({})**{}**
[XKCD ]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(
            img, input_str, xkcd_link, safe_title, alt, day, month, year
        )
        await xx.edit(output_str, link_preview=True)
    else:
        await edit_delete(xx, "xkcd n.{} not found!".format(xkcd_id))


@man_cmd(pattern="remove(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    if event.sender_id in SUDO_USERS:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await edit_delete(event, "`Anda Bukan Admin Disini!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    xx = await edit_or_reply(event, "`Mencari Daftar Peserta....`")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                    break
                c += 1
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                    break
                c += 1
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                    break
                c += 1
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                    break
                c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await event.edit(
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**"
                    )
                    e.append(str(e))
                    break
                c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                    break
                c += 1
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                    break
                c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await edit_delete(
                        xx,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                    )
                    e.append(str(e))
                else:
                    c += 1
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await xx.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await event.edit(
        """Total= {} users
Number Of Deleted Accounts= {}
Status: Empty= {}
      : Last Month= {}
      : Last Week= {}
      : Offline= {}
      : Online= {}
      : Recently= {}
Number Of Bots= {}
Unidentified= {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


async def ban_user(chat_id, i, rights):
    try:
        await client(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@man_cmd(pattern="rnupload(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    xx = await edit_or_reply(event, "`Rename & Upload in processing ....`")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        end = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        to_download_directory = TEMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message,
            downloaded_file_name,
        )
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            time.time()
            await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await xx.edit(
                "**Downloaded in** `{}` **seconds. Uploaded in** `{}` **seconds**".format(
                    ms_one, ms_two
                )
            )
        else:
            await edit_delete(xx, "File Not Found {}".format(input_str))
    else:
        await edit_delete(xx, "Syntax // .rnupload filename.extension <reply ke media>")


@man_cmd(pattern="grab(?: |$)(.*)")
async def potocmd(event):
    id = "".join(event.raw_text.split(maxsplit=2)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    xx = await edit_or_reply(event, "`Processing...`")
    if user:
        photos = await event.client.get_profile_photos(user.sender)
    else:
        photos = await event.client.get_profile_photos(chat)
    if id.strip() == "":
        try:
            await event.client.send_file(event.chat_id, photos)
        except a:
            photo = await event.client.download_profile_photo(chat)
            await event.client.send_file(event.chat_id, photo)
    else:
        try:
            id = int(id)
            if id <= 0:
                return await edit_delete(
                    xx, "**Nomer ID Yang Anda Masukkan Tidak Valid**"
                )
        except BaseException:
            return await edit_delete(xx, "**Lmao**")
        if int(id) <= (len(photos)):
            send_photos = await event.client.download_media(photos[id - 1])
            await event.client.send_file(event.chat_id, send_photos)
            await xx.delete()
        else:
            return await edit_delete(xx, "**Tidak Dapat Menemukan Foto Pengguna Ini**")


@man_cmd(pattern="res(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        return await edit_delete(event, "**Mohon Balas Ke Link.**")
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        return await edit_delete(event, "**Mohon Balas Ke Link.**")
    chat = "@CheckRestrictionsBot"
    xx = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=894227130)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await event.client.forward_messages(chat, reply_message)
            response = await response
        if response.text.startswith(""):
            await event.edit("**Terjadi Error**")
        else:
            await xx.delete()
            await event.client.send_message(event.chat_id, response.message)
            await event.client.delete_message(chat, event.chat_id, response.message)


def get_stream_data(query):
    stream_data = {}

    # Compatibility for Current Userge Users
    try:
        country = Config.WATCH_COUNTRY
    except Exception:
        country = "IN"

    # Cooking Data
    just_watch = JustWatch(country=country)
    results = just_watch.search_for_item(query=query)
    movie = results["items"][0]
    stream_data["title"] = movie["title"]
    stream_data["movie_thumb"] = (
        "https://images.justwatch.com"
        + movie["poster"].replace("{profile}", "")
        + "s592"
    )
    stream_data["release_year"] = movie["original_release_year"]
    try:
        print(movie["cinema_release_date"])
        stream_data["release_date"] = movie["cinema_release_date"]
    except KeyError:
        try:
            stream_data["release_date"] = movie["localized_release_date"]
        except KeyError:
            stream_data["release_date"] = None

    stream_data["type"] = movie["object_type"]

    available_streams = {}
    for provider in movie["offers"]:
        provider_ = get_provider(provider["urls"]["standard_web"])
        available_streams[provider_] = provider["urls"]["standard_web"]

    stream_data["providers"] = available_streams

    scoring = {}
    for scorer in movie["scoring"]:
        if scorer["provider_type"] == "tmdb:score":
            scoring["tmdb"] = scorer["value"]

        if scorer["provider_type"] == "imdb:score":
            scoring["imdb"] = scorer["value"]
    stream_data["score"] = scoring
    return stream_data


# Helper Functions


def pretty(name):
    if name == "play":
        name = "Google Play Movies"
    return name[0].upper() + name[1:]


def get_provider(url):
    url = url.replace("https://www.", "")
    url = url.replace("https://", "")
    url = url.replace("http://www.", "")
    url = url.replace("http://", "")
    url = url.split(".")[0]
    return url


@man_cmd(pattern="watch(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    xx = await edit_or_reply(event, "`Processing...`")
    streams = get_stream_data(query)
    title = streams["title"]
    thumb_link = streams["movie_thumb"]
    release_year = streams["release_year"]
    release_date = streams["release_date"]
    scores = streams["score"]
    try:
        imdb_score = scores["imdb"]
    except KeyError:
        imdb_score = None
    try:
        tmdb_score = scores["tmdb"]
    except KeyError:
        tmdb_score = None
    stream_providers = streams["providers"]
    if release_date is None:
        release_date = release_year
    output_ = f"**Movie:**\n`{title}`\n**Release Date:**\n`{release_date}`"
    if imdb_score:
        output_ = output_ + f"\n**IMDB: **{imdb_score}"
    if tmdb_score:
        output_ = output_ + f"\n**TMDB: **{tmdb_score}"
    output_ = output_ + "\n\n**Available on:**\n"
    for provider, link in stream_providers.items():
        if "sonyliv" in link:
            link = link.replace(" ", "%20")
        output_ += f"[{pretty(provider)}]({link})\n"
    await event.client.send_file(
        event.chat_id,
        caption=output_,
        file=thumb_link,
        force_document=False,
        allow_cache=False,
        silent=True,
    )
    await xx.delete()


# credits:
# Ported from Saitama Bot.
# By :- @PhycoNinja13b
# Modified by :- @kirito6969,@deleteduser420


@man_cmd(pattern="weeb(?: |$)(.*)")
async def weebify(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("**Teks Apa Yang Harus Saya Weebify Kan?**")
        return
    string = " ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await event.edit(string)


boldfont = [
    "𝗮",
    "𝗯",
    "𝗰",
    "𝗱",
    "𝗲",
    "𝗳",
    "𝗴",
    "𝗵",
    "𝗶",
    "𝗷",
    "𝗸",
    "𝗹",
    "𝗺",
    "𝗻",
    "𝗼",
    "𝗽",
    "𝗾",
    "𝗿",
    "𝘀",
    "𝘁",
    "𝘂",
    "𝘃",
    "𝘄",
    "𝘅",
    "𝘆",
    "𝘇",
]


@man_cmd(pattern="bold(?: |$)(.*)")
async def thicc(bolded):
    args = bolded.pattern_match.group(1)
    if not args:
        get = await bolded.get_reply_message()
        args = get.text
    if not args:
        return await edit_delete(bolded, "**Teks Apa Yang Harus Saya Bold Kan?**")
    xx = await edit_or_reply(bolded, "`Processing...`")
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            boldcharacter = boldfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, boldcharacter)
    await xx.edit(string)


medievalbold = [
    "𝖆",
    "𝖇",
    "𝖈",
    "𝖉",
    "𝖊",
    "𝖋",
    "𝖌",
    "𝖍",
    "𝖎",
    "𝖏",
    "𝖐",
    "𝖑",
    "𝖒",
    "𝖓",
    "𝖔",
    "𝖕",
    "𝖖",
    "𝖗",
    "𝖘",
    "𝖙",
    "𝖚",
    "𝖛",
    "𝖜",
    "𝖝",
    "𝖞",
    "𝖟",
]


@man_cmd(pattern="medibold(?: |$)(.*)")
async def mediv(medievalx):
    args = medievalx.pattern_match.group(1)
    if not args:
        get = await medievalx.get_reply_message()
        args = get.text
    if not args:
        return await edit_delete(
            medievalx, "**Teks Apa Yang Harus Saya Medibold Kan?**"
        )
    xx = await edit_or_reply(medievalx, "`Processing...`")
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            medievalcharacter = medievalbold[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, medievalcharacter)
    await xx.edit(string)


doublestruckt = [
    "𝕒",
    "𝕓",
    "𝕔",
    "𝕕",
    "𝕖",
    "𝕗",
    "𝕘",
    "𝕙",
    "𝕚",
    "𝕛",
    "𝕜",
    "𝕝",
    "𝕞",
    "𝕟",
    "𝕠",
    "𝕡",
    "𝕢",
    "𝕣",
    "𝕤",
    "𝕥",
    "𝕦",
    "𝕧",
    "𝕨",
    "𝕩",
    "𝕪",
    "𝕫",
]


@man_cmd(pattern="doublestruck(?: |$)(.*)")
async def doublex(doublestrucktx):
    args = doublestrucktx.pattern_match.group(1)
    if not args:
        get = await doublestrucktx.get_reply_message()
        args = get.text
    if not args:
        return await edit_delete(
            doublestrucktx, "**Teks Apa Yang Harus Saya Double Struck Kan?**"
        )
    xx = await edit_or_reply(doublestrucktx, "`Processing...`")
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            strucktcharacter = doublestruckt[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, strucktcharacter)
    await xx.edit(string)


cursiveboldx = [
    "𝓪",
    "𝓫",
    "𝓬",
    "𝓭",
    "𝓮",
    "𝓯",
    "𝓰",
    "𝓱",
    "𝓲",
    "𝓳",
    "𝓴",
    "𝓵",
    "𝓶",
    "𝓷",
    "𝓸",
    "𝓹",
    "𝓺",
    "𝓻",
    "𝓼",
    "𝓽",
    "𝓾",
    "𝓿",
    "𝔀",
    "𝔁",
    "𝔂",
    "𝔃",
]


@man_cmd(pattern="curbold(?: |$)(.*)")
async def cursive2(cursivebolded):
    args = cursivebolded.pattern_match.group(1)
    if not args:
        get = await cursivebolded.get_reply_message()
        args = get.text
    if not args:
        await edit_delete.edit(
            cursivebolded, "**Teks Apa Yang Harus Saya Cursive Bold Kan?**"
        )
        return
    xx = await edit_or_reply(cursivebolded, "`Processing...`")
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            cursiveboldcharacter = cursiveboldx[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, cursiveboldcharacter)
    await xx.edit(string)


medival2 = [
    "𝔞",
    "𝔟",
    "𝔠",
    "𝔡",
    "𝔢",
    "𝔣",
    "𝔤",
    "𝔥",
    "𝔦",
    "𝔧",
    "𝔨",
    "𝔩",
    "𝔪",
    "𝔫",
    "𝔬",
    "𝔭",
    "𝔮",
    "𝔯",
    "𝔰",
    "𝔱",
    "𝔲",
    "𝔳",
    "𝔴",
    "𝔵",
    "𝔶",
    "𝔷",
]


@man_cmd(pattern="medi(?: |$)(.*)")
async def medival22(medivallite):
    args = medivallite.pattern_match.group(1)
    if not args:
        get = await medivallite.get_reply_message()
        args = get.text
    if not args:
        await edit_delete(medivallite, "****Teks Apa Yang Harus Saya Medival Kan?****")
        return
    xx = await edit_or_reply(medivallite, "`Processing...`")
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            medivalxxcharacter = medival2[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, medivalxxcharacter)
    await xx.edit(string)


cursive = [
    "𝒶",
    "𝒷",
    "𝒸",
    "𝒹",
    "𝑒",
    "𝒻",
    "𝑔",
    "𝒽",
    "𝒾",
    "𝒿",
    "𝓀",
    "𝓁",
    "𝓂",
    "𝓃",
    "𝑜",
    "𝓅",
    "𝓆",
    "𝓇",
    "𝓈",
    "𝓉",
    "𝓊",
    "𝓋",
    "𝓌",
    "𝓍",
    "𝓎",
    "𝓏",
]


@man_cmd(pattern="cur(?: |$)(.*)")
async def xcursive(cursivelite):
    args = cursivelite.pattern_match.group(1)
    if not args:
        get = await cursivelite.get_reply_message()
        args = get.text
    if not args:
        await edit_delete.edit(cursivelite, "**Teks Apa Yang Harus Saya Cursive Kan?**")
        return
    xx = await edit_or_reply(cursivelite, "`Processing...`")
    string = "".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            cursivecharacter = cursive[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, cursivecharacter)
    await xx.edit(string)


CMD_HELP.update(
    {
        "watch": f"**Plugin : **`watch`\
        \n\n  •  **Syntax :** `{cmd}watch` <nama movie/tv>\
        \n  •  **Function : **Untuk Mengetahui Detail Tentang Film.\
    "
    }
)

CMD_HELP.update(
    {
        "randompp": f"**Plugin : **`randompp`\
        \n\n  •  **Syntax :** `{cmd}randompp`\
        \n  •  **Function : **Otomatis Mengganti Foto Profile Mu, Untuk Stop ini Ketik .restart\
    "
    }
)

CMD_HELP.update(
    {
        "glitch": f"**Plugin : **`glitch`\
        \n\n  •  **Syntax :** `{cmd}glitch` <Reply Ke Media>\
        \n  •  **Function : **Memberikan Glitch (Gif , Stickers , Gambar, Video) Ke Gif Dan Level Glitch 1 - 8.\nJika Tidak Memberikan Level Otomatis Default Ke Level 2\
    "
    }
)

CMD_HELP.update(
    {
        "grab": f"**Plugin : **`grab`\
        \n\n  •  **Syntax :** `{cmd}grab` <reply ke user yang ingin di grab>\
        \n  •  **Function : **Balas Ke Pesan Pengguna Telegram dan Ketik `{cmd}grab` Atau `{cmd}grab <count>` Untuk Mengambil Foto Profil.\
        \n\n  •  **Syntax :** `{cmd}grab` <jumlah foto>\
        \n  •  **Function : **Untuk Mengambil Foto Profil dengan jumlah foto yg di inginkan.\
    "
    }
)

CMD_HELP.update(
    {
        "bannedall": f"**Plugin : **`bannedall`.\
        \n\n  •  **Syntax :** `{cmd}remove`\
        \n  •  **Function : **Untuk Menganalisa user dari grup secara spesifik\
        \n\n  •  **Syntax :** `{cmd}remove d`\
        \n  •  **Function : **Untuk mengkik user dari grup secara spesifik\
        \n\n  •  **Syntax :** `{cmd}remove y`\
        \n  •  **Function : **Untuk Membanned Akun yang Terakhir Dilihat setahun yang lalu\
        \n\n  •  **Syntax :** `{cmd}remove m`\
        \n  •  **Function : **Untuk Membanned Akun yang Terakhir Dilihat sebulan yang lalu\
        \n\n  •  **Syntax :** `{cmd}remove w`\
        \n  •  **Function : **Untuk Membanned Akun yang Terakhir Dilihat seminggu yang lalu\
        \n\n  •  **Syntax :** `{cmd}remove o`\
        \n  •  **Function : **Untuk Membanned Akun yang sedang offline\
        \n\n  •  **Syntax :** `{cmd}remove q`\
        \n  •  **Function : **Untuk Membanned Akun yang sedang online\
        \n\n  •  **Syntax :** `{cmd}remove r`\
        \n  •  **Function : **Untuk Membanned Akun yang terakhir dilihat\
        \n\n  •  **Syntax :** `{cmd}remove b`\
        \n  •  **Function : **Untuk Membanned Bot yang ada di Grup chat\
        \n\n  •  **Syntax :** `{cmd}remove n`\
        \n  •  **Function : **Untuk Membanned Akun yang Last Seen A Long Time Ago\
        \n\n **HATI HATI PLUGIN INI BERBAHAYA, MOHON GUNAKAN DENGAN BIJAK**\
    "
    }
)

CMD_HELP.update(
    {
        "rnupload": f"**Plugin : **`rnupload`\
        \n\n  •  **Syntax :** `{cmd}rnupload`\
        \n  •  **Function : **Untuk Rename dan Upload, Balas Ke Media Dan Ketik .rnupload xyz.jpg\
    "
    }
)


CMD_HELP.update(
    {
        "appmisc": f"`{cmd}app`\
\nUsage: ketik `{cmd}app namaapp` Dan Dapatkan Detail Informasi App.\
\n\n`.calc`\
\nUsage: `{cmd}calc <term1><operator><term2>\nUntuk eg {cmd}calc 02*02 Atau 99*99 (Angka Nol Penting) (Minimal Dua Suku Dan Dua Digit).\
\n\n`{cmd}xcd`\
\nUsage: Ketik xcd <query>.ps:Aku Sangat Bosan\
\n\n`{cmd}res`\
\nUsage: Ketik Username Akun,Channel,Group Atau Bot Bersama {cmd}res Dan Check Batasan\
\n\n`{cmd}weeb` <text>\
\nUsage:Teks Weebify\
\n\nKetik (`{cmd}bold <Teks>`,`{cmd}cur <Teks>`,`{cmd}curbold <Teks>`,`{cmd}medi <Teks>`,`{cmd}medibold <Teks>`,`{cmd}doublestruck <Teks>`)\
\nUsage: Buat Teks <Bold,Cursive,Cursivebold,Medival,Medivalbold,Gayishbold>\
\n\n`{cmd}glitchs` Balas Ke Media\
\nUsage: Memberikan Glitch (Gif , Stickers , Gambar, Video) Ke Sticker Dan Level Glitch 1 to 8.\
Jika Tidak Memberikan Level Otomatis Default Ke Level 2."
    }
)
