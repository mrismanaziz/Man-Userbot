# Credits: @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import os

import heroku3
from telethon.tl.functions.users import GetFullUserRequest

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_HANDLER, SUDO_USERS
from userbot.utils import edit_delete, edit_or_reply, man_cmd

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
sudousers = os.environ.get("SUDO_USERS") or ""


@man_cmd(pattern="sudo$")
async def sudo(event):
    sudo = "True" if SUDO_USERS else "False"
    users = sudousers
    if sudo == "True":
        await edit_or_reply(
            event,
            f"🔮 **Sudo:** `Enabled`\n\n📚 ** List Sudo Users:**\n» `{users}`\n\n**SUDO_HANDLER:** `{SUDO_HANDLER}`",
        )
    else:
        await edit_delete(event, "🔮 **Sudo:** `Disabled`")


@man_cmd(pattern="addsudo(?:\s|$)([\s\S]*)")
async def add(event):
    suu = event.text[9:]
    if f"{cmd}add " in event.text:
        return
    if event.sender_id in SUDO_USERS:
        return
    xxnx = await edit_or_reply(event, "`Processing...`")
    var = "SUDO_USERS"
    reply = await event.get_reply_message()
    if not suu and not reply:
        return await edit_delete(
            xxnx,
            "Balas ke pengguna atau berikan user id untuk menambahkannya ke daftar pengguna sudo anda.",
            45,
        )
    if suu and not suu.isnumeric():
        return await edit_delete(
            xxnx, "Berikan User ID atau reply ke pesan penggunanya.", 45
        )
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            xxnx,
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan pengguna sudo**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    if suu:
        target = suu
    elif reply:
        target = await get_user(event)
    suudo = f"{sudousers} {target}"
    newsudo = suudo.replace("{", "")
    newsudo = newsudo.replace("}", "")
    await xxnx.edit(
        f"**Berhasil Menambahkan** `{target}` **ke Pengguna Sudo.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
    )
    heroku_Config[var] = newsudo


@man_cmd(pattern="delsudo(?:\s|$)([\s\S]*)")
async def _(event):
    if event.sender_id in SUDO_USERS:
        return
    suu = event.text[8:]
    xxx = await edit_or_reply(event, "`Processing...`")
    reply = await event.get_reply_message()
    if not suu and not reply:
        return await edit_delete(
            xxx,
            "Balas ke pengguna atau berikan user id untuk menghapusnya dari daftar pengguna sudo Anda.",
            45,
        )
    if suu and not suu.isnumeric():
        return await edit_delete(
            xxx, "Berikan User ID atau reply ke pesan penggunanya.", 45
        )
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            xxx,
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menghapus pengguna sudo**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    if suu != "" and suu.isnumeric():
        target = suu
    elif reply:
        target = await get_user(event)
    gett = str(target)
    if gett in sudousers:
        newsudo = sudousers.replace(gett, "")
        await xxx.edit(
            f"**Berhasil Menghapus** `{target}` **dari Pengguna Sudo.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
        )
        var = "SUDO_USERS"
        heroku_Config[var] = newsudo
    else:
        await edit_delete(
            xxx, "**Pengguna ini tidak ada dalam Daftar Pengguna Sudo anda.**", 45
        )


@man_cmd(pattern="listsudo")
async def sudolists(event):
    xx = await edit_or_reply(event, "`Processing...`")
    app = Heroku.app(HEROKU_APP_NAME)
    app.config()
    if not sudousers:
        return await edit_delete(event, "**Daftar Sudo Kosong**")
    sudos = sudousers.split(" ")
    sudoz = "**» List Sudo «**"
    for sudo in sudos:
        k = await event.client.get_entity(int(sudo))
        pro = f"\n[**Name:** {k.first_name} \n**Username:~** @{k.username or None}]\n"
        sudoz += pro
    await xx.edit(sudoz)


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    return replied_user.user.id


CMD_HELP.update(
    {
        "sudo": f"**Plugin : **`sudo`\
        \n\n  •  **Syntax :** `{cmd}sudo`\
        \n  •  **Function : **Untuk Mengecek informasi Sudo.\
        \n\n  •  **Syntax :** `{cmd}addsudo` <reply/user id>\
        \n  •  **Function : **Untuk Menambahkan User ke Pengguna Sudo.\
        \n\n  •  **Syntax :** `{cmd}delsudo` <reply/user id>\
        \n  •  **Function : **Untuk Menghapus User dari Pengguna Sudo.\
        \n\n  •  **NOTE: Berikan Hak Sudo anda Kepada orang yang anda percayai**\
    "
    }
)
