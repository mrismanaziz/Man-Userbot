# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import html
import json
import re
import textwrap
from io import BytesIO, StringIO

import aiohttp
import bs4
import jikanpy
import pendulum
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from telethon.errors.rpcerrorlist import FilePartsInvalidError
from telethon.tl.types import (
    DocumentAttributeAnimated,
    DocumentAttributeFilename,
    MessageMediaDocument,
)
from telethon.utils import is_image, is_video

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, edit_or_reply, man_cmd

jikan = Jikan()

# Anime Helper


def getPosterLink(mal):
    # grab poster from kitsu
    kitsu = getKitsu(mal)
    image = requests.get(f"https://kitsu.io/api/edge/anime/{kitsu}").json()
    return image["data"]["attributes"]["posterImage"]["original"]


def getKitsu(mal):
    # get kitsu id from mal id
    link = f"https://kitsu.io/api/edge/mappings?filter[external_site]=myanimelist/anime&filter[external_id]={mal}"
    result = requests.get(link).json()["data"][0]["id"]
    link = f"https://kitsu.io/api/edge/mappings/{result}/item?fields[anime]=slug"
    return requests.get(link).json()["data"]["id"]


def getBannerLink(mal, kitsu_search=True):
    # try getting kitsu backdrop
    if kitsu_search:
        kitsu = getKitsu(mal)
        image = f"http://media.kitsu.io/anime/cover_images/{kitsu}/original.jpg"
        response = requests.get(image)
        if response.status_code == 200:
            return image
    # try getting anilist banner
    query = """
    query ($idMal: Int){
        Media(idMal: $idMal){
            bannerImage
        }
    }
    """
    data = {"query": query, "variables": {"idMal": int(mal)}}
    image = requests.post("https://graphql.anilist.co", json=data).json()["data"][
        "Media"
    ]["bannerImage"]
    if image:
        return image
    return getPosterLink(mal)


def get_anime_manga(mal_id, search_type, _user_id):
    jikan = jikanpy.jikan.Jikan()
    if search_type == "anime_anime":
        result = jikan.anime(mal_id)
        trailer = result["trailer_url"]
        if trailer:
            LOL = f"<a href='{trailer}'>YouTube</a>"
        else:
            LOL = "<code>No Trailer Available</code>"
        image = getBannerLink(mal_id)
        studio_string = ", ".join(
            studio_info["name"] for studio_info in result["studios"]
        )
        producer_string = ", ".join(
            producer_info["name"] for producer_info in result["producers"]
        )
    elif search_type == "anime_manga":
        result = jikan.manga(mal_id)
        image = result["image_url"]
    caption = f"<a href='{result['url']}'>{result['title']}</a>"
    if result["title_japanese"]:
        caption += f" ({result['title_japanese']})\n"
    else:
        caption += "\n"
    alternative_names = []
    if result["title_english"] is not None:
        alternative_names.append(result["title_english"])
    alternative_names.extend(result["title_synonyms"])
    if alternative_names:
        alternative_names_string = ", ".join(alternative_names)
        caption += f"\n<b>Also known as</b> : <code>{alternative_names_string}</code>\n"
    genre_string = ", ".join(genre_info["name"] for genre_info in result["genres"])
    if result["synopsis"] is not None:
        synopsis = result["synopsis"].split(" ", 60)
        try:
            synopsis.pop(60)
        except IndexError:
            pass
        synopsis_string = " ".join(synopsis) + "..."
    else:
        synopsis_string = "Unknown"
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    if search_type == "anime_anime":
        caption += textwrap.dedent(
            f"""
            <b>Type :</b> <code>{result['type']}</code>
            <b>Status :</b> <code>{result['status']}</code>
            <b>Aired :</b> <code>{result['aired']['string']}</code>
            <b>Episodes :</b> <code>{result['episodes']} ({result['duration']})</code>
            <b>Rating :</b> <code>{result['score']}</code>
            <b>Premiered :</b> <code>{result['premiered']}</code>
            <b>Genres :</b> <code>{genre_string}</code>
            <b>Studios :</b> <code>{studio_string}</code>
            <b>Producers :</b> <code>{producer_string}</code>
            <b>Trailer :</b> {LOL}
            <b>📖 Synopsis :</b> <i>{synopsis_string}</i> <a href='{result['url']}'>Read More</a>
        """
        )
    elif search_type == "anime_manga":
        caption += textwrap.dedent(
            f"""
            <b>Type :</b> <code>{result['type']}</code>
            <b>Status :</b> <code>{result['status']}</code>
            <b>Volumes :</b> <code>{result['volumes']}</code>
            <b>Chapters :</b> <code>{result['chapters']}</code>
            <b>Score :</b> <code>{result['score']}</code>
            <b>Genres :</b> <code>{genre_string}</code>
            📖 <b>Synopsis :</b> <i>{synopsis_string}</i> <a href='{result['url']}'>Read More</a>
        """
        )
    return caption, image


def get_poster(query):
    url_enc_name = query.replace(" ", "+")
    # Searching for query list in imdb
    page = requests.get(
        f"https://www.imdb.com/find?ref_=nv_sr_fn&q={url_enc_name}&s=all"
    )
    soup = bs4.BeautifulSoup(page.content, "lxml")
    odds = soup.findAll("tr", "odd")
    # Fetching the first post from search
    page_link = "http://www.imdb.com/" + odds[0].findNext("td").findNext("td").a["href"]
    page1 = requests.get(page_link)
    soup = bs4.BeautifulSoup(page1.content, "lxml")
    # Poster Link
    image = soup.find("link", attrs={"rel": "image_src"}).get("href", None)
    if image is not None:
        # img_path = wget.download(image, os.path.join(Config.DOWNLOAD_LOCATION, 'imdb_poster.jpg'))
        return image


def replace_text(text):
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


async def callAPI(search_str):
    query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          chapters
          volumes
          season
          type
          format
          status
          duration
          averageScore
          genres
          bannerImage
      }
    }
    """
    variables = {"search": search_str}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.text


async def formatJSON(outData):
    msg = ""
    jsonData = json.loads(outData)
    res = list(jsonData.keys())
    if "errors" in res:
        msg += f"**Error** : `{jsonData['errors'][0]['message']}`"
    else:
        jsonData = jsonData["data"]["Media"]
        if "bannerImage" in jsonData.keys():
            msg += f"[〽️]({jsonData['bannerImage']})"
        else:
            msg += "〽️"
        title = jsonData["title"]["romaji"]
        link = f"https://anilist.co/anime/{jsonData['id']}"
        msg += f"[{title}]({link})"
        msg += f"\n\n**Type** : {jsonData['format']}"
        msg += "\n**Genres** : "
        for g in jsonData["genres"]:
            msg += g + " "
        msg += f"\n**Status** : {jsonData['status']}"
        msg += f"\n**Episode** : {jsonData['episodes']}"
        msg += f"\n**Year** : {jsonData['startDate']['year']}"
        msg += f"\n**Score** : {jsonData['averageScore']}"
        msg += f"\n**Duration** : {jsonData['duration']} min\n\n"
        cat = f"{jsonData['description']}"
        msg += " __" + re.sub("<br>", "\n", cat) + "__"

    return msg


@man_cmd(pattern="anilist ?(.*)")
async def anilist(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    result = await callAPI(input_str)
    msg = await formatJSON(result)
    await edit_or_reply(event, msg, link_preview=True)


@man_cmd(pattern="anime ?(.*)")
async def search_anime(message):
    search_query = message.pattern_match.group(1)
    await message.get_reply_message()
    xx = await edit_or_reply(message, "`Searching Anime..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("anime", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_anime", message.chat_id)
    try:
        await xx.delete()
        await message.client.send_file(
            message.chat_id, file=image, caption=caption, parse_mode="HTML"
        )
    except BaseException:
        image = getBannerLink(first_mal_id, False)
        await message.client.send_file(
            message.chat_id, file=image, caption=caption, parse_mode="HTML"
        )


@man_cmd(pattern=r"manga ?(.*)")
async def search_manga(message):
    search_query = message.pattern_match.group(1)
    await message.get_reply_message()
    xx = await edit_or_reply(message, "`Searching Manga..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("manga", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_manga", message.chat_id)
    await xx.delete()
    await message.client.send_file(
        message.chat_id, file=image, caption=caption, parse_mode="HTML"
    )


@man_cmd(pattern="a(kaizoku|kayo) ?(.*)")
async def site_search(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(2)
    site = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        return await edit_delete(event, "`Uuf Bro.. Gib something to Search`")
    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<a href='{search_url}'>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n\n"
            for entry in search_result:
                post_link = entry.a["href"]
                post_name = html.escape(entry.text.strip())
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
                await event.edit(result, parse_mode="HTML")
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"
            await event.edit(result, parse_mode="HTML")

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<a href='{search_url}'>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n\n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
            await edit_or_reply(event, result, parse_mode="HTML")


@man_cmd(pattern="char ?(.*)")
async def character(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        await edit_or_reply(event, "Format: `.char <character name>`")
        return
    xx = await edit_delete(event, "`Searching Character...`")
    try:
        search_result = jikan.search("character", search_query)
    except APIException:
        return await xx.edit("`Character not found.`")
    first_mal_id = search_result["results"][0]["mal_id"]
    character = jikan.character(first_mal_id)
    caption = f"[{character['name']}]({character['url']})"
    if character["name_kanji"] != "Japanese":
        caption += f" ({character['name_kanji']})\n"
    else:
        caption += "\n"
    if character["nicknames"]:
        nicknames_string = ", ".join(character["nicknames"])
        caption += f"\n**Nicknames** : `{nicknames_string}`"
    about = character["about"].split(" ", 60)
    try:
        about.pop(60)
    except IndexError:
        pass
    about_string = " ".join(about)
    mal_url = search_result["results"][0]["url"]
    for entity in character:
        if character[entity] is None:
            character[entity] = "Unknown"
    caption += f"\n🔰**Extracted Character Data**🔰\n\n{about_string}"
    caption += f" [Read More]({mal_url})..."
    await xx.delete()
    await event.client.send_file(
        event.chat_id,
        file=character["image_url"],
        caption=replace_text(caption),
        reply_to=event,
    )


@man_cmd(pattern="upcoming$")
async def upcoming(message):
    rep = "<b>Upcoming anime</b>\n"
    later = jikan.season_later()
    anime = later.get("anime")
    for new in anime:
        name = new.get("title")
        url = new.get("url")
        rep += f"• <a href='{url}'>{name}</a>\n"
        if len(rep) > 1000:
            break
        await edit_or_reply(message, rep, parse_mode="html")


@man_cmd(pattern="whatanime$")
async def whatanime(e):
    media = e.media
    if not media:
        r = await e.get_reply_message()
        media = getattr(r, "media", None)
    if not media:
        await edit_delete(e, "`Media required`")
        return
    ig = is_gif(media) or is_video(media)
    if not is_image(media) and not ig:
        await edit_delete(e, "`Media must be an image or gif or video`")
        return
    filename = "file.jpg"
    if not ig and isinstance(media, MessageMediaDocument):
        attribs = media.document.attributes
        for i in attribs:
            if isinstance(i, DocumentAttributeFilename):
                filename = i.file_name
                break
    xx = await edit_or_reply(e, "`Downloading image..`")
    content = await e.client.download_media(media, bytes, thumb=-1 if ig else None)
    await xx.edit("`Searching for result..`")
    file = memory_file(filename, content)
    async with aiohttp.ClientSession() as session:
        url = "https://api.trace.moe/search?anilistInfo"
        async with session.post(url, data={"image": file}) as raw_resp0:
            resp0 = await raw_resp0.json()
        js0 = resp0.get("result")
        if not js0:
            await xx.edit("`No results found.`")
            return
        js0 = js0[0]
        text = f'<b>{html.escape(js0["anilist"]["title"]["romaji"])}'
        if js0["anilist"]["title"]["native"]:
            text += f' ({html.escape(js0["anilist"]["title"]["native"])})'
        text += "</b>\n"
        if js0["episode"]:
            text += f'<b>Episode:</b> {html.escape(str(js0["episode"]))}\n'
        percent = round(js0["similarity"] * 100, 2)
        text += f"<b>Similarity:</b> {percent}%\n"
        at = re.findall(r"t=(.+)&", js0["video"])[0]
        dt = pendulum.from_timestamp(float(at))
        text += f"<b>At:</b> {html.escape(dt.to_time_string())}"
        await e.edit(text, parse_mode="html")
        dt0 = pendulum.from_timestamp(js0["from"])
        dt1 = pendulum.from_timestamp(js0["to"])
        ctext = (
            f"{html.escape(dt0.to_time_string())} - {html.escape(dt1.to_time_string())}"
        )
        async with session.get(js0["video"]) as raw_resp1:
            file = memory_file("preview.mp4", await raw_resp1.read())
        try:
            await xx.edit(ctext, file=file, parse_mode="html")
        except FilePartsInvalidError:
            await xx.edit("`Cannot send preview.`")


def memory_file(name=None, contents=None, *, _bytes=True):
    if isinstance(contents, str) and _bytes:
        contents = contents.encode()
    file = BytesIO() if _bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file


def is_gif(file):
    # ngl this should be fixed, telethon.utils.is_gif but working
    # lazy to go to github and make an issue kek
    if not is_video(file):
        return False
    return DocumentAttributeAnimated() in getattr(file, "document", file).attributes


CMD_HELP.update(
    {
        "anime": f"**Plugin : **`anime`\
        \n\n  •  **Syntax :** `{cmd}anilist` **<nama anime>**\
        \n  •  **Function : **Mencari informasi anime dari anilist\
        \n\n  •  **Syntax :** `{cmd}anime` **<nama anime>**\
        \n  •  **Function : **Mencari infomasi anime.\
        \n\n  •  **Syntax :** `{cmd}manga` **<manga name>**\
        \n  •  **Function : **Menari informasi manga.\
        \n\n  •  **Syntax :** `{cmd}akaizoku` atau `.akayo` **<nama anime>**\
        \n  •  **Function : **Mencari anime dan memberikan link tautan Unduh Anime.\
        \n\n  •  **Syntax :** `{cmd}char` **<nama character anime>**\
        \n  •  **Function : **Mencari informasi karakter anime.\
        \n\n  •  **Syntax :** `{cmd}upcoming`\
        \n  •  **Function : **Mencari informasi Anime yang akan datang.\
        \n\n  •  **Syntax :** `{cmd}scanime` **<nama anime>** atau `.sanime` **<nama anime>**\
        \n  •  **Function : **Mencari anime\
        \n\n  •  **Syntax :** `{cmd}smanga` **<manga>**\
        \n  •  **Function : **Untuk mencari akun terhapus dalam grup\
        \n\n  •  **Syntax :** `{cmd}whatanime` **<Reply Gambar scene Anime.>**\
        \n  •  **Function : **Temukan anime dari file media.\
    "
    }
)
