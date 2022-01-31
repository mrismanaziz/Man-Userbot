# Coded by KenHV
# Recode by @mrismanaziz
# FORM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, LOGS, STORAGE, SUDO_USERS
from userbot.utils import edit_or_reply, man_cmd

if not hasattr(STORAGE, "userObj"):
    STORAGE.userObj = False


@man_cmd(pattern="clone ?(.*)")
async def impostor(event):
    if event.sender_id in SUDO_USERS:
        return
    inputArgs = event.pattern_match.group(1)
    xx = await edit_or_reply(event, "`Processing...`")
    if "restore" in inputArgs:
        await event.edit("**Kembali ke identitas asli...**")
        if not STORAGE.userObj:
            return await xx.edit("**Anda harus mengclone orang dulu sebelum kembali!**")
        await updateProfile(event, STORAGE.userObj, restore=True)
        return await xx.edit("**Berhasil Mengembalikan Akun Anda dari clone**")
    if inputArgs:
        try:
            user = await event.client.get_entity(inputArgs)
        except BaseException:
            return await xx.edit("**Username/ID tidak valid.**")
        userObj = await event.client(GetFullUserRequest(user))
    elif event.reply_to_msg_id:
        replyMessage = await event.get_reply_message()
        if replyMessage.sender_id is None:
            return await xx.edit("**Tidak dapat menyamar sebagai admin anonim 🥺**")
        userObj = await event.client(GetFullUserRequest(replyMessage.sender_id))
    else:
        return await xx.edit("**Ketik** `.help clone` **bila butuh bantuan.**")

    if not STORAGE.userObj:
        STORAGE.userObj = await event.client(GetFullUserRequest(event.sender_id))

    LOGS.info(STORAGE.userObj)
    await xx.edit("**Mencuri identitas orang ini...**")
    await updateProfile(event, userObj)
    await xx.edit("**Aku adalah kamu dan kamu adalah aku. asekk 🥴**")


async def updateProfile(event, userObj, restore=False):
    firstName = (
        "Deleted Account"
        if userObj.user.first_name is None
        else userObj.user.first_name
    )
    lastName = "" if userObj.user.last_name is None else userObj.user.last_name
    userAbout = userObj.about if userObj.about is not None else ""
    userAbout = "" if len(userAbout) > 70 else userAbout
    if restore:
        userPfps = await event.client.get_profile_photos("me")
        userPfp = userPfps[0]
        await event.client(
            DeletePhotosRequest(
                id=[
                    InputPhoto(
                        id=userPfp.id,
                        access_hash=userPfp.access_hash,
                        file_reference=userPfp.file_reference,
                    )
                ]
            )
        )
    else:
        try:
            userPfp = userObj.profile_photo
            pfpImage = await event.client.download_media(userPfp)
            await event.client(
                UploadProfilePhotoRequest(await event.client.upload_file(pfpImage))
            )
        except BaseException:
            pass
    await event.client(
        UpdateProfileRequest(about=userAbout, first_name=firstName, last_name=lastName)
    )


CMD_HELP.update(
    {
        "clone": f"**Plugin : **`clone`\
        \n\n  •  **Syntax :** `{cmd}clone` <reply/username/ID>\
        \n  •  **Function : **Untuk mengclone identitas dari username/ID Telegram yang diberikan.\
        \n\n  •  **Syntax :** `{cmd}clone restore`\
        \n  •  **Function : **Mengembalikan ke identitas asli anda.\
        \n\n  •  **NOTE :** `{cmd}clone restore` terlebih dahulu sebelum mau nge `{cmd}clone` lagi.\
    "
    }
)
