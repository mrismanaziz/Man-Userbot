#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  UniBorg Telegram UseRBot
#  Copyright (C) 2020 @UniBorg
#
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
#
# 114994699218449095458463470499996630
#

import asyncio
import logging
import os
import time
from mimetypes import guess_type

import aiofiles
import aiohttp
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file
from telethon import events

from userbot import (
    BOTLOG_CHATID,
    G_PHOTOS_AUTH_TOKEN_ID,
    G_PHOTOS_CLIENT_ID,
    G_PHOTOS_CLIENT_SECRET,
    TEMP_DOWNLOAD_DIRECTORY,
)
from userbot.events import register
from userbot.utils import progress

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)

# setup the gPhotos v1 API
OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/photoslibrary",
    "https://www.googleapis.com/auth/photoslibrary.sharing",
]
# Redirect URI for installed apps, can be left as is
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
#
PHOTOS_BASE_URI = "https://photoslibrary.googleapis.com"

TOKEN_FILE_NAME = "GP_LORD.json"


@register(outgoing=True, pattern=r"^\.gpsetup")
async def setup_google_photos(event):
    if event.chat_id != BOTLOG_CHATID:
        return
    token_file = TOKEN_FILE_NAME
    is_cred_exists, _ = await check_creds(token_file, event)
    if not is_cred_exists:
        await create_token_file(token_file, event)
    await event.edit("`CREDS Telah Dibuat`")


async def create_token_file(token_file, event):
    # Run through the OAuth flow and retrieve credentials
    flow = client.OAuth2WebServerFlow(
        G_PHOTOS_CLIENT_ID,
        G_PHOTOS_CLIENT_SECRET,
        OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    authorize_url = flow.step1_get_authorize_url()
    async with event.client.conversation(event.chat_id, timeout=600) as conv:
        await conv.send_message(
            "Pergi Ke "
            "Linknya Dan Ikuti "
            f"Browser Anda : {authorize_url} Dan "
            "Balas Kode"
        )
        response = await conv.wait_event(
            events.NewMessage(outgoing=True, chats=BOTLOG_CHATID)
        )
        # logger.info(response.stringify())
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = file.Storage(token_file)
        storage.put(credentials)
        imp_gsem = await conv.send_message(file=token_file)
        await imp_gsem.reply(
            "Mohon Setel Heroku ENV "
            "<code>G_PHOTOS_AUTH_TOKEN_ID</code> "
            "= "
            f"<u>{imp_gsem.id}</u> ..!"
            "\n\n<i>Ini Hanya Di Perlukan, "
            "Jika Anda Menjalankan Ephimeral File-System</i>.",
            parse_mode="html",
        )
        return storage


async def check_creds(token_file, event):
    if G_PHOTOS_AUTH_TOKEN_ID:
        confidential_message = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=G_PHOTOS_AUTH_TOKEN_ID
        )
        if confidential_message and confidential_message.file:
            await confidential_message.download_media(file=token_file)

    if os.path.exists(token_file):
        pho_storage = file.Storage(token_file)
        creds = pho_storage.get()
        if not creds or creds.invalid:
            return False, None
        creds.refresh(Http())
        return True, creds

    return False, None


@register(outgoing=True, pattern=r"^\.gp( -- (.*))?")
async def upload_google_photos(event):
    if event.fwd_from:
        return

    input_str = event.pattern_match.group(2)
    logger.info(input_str)

    if not event.reply_to_msg_id and not input_str:
        await event.edit(
            "©️ <b>[USERBOT]</b>\nTidak Ada Yang Akan Membantu Anda", parse_mode="html"
        )
        return

    token_file = TOKEN_FILE_NAME
    is_cred_exists, creds = await check_creds(token_file, event)
    if not is_cred_exists:
        await event.edit(
            "Pertama Jalankan <code>.gpsetup</code> Dulu", parse_mode="html"
        )

    service = build("photoslibrary", "v1", http=creds.authorize(Http()))

    # create directory if not exists
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    file_path = None

    if input_str and os.path.exists(input_str):
        file_path = input_str

    elif not input_str:
        media_message = await event.client.get_messages(
            entity=event.chat_id, ids=event.reply_to_msg_id
        )

        c_time = time.time()
        file_path = await media_message.download_media(
            file=TEMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "[DOWNLOADING]")
            ),
        )

    logger.info(file_path)

    if not file_path:
        await event.edit("<b>[BERHENTI MELAKUKAN SPAM]</b>", parse_mode="html")
        return

    file_name, mime_type, file_size = file_ops(file_path)
    await event.edit("`File downloaded, " "`Sedang Mengumpulkan Informasi Unggahan`")

    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Length": "0",
            "Lord-Goog-Upload-Command": "start",
            "Lord-Goog-Upload-Content-Type": mime_type,
            "Lord-Goog-Upload-File-Name": file_name,
            "Lord-Goog-Upload-Protocol": "resumable",
            "Lord-Goog-Upload-Raw-Size": str(file_size),
            "Authorization": "Bearer " + creds.access_token,
        }
        # Step 1: Initiating an upload session
        step_one_response = await session.post(
            f"{PHOTOS_BASE_URI}/v1/uploads",
            headers=headers,
        )

        if step_one_response.status != 200:
            await event.edit((await step_one_response.text()))
            return

        step_one_resp_headers = step_one_response.headers
        logger.info(step_one_resp_headers)
        # Step 2: Saving the session URL

        real_upload_url = step_one_resp_headers.get("Lord-Goog-Upload-URL")
        logger.info(real_upload_url)
        upload_granularity = int(
            step_one_resp_headers.get("Lord-Goog-Upload-Chunk-Granularity")
        )
        logger.info(upload_granularity)
        number_of_req_s = int((file_size / upload_granularity))
        logger.info(number_of_req_s)
        c_time = time.time()
        loop = asyncio.get_event_loop()
        async with aiofiles.open(file_path, mode="rb") as f_d:
            for i in range(number_of_req_s):
                current_chunk = await f_d.read(upload_granularity)
                offset = i * upload_granularity
                part_size = len(current_chunk)

                headers = {
                    "Content-Length": str(part_size),
                    "Lord-Goog-Upload-Command": "upload",
                    "Lord-Goog-Upload-Offset": str(offset),
                    "Authorization": "Bearer " + creds.access_token,
                }
                logger.info(i)
                logger.info(headers)
                response = await session.post(
                    real_upload_url, headers=headers, data=current_chunk
                )
                loop.create_task(
                    progress(
                        offset + part_size,
                        file_size,
                        event,
                        c_time,
                        "uploading(gphoto)🧐?",
                    )
                )
                logger.info(response.headers)

                # await f_d.seek(i * upload_granularity)
            # await f_d.seek(upload_granularity)
            current_chunk = await f_d.read(upload_granularity)

            logger.info(number_of_req_s)
            headers = {
                "Content-Length": str(len(current_chunk)),
                "Lord-Goog-Upload-Command": "upload, finalize",
                "Lord-Goog-Upload-Offset": str(number_of_req_s * upload_granularity),
                "Authorization": "Bearer " + creds.access_token,
            }
            logger.info(headers)
            response = await session.post(
                real_upload_url, headers=headers, data=current_chunk
            )
            logger.info(response.headers)

        final_response_text = await response.text()
        logger.info(final_response_text)

    await event.edit("`Mengunggah Foto Google, " "Mendapatkan FILE URI`")

    response_create_album = (
        service.mediaItems()
        .batchCreate(
            body={
                "newMediaItems": [
                    {
                        "description": file_name,
                        "simpleMediaItem": {
                            "fileName": file_name,
                            "uploadToken": final_response_text,
                        },
                    }
                ]
            }
        )
        .execute()
    )
    logger.info(response_create_album)

    try:
        photo_url = (
            response_create_album.get("newMediaItemResults")[0]
            .get("mediaItem")
            .get("productUrl")
        )
        await event.edit(
            f"`[BERHASIL]`\n\nMengunggah Foto Ke Google [Lihat]({photo_url})"
        )
    except Exception as e:
        await event.edit(str(e))


# Get mime type and name of given file
def file_ops(file_path):
    file_size = os.stat(file_path).st_size
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type, file_size
