# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for changing your Telegram profile details+ now u can steal personal details of user. """

import os

from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import PhotoExtInvalidError, UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import (
    DeletePhotosRequest,
    GetUserPhotosRequest,
    UploadProfilePhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    Channel,
    Chat,
    InputPhoto,
    MessageEntityMentionName,
    MessageMediaPhoto,
    User,
)
from telethon.utils import get_input_location

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register

# ====================== CONSTANT ===============================
INVALID_MEDIA = "```Maaf Media Tidak Valid.```"
PP_CHANGED = "```Foto Profil Anda Telah Berhasil Diubah.```"
PP_TOO_SMOL = "```Gambar Terlalu Kecil, Mohon Gunakan Yang Lebih Besar.```"
PP_ERROR = "```Kegagalan Terjadi Saat Proses Gambar, Foto Profil Gagal Diubah.```"

BIO_SUCCESS = "```Bio Anda Telah Berhasil Diubah.```"

NAME_OK = "```Nama Anda Telah Berhasil Diubah.```"
USERNAME_SUCCESS = "```Username Anda Sudah Diubah.```"
USERNAME_TAKEN = "```Mohon Maaf, Username Itu Sudah Ada Yang Menggunakannya.```"
# ===============================================================


@register(outgoing=True, pattern="^.reserved$")
async def mine(event):
    """ For .reserved command, get a list of your reserved usernames. """
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"{channel_obj.title}\n@{channel_obj.username}\n\n"
    await event.edit(output_str)


@register(outgoing=True, pattern="^.name")
async def update_name(name):
    """ For .name command, change your name in Telegram. """
    newname = name.text[6:]
    if " " not in newname:
        firstname = newname
        lastname = ""
    else:
        namesplit = newname.split(" ", 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    await name.client(UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await name.edit(NAME_OK)


@register(outgoing=True, pattern="^.setpfp$")
async def set_profilepic(propic):
    """ For .profilepic command, change your profile picture in Telegram. """
    replymsg = await propic.get_reply_message()
    photo = None
    if replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await propic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await propic.client.download_file(replymsg.media.document)
        else:
            await propic.edit(INVALID_MEDIA)

    if photo:
        try:
            await propic.client(
                UploadProfilePhotoRequest(await propic.client.upload_file(photo))
            )
            os.remove(photo)
            await propic.edit(PP_CHANGED)
        except PhotoCropSizeSmallError:
            await propic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await propic.edit(PP_ERROR)
        except PhotoExtInvalidError:
            await propic.edit(INVALID_MEDIA)


@register(outgoing=True, pattern="^.setbio (.*)")
async def set_biograph(setbio):
    """ For .setbio command, set a new bio for your profile in Telegram. """
    newbio = setbio.pattern_match.group(1)
    await setbio.client(UpdateProfileRequest(about=newbio))
    await setbio.edit(BIO_SUCCESS)


@register(outgoing=True, pattern="^.username (.*)")
async def update_username(username):
    """ For .username command, set a new username in Telegram. """
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@register(outgoing=True, pattern="^.count$")
async def count(event):
    """ For .count command, get profile stats. """
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("`Sedang Dalam Proses....`")
    dialogs = await bot.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)

    result += f"`Pengguna:`\t**{u}**\n"
    result += f"`Grup:`\t**{g}**\n"
    result += f"`Super Grup:`\t**{c}**\n"
    result += f"`Channel:`\t**{bc}**\n"
    result += f"`Bot:`\t**{b}**"

    await event.edit(result)


@register(outgoing=True, pattern=r"^.delpfp")
async def remove_profilepic(delpfp):
    """ For .delpfp command, delete your current profile picture in Telegram. """
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.from_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(
                id=sep.id,
                access_hash=sep.access_hash,
                file_reference=sep.file_reference,
            )
        )
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(f"`Berhasil Menghapus {len(input_photos)} Foto Profil.`")


@register(pattern=".info(?: |$)(.*)", outgoing=True)
async def who(event):

    await event.edit("`Mengambil Informasi Data User ini...`")

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        event.edit("`Saya Tidak Mendapatkan Informasi Pengguna.`")
        return

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )

        if not photo.startswith("http"):
            os.remove(photo)
        await event.delete()

    except TypeError:
        await event.edit(caption, parse_mode="html")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "This gay has no pic."
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, _ = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Tidak Dapat Mengambil DC ID!"
        str(e)
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(
        user_id, TEMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("Orang Ini Tidak Punya Nama Depan")
    )
    last_name = (
        last_name.replace("\u2060", "")
        if last_name
        else ("Orang Ini Tidak Punya Nama Belakang")
    )
    username = (
        "@{}".format(username)
        if username
        else ("Pengguna Ini Tidak Menggunakan Username")
    )
    user_bio = "Orang Ini Tidak Menggunakan Bio" if not user_bio else user_bio

    caption = "<b>Informasi Pengguna:</b>\n\n"
    caption += f"Nama Depan: {first_name}\n"
    caption += f"Nama Belakang: {last_name}\n"
    caption += f"Username: {username}\n"
    caption += f"Data Centre ID: {dc_id}\n"
    caption += f"Total Foto Profil: {replied_user_profile_photos_count}\n"
    caption += f"Apakah Bot: {is_bot}\n"
    caption += f"Dibatasi: {restricted}\n"
    caption += f"Diverifikasi Oleh Telegram: {verified}\n"
    caption += f"ID: <code>{user_id}</code>\n\n"
    caption += f"Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"Obrolan Umum Untuk Pengguna Ini: {common_chat}\n"
    caption += "Link Permanen Ke Profil: "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'

    return photo, caption


CMD_HELP.update(
    {
        "profil": "**Plugin : **`profil`\
        \n\n  •  **Syntax :** `.username` <username baru>\
        \n  •  **Function : **Menganti Username Telegram.\
        \n\n  •  **Syntax :** `.name` <nama depan> atau `.name` <Nama Depan> <Nama Belakang>\
        \n  •  **Function : **Menganti Nama Telegram Anda.\
        \n\n  •  **Syntax :** `.setbio` <bio baru>\
        \n  •  **Function : **Untuk Mengganti Bio Telegram.\
        \n\n  •  **Syntax :** `.setpfp`\
        \n  •  **Function : **Balas Ke Gambar Ketik .setpfp Untuk Mengganti Foto Profil Telegram.\
        \n\n  •  **Syntax :** `.delpfp` atau `.delpfp` <berapa profil>/<all>\
        \n  •  **Function : **Menghapus Foto Profil Telegram.\
        \n\n  •  **Syntax :** `.reserved`\
        \n  •  **Function : **Menunjukkan nama pengguna yang dipesan oleh Anda.\
        \n\n  •  **Syntax :** `.count`\
        \n  •  **Function : **Menghitung Grup, Chat, Bot dll.\
        \n\n  •  **Syntax :** `.info` <username> Atau Balas Ke Pesan Ketik `.data`\
        \n  •  **Function : **Mendapatkan Informasi Pengguna.\
    "
    }
)
