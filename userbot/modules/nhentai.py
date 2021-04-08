# Copyright (C) 2020 KeselekPermen69
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import re

from hentai import Hentai
from natsort import natsorted

from userbot import CMD_HELP
from userbot.events import register
from userbot.modules.anime import post_to_telegraph


@register(outgoing=True, pattern=r"^\.nhentai(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    code = input_str
    if "nhentai" in input_str:
        link_regex = r"(https?://)?(www\.)?nhentai\.net/g/(\d+)"
        match = re.match(link_regex, input_str)
        code = match.group(3)
    await event.edit("`Searching for doujin...`")
    try:
        doujin = Hentai(code)
    except BaseException as n_e:
        if "404" in str(n_e):
            return await event.edit(f"`{code}` is not found!")
        return await event.edit(f"**Error: **`{n_e}`")
    msg = ""
    imgs = ""
    for url in doujin.image_urls:
        imgs += f"<img src='{url}'/>"
    imgs = f"&#8205; {imgs}"
    title = doujin.title()
    graph_link = post_to_telegraph(title, imgs)
    msg += f"[{title}]({graph_link})"
    msg += f"\n**Source :**\n[{code}]({doujin.url})"
    if doujin.parody:
        msg += "\n**Parodies :**"
        parodies = []
        for parody in doujin.parody:
            parodies.append("#" + parody.name.replace(" ", "_").replace("-", "_"))
        msg += "\n" + " ".join(natsorted(parodies))
    if doujin.character:
        msg += "\n**Characters :**"
        charas = []
        for chara in doujin.character:
            charas.append("#" + chara.name.replace(" ", "_").replace("-", "_"))
        msg += "\n" + " ".join(natsorted(charas))
    if doujin.tag:
        msg += "\n**Tags :**"
        tags = []
        for tag in doujin.tag:
            tags.append("#" + tag.name.replace(" ", "_").replace("-", "_"))
        msg += "\n" + " ".join(natsorted(tags))
    if doujin.artist:
        msg += "\n**Artists :**"
        artists = []
        for artist in doujin.artist:
            artists.append("#" + artist.name.replace(" ", "_").replace("-", "_"))
        msg += "\n" + " ".join(natsorted(artists))
    if doujin.language:
        msg += "\n**Languages :**"
        languages = []
        for language in doujin.language:
            languages.append("#" + language.name.replace(" ", "_").replace("-", "_"))
        msg += "\n" + " ".join(natsorted(languages))
    if doujin.category:
        msg += "\n**Categories :**"
        categories = []
        for category in doujin.category:
            categories.append("#" + category.name.replace(" ", "_").replace("-", "_"))
        msg += "\n" + " ".join(natsorted(categories))
    msg += f"\n**Pages :**\n{doujin.num_pages}"
    await event.edit(msg, link_preview=True)


CMD_HELP.update(
    {
        "nhentai": "**Plugin : **`nhentai`\
        \n\n  •  **Syntax :** `.nhentai`\
        \n  •  **Function : **Melihat nhentai di telegra.ph XD\
    "
    }
)
