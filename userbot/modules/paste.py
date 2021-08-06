# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module containing commands for interacting with dogbin(https://del.dog)"""

import os

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from requests import exceptions, get

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


class PasteBin:

    DOGBIN_URL = "https://del.dog/"
    HASTEBIN_URL = "https://hastebin.com/"
    NEKOBIN_URL = "https://nekobin.com/"
    _dkey = _hkey = _nkey = retry = None
    service_match = {"-d": "dogbin", "-n": "nekobin", "-h": "hastebin"}

    def __init__(self, data: str = None):
        self.http = aiohttp.ClientSession()
        self.data = data
        self.retries = 3

    def __bool__(self):
        return bool(self._dkey or self._nkey or self._hkey)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        await self.http.close()

    async def __call__(self, service="dogbin"):
        if service == "dogbin":
            await self._post_dogbin()
        elif service == "nekobin":
            await self._post_nekobin()
        elif service == "hastebin":
            await self._post_hastebin()
        else:
            raise KeyError(f"**Unknown service input:** {service}")

    async def _post_dogbin(self):
        if self._dkey:
            return
        try:
            async with self.http.post(
                self.DOGBIN_URL + "documents", data=self.data.encode("utf-8")
            ) as req:
                if req.status == 200:
                    res = await req.json()
                    self._dkey = res["key"]
                else:
                    self.retry = "nekobin"
        except ClientConnectorError:
            self.retry = "nekobin"

    async def _post_nekobin(self):
        if self._nkey:
            return
        try:
            async with self.http.post(
                self.NEKOBIN_URL + "api/documents", json={"content": self.data}
            ) as req:
                if req.status == 201:
                    res = await req.json()
                    self._nkey = res["result"]["key"]
                else:
                    self.retry = "hastebin"
        except ClientConnectorError:
            self.retry = "hastebin"

    async def _post_hastebin(self):
        if self._hkey:
            return
        try:
            async with self.http.post(
                self.HASTEBIN_URL + "documents", data=self.data.encode("utf-8")
            ) as req:
                if req.status == 200:
                    res = await req.json()
                    self._hkey = res["key"]
                else:
                    self.retry = "dogbin"
        except ClientConnectorError:
            self.retry = "dogbin"

    async def post(self, serv: str = "dogbin"):
        """Post the initialized data to the pastebin service."""
        if self.retries == 0:
            return

        await self.__call__(serv)

        if self.retry:
            self.retries -= 1
            await self.post(self.retry)
            self.retry = None

    @property
    def link(self) -> str:
        """Return the view link"""
        if self._dkey:
            return self.DOGBIN_URL + self._dkey
        if self._nkey:
            return self.NEKOBIN_URL + self._nkey
        if self._hkey:
            return self.HASTEBIN_URL + self._hkey
        return False

    @property
    def raw_link(self) -> str:
        """Return the view raw link"""
        if self._dkey:
            return self.DOGBIN_URL + "raw/" + self._dkey
        if self._nkey:
            return self.NEKOBIN_URL + "raw/" + self._nkey
        if self._hkey:
            return self.HASTEBIN_URL + "raw/" + self._hkey
        return False


@register(outgoing=True, pattern=r"^\.paste(?: (-d|-n|-h)|$)?(?: ([\s\S]+)|$)")
async def paste(pstl):
    """For .paste command, pastes the text directly to a pastebin."""
    service = pstl.pattern_match.group(1)
    match = pstl.pattern_match.group(2)
    reply_id = pstl.reply_to_msg_id

    if not (match or reply_id):
        return await pstl.edit("`Elon Musk said I cannot paste void.`")

    if match:
        message = match.strip()
    elif reply_id:
        message = await pstl.get_reply_message()
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = message.message

    await pstl.edit("`Pasting text . . .`")
    async with PasteBin(message) as client:
        if service:
            service = service.strip()
            if service not in ["-d", "-n", "-h"]:
                return await pstl.edit("Invalid flag")
            await client(client.service_match[service])
        else:
            await client.post()

        if client:
            reply_text = (
                "**Pasted successfully!**\n\n"
                f"[URL]({client.link})\n"
                f"[View RAW]({client.raw_link})"
            )
        else:
            reply_text = "**Failed to reach Pastebin Service**"

    await pstl.edit(reply_text, link_preview=False)


@register(outgoing=True, pattern=r"^\.getpaste(?: |$)(.*)")
async def get_dogbin_content(dog_url):
    """For .getpaste command, fetches the content of a dogbin URL."""
    DOGBIN_URL = PasteBin.DOGBIN_URL
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit("`Getting dogbin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f"{DOGBIN_URL}"
    format_view = f"{DOGBIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view) :]
    elif message.startswith(format_normal):
        message = message[len(format_normal) :]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/") :]
    else:
        return await dog_url.edit("`Is that even a dogbin url?`")

    resp = get(f"{DOGBIN_URL}raw/{message}")

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await dog_url.edit(
            "**Request returned an unsuccessful status code.**\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await dog_url.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await dog_url.edit(
            "Request exceeded the configured number of maximum redirections."
            + str(RedirectsErr)
        )
        return

    reply_text = (
        "**Fetched dogbin URL content successfully!**" "\n\n`Content:` " + resp.text
    )

    await dog_url.edit(reply_text)


CMD_HELP.update(
    {
        "paste": "**Plugin : **`paste`\
        \n\n  •  **Syntax :** `.paste` <text/reply>\
        \n  •  **Function : **Untuk Menyimpan text ke ke layanan pastebin gunakan flags [`-d`, `-n`, `-h`]\
        \n  •  **NOTE :** `-d` = **Dogbin** atau `-n` = **Nekobin** atau `-h` = **Hastebin**\
        \n\n  •  **Syntax :** `.getpaste` <reply/link>\
        \n  •  **Function : **Mendapatkan konten dari paste atau url singkat dari dogbin (https://del.dog/)\
    "
    }
)
