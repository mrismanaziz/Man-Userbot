# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import html
import json
import re
import textwrap
from io import BytesIO, StringIO
from urllib.parse import quote as urlencode

import aiohttp
import bs4
import jikanpy
import pendulum
import requests
from html_telegraph_poster import TelegraphPoster
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from telethon.errors.rpcerrorlist import FilePartsInvalidError
from telethon.tl.types import (
    DocumentAttributeAnimated,
    DocumentAttributeFilename,
    MessageMediaDocument,
)
from telethon.utils import is_image, is_video

from userbot import CMD_HELP
from userbot.events import register

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
            LOL = f"<a href='{trailer}'>Trailer</a>"
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
    caption = f"📺 <a href='{result['url']}'>{result['title']}</a>"
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
        caption += f"\n<b>Also known as</b>: <code>{alternative_names_string}</code>"
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
        🆎 <b>Type</b>: <code>{result['type']}</code>
        📡 <b>Status</b>: <code>{result['status']}</code>
        🎙️ <b>Aired</b>: <code>{result['aired']['string']}</code>
        🔢 <b>Episodes</b>: <code>{result['episodes']}</code>
        💯 <b>Score</b>: <code>{result['score']}</code>
        🌐 <b>Premiered</b>: <code>{result['premiered']}</code>
        ⌛ <b>Duration</b>: <code>{result['duration']}</code>
        🎭 <b>Genres</b>: <code>{genre_string}</code>
        🎙️ <b>Studios</b>: <code>{studio_string}</code>
        💸 <b>Producers</b>: <code>{producer_string}</code>
        🎬 <b>Trailer:</b> {LOL}
        📖 <b>Synopsis</b>: <code>{synopsis_string}</code> <a href='{result['url']}'>Read More</a>
        """
        )
    elif search_type == "anime_manga":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <code>{result['type']}</code>
        📡 <b>Status</b>: <code>{result['status']}</code>
        🔢 <b>Volumes</b>: <code>{result['volumes']}</code>
        📃 <b>Chapters</b>: <code>{result['chapters']}</code>
        💯 <b>Score</b>: <code>{result['score']}</code>
        🎭 <b>Genres</b>: <code>{genre_string}</code>
        📖 <b>Synopsis</b>: <code>{synopsis_string}</code>
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


def post_to_telegraph(title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "WeebProject"
    auth_url = "https://github.com/BianSepang/WeebProject"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=title,
        author=auth_name,
        author_url=auth_url,
        text=html_format_content,
    )
    return post_page["url"]


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


@register(outgoing=True, pattern=r"^\.anilist ?(.*)")
async def anilist(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    result = await callAPI(input_str)
    msg = await formatJSON(result)
    await event.edit(msg, link_preview=True)


@register(outgoing=True, pattern=r"^\.anime ?(.*)")
async def anime(event):
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    await event.edit("`Searching Anime...`")
    if query:
        pass
    elif reply:
        query = reply.text
    else:
        await event.edit("`Bruh.. What I am supposed to search ?`")
        await asyncio.sleep(6)
        await event.delete()
        return
    try:
        res = jikan.search("anime", query)
    except Exception as err:
        await event.edit(f"**Error:** \n`{err}`")
        return
    try:
        res = res.get("results")[0].get("mal_id")  # Grab first result
    except APIException:
        await event.edit("`Error connecting to the API. Please try again!`")
        return
    if res:
        anime = jikan.anime(res)
        title = anime.get("title")
        japanese = anime.get("title_japanese")
        anime.get("title_english")
        type = anime.get("type")
        duration = anime.get("duration")
        synopsis = anime.get("synopsis")
        source = anime.get("source")
        status = anime.get("status")
        episodes = anime.get("episodes")
        score = anime.get("score")
        rating = anime.get("rating")
        genre_lst = anime.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        studios = ""
        studio_lst = anime.get("studios")
        for studio in studio_lst:
            studios += studio.get("name") + ", "
        studios = studios[:-2]
        duration = anime.get("duration")
        premiered = anime.get("premiered")
        image_url = anime.get("image_url")
        trailer = anime.get("trailer_url")
        if trailer:
            bru = f"<a href='{trailer}'>Trailer</a>"
        url = anime.get("url")
    else:
        await event.edit("`No results Found!`")
        return
    rep = f"<b>{title}</b> - ({japanese})\n"
    rep += f"<b>Type:</b> <code>{type}</code>\n"
    rep += f"<b>Source:</b> <code>{source}</code>\n"
    rep += f"<b>Status:</b> <code>{status}</code>\n"
    rep += f"<b>Genres:</b> <code>{genres}</code>\n"
    rep += f"<b>Episodes:</b> <code>{episodes}</code>\n"
    rep += f"<b>Duration:</b> <code>{duration}</code>\n"
    rep += f"<b>Score:</b> <code>{score}</code>\n"
    rep += f"<b>Studio(s):</b> <code>{studios}</code>\n"
    rep += f"<b>Premiered:</b> <code>{premiered}</code>\n"
    rep += f"<b>Rating:</b> <code>{rating}</code>\n\n"
    rep += f"<a href='{image_url}'>\u200c</a>"
    rep += f"📖 <b>Synopsis</b>: <i>{synopsis}</i>\n"
    rep += f'<b>Read More:</b> <a href="{url}">MyAnimeList</a>'
    await event.edit(rep, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.manga ?(.*)")
async def manga(event):
    query = event.pattern_match.group(1)
    await event.edit("`Searching Manga...`")
    if not query:
        await event.edit("`Bruh.. Gib me Something to Search`")
        return
    res = ""
    manga = ""
    try:
        res = jikan.search("manga", query).get("results")[0].get("mal_id")
    except APIException:
        await event.edit("`Error connecting to the API. Please try again!`")
        return ""
    if res:
        try:
            manga = jikan.manga(res)
        except APIException:
            await event.edit("`Error connecting to the API. Please try again!`")
            return ""
        title = manga.get("title")
        japanese = manga.get("title_japanese")
        type = manga.get("type")
        status = manga.get("status")
        score = manga.get("score")
        volumes = manga.get("volumes")
        chapters = manga.get("chapters")
        genre_lst = manga.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        synopsis = manga.get("synopsis")
        image = manga.get("image_url")
        url = manga.get("url")
        rep = f"<b>{title} ({japanese})</b>\n"
        rep += f"<b>Type:</b> <code>{type}</code>\n"
        rep += f"<b>Status:</b> <code>{status}</code>\n"
        rep += f"<b>Genres:</b> <code>{genres}</code>\n"
        rep += f"<b>Score:</b> <code>{score}</code>\n"
        rep += f"<b>Volumes:</b> <code>{volumes}</code>\n"
        rep += f"<b>Chapters:</b> <code>{chapters}</code>\n\n"
        rep += f"<a href='{image}'>\u200c</a>"
        rep += f"📖 <b>Synopsis</b>: <i>{synopsis}</i>\n"
        rep += f'<b>Read More:</b> <a href="{url}">MyAnimeList</a>'
        await event.edit(rep, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.a(kaizoku|kayo) ?(.*)")
async def site_search(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(2)
    site = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        await event.edit("`Uuf Bro.. Gib something to Search`")
        return

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
            await event.edit(result, parse_mode="HTML")


@register(outgoing=True, pattern=r"^\.char ?(.*)")
async def character(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        await event.edit("Format: `.char <character name>`")
        return

    try:
        search_result = jikan.search("character", search_query)
    except APIException:
        await event.edit("`Character not found.`")
        return
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
    await event.delete()
    await event.client.send_file(
        event.chat_id,
        file=character["image_url"],
        caption=replace_text(caption),
        reply_to=event,
    )


@register(outgoing=True, pattern=r"^\.upcoming ?(.*)")
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
        await message.edit(rep, parse_mode="html")


@register(outgoing=True, pattern=r"^\.scanime ?(.*)")
async def get_anime(message):
    try:
        query = message.pattern_match.group(1)
    except IndexError:
        if message.reply_to_msg_id:
            query = await message.get_reply_message().text
        else:
            await message.reply(
                "You gave nothing to search. (｡ì _ í｡)\n `Usage: .scanime <anime name>`"
            )
            return
    except Exception as err:
        await message.edit(f"**Encountered an Unknown Exception**: \n{err}")
        return

    p_rm = await message.reply("`Searching Anime...`")
    f_mal_id = ""
    try:
        jikan = jikanpy.AioJikan()
        search_res = await jikan.search("anime", query)
        f_mal_id = search_res["results"][0]["mal_id"]
    except IndexError:
        await p_rm.edit(f"No Results Found for {query}")
        return
    except Exception as err:
        await p_rm.edit(f"**Encountered an Unknown Exception**: \n{err}")
        return

    results_ = await jikan.anime(f_mal_id)
    await jikan.close()
    await message.delete()

    # Get All Info of anime
    anime_title = results_["title"]
    jap_title = results_["title_japanese"]
    eng_title = results_["title_english"]
    type_ = results_["type"]
    results_["source"]
    episodes = results_["episodes"]
    status = results_["status"]
    results_["aired"].get("string")
    results_["duration"]
    rating = results_["rating"]
    score = results_["score"]
    synopsis = results_["synopsis"]
    results_["background"]
    producer_list = results_["producers"]
    studios_list = results_["studios"]
    genres_list = results_["genres"]

    # Info for Buttons
    mal_dir_link = results_["url"]
    trailer_link = results_["trailer_url"]

    main_poster = ""
    telegraph_poster = ""
    # Poster Links Search
    try:
        main_poster = get_poster(anime_title)
    except BaseException:
        pass
    try:
        telegraph_poster = getBannerLink(f_mal_id)
    except BaseException:
        pass
    # if not main_poster:
    main_poster = telegraph_poster
    if not telegraph_poster:
        telegraph_poster = main_poster

    genress_md = ""
    producer_md = ""
    studio_md = ""
    for i in genres_list:
        genress_md += f"{i['name']} "
    for i in producer_list:
        producer_md += f"[{i['name']}]({i['url']}) "
    for i in studios_list:
        studio_md += f"[{i['name']}]({i['url']}) "

    # Build synopsis telegraph post
    html_enc = ""
    html_enc += f"<img src = '{telegraph_poster}' title = {anime_title}/>"
    html_enc += "<br><b>» Synopsis: </b></br>"
    html_enc += f"<br><em>{synopsis}</em></br>"
    synopsis_link = post_to_telegraph(anime_title, html_enc)

    # Build captions:
    captions = f"""📺  `{anime_title}` - `{eng_title}` - `{jap_title}`
**🎭 Genre:** `{genress_md}`
**🆎 Type:** `{type_}`
**🔢 Episodes:** `{episodes}`
**📡 Status:** `{status}`
**🔞 Rating:** `{rating}`
**💯 Score:** `{score}`
[📖 Synopsis]({synopsis_link})
[🎬 Trailer]({trailer_link})
[📚 More Info]({mal_dir_link})
"""

    await p_rm.delete()
    await message.client.send_file(message.chat_id, file=main_poster, caption=captions)


@register(outgoing=True, pattern=r"^\.smanga ?(.*)")
async def manga(message):
    search_query = message.pattern_match.group(1)
    await message.get_reply_message()
    await message.edit("`Searching Manga..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("manga", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_manga", message.chat_id)
    await message.delete()
    await message.client.send_file(
        message.chat_id, file=image, caption=caption, parse_mode="HTML"
    )


@register(outgoing=True, pattern=r"^\.sanime ?(.*)")
async def anime(message):
    search_query = message.pattern_match.group(1)
    await message.get_reply_message()
    await message.edit("`Searching Anime..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("anime", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_anime", message.chat_id)
    try:
        await message.delete()
        await message.client.send_file(
            message.chat_id, file=image, caption=caption, parse_mode="HTML"
        )
    except BaseException:
        image = getBannerLink(first_mal_id, False)
        await message.client.send_file(
            message.chat_id, file=image, caption=caption, parse_mode="HTML"
        )


@register(outgoing=True, pattern=r"^\.whatanime")
async def whatanime(e):
    media = e.media
    if not media:
        r = await e.get_reply_message()
        media = getattr(r, "media", None)
    if not media:
        await e.edit("`Media required`")
        return
    ig = is_gif(media) or is_video(media)
    if not is_image(media) and not ig:
        await e.edit("`Media must be an image or gif or video`")
        return
    filename = "file.jpg"
    if not ig and isinstance(media, MessageMediaDocument):
        attribs = media.document.attributes
        for i in attribs:
            if isinstance(i, DocumentAttributeFilename):
                filename = i.file_name
                break
    await e.edit("`Downloading image..`")
    content = await e.client.download_media(media, bytes, thumb=-1 if ig else None)
    await e.edit("`Searching for result..`")
    file = memory_file(filename, content)
    async with aiohttp.ClientSession() as session:
        url = "https://trace.moe/api/search"
        async with session.post(url, data={"image": file}) as raw_resp0:
            resp0 = await raw_resp0.text()
        js0 = json.loads(resp0)["docs"]
        if not js0:
            await e.edit("`No results found.`")
            return
        js0 = js0[0]
        text = f'<b>{html.escape(js0["title_romaji"])}'
        if js0["title_native"]:
            text += f' ({html.escape(js0["title_native"])})'
        text += "</b>\n"
        if js0["episode"]:
            text += f'<b>Episode:</b> {html.escape(str(js0["episode"]))}\n'
        percent = round(js0["similarity"] * 100, 2)
        text += f"<b>Similarity:</b> {percent}%\n"
        dt = pendulum.from_timestamp(js0["at"])
        text += f"<b>At:</b> {html.escape(dt.to_time_string())}"
        await e.edit(text, parse_mode="html")
        dt0 = pendulum.from_timestamp(js0["from"])
        dt1 = pendulum.from_timestamp(js0["to"])
        ctext = (
            f"{html.escape(dt0.to_time_string())} - {html.escape(dt1.to_time_string())}"
        )
        url = (
            "https://media.trace.moe/video/"
            f'{urlencode(str(js0["anilist_id"]))}' + "/"
            f'{urlencode(js0["filename"])}'
            f'?t={urlencode(str(js0["at"]))}'
            f'&token={urlencode(js0["tokenthumb"])}'
        )
        async with session.get(url) as raw_resp1:
            file = memory_file("preview.mp4", await raw_resp1.read())
        try:
            await e.reply(ctext, file=file, parse_mode="html")
        except FilePartsInvalidError:
            await e.reply("`Cannot send preview.`")


def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
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
        "anime": "**Plugin : **`anime`\
        \n\n  •  **Syntax :** `.anilist` **<nama anime>**\
        \n  •  **Function : **Mencari informasi anime dari anilist\
        \n\n  •  **Syntax :** `.anime` **<nama anime>**\
        \n  •  **Function : **Mencari infomasi anime.\
        \n\n  •  **Syntax :** `.manga` **<manga name>**\
        \n  •  **Function : **Menari informasi manga.\
        \n\n  •  **Syntax :** `.akaizoku` atau `.akayo` **<nama anime>**\
        \n  •  **Function : **Mencari anime dan memberikan link tautan Unduh Anime.\
        \n\n  •  **Syntax :** `.char` **<nama character anime>**\
        \n  •  **Function : **Mencari informasi karakter anime.\
        \n\n  •  **Syntax :** `.upcoming`\
        \n  •  **Function : **Mencari informasi Anime yang akan datang.\
        \n\n  •  **Syntax :** `.scanime` **<nama anime>** atau `.sanime` **<nama anime>**\
        \n  •  **Function : **Mencari anime\
        \n\n  •  **Syntax :** `.smanga` **<manga>**\
        \n  •  **Function : **Untuk mencari akun terhapus dalam grup\
        \n\n  •  **Syntax :** `.whatanime` **<Reply Gambar scene Anime.>**\
        \n  •  **Function : **Temukan anime dari file media.\
    "
    }
)
