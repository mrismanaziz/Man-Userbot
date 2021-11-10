# Credits: @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import os
from pathlib import Path

from userbot import CMD_HELP, bot
from userbot.events import man_cmd
from userbot.utils import edit_or_reply, load_module, remove_plugin, reply_id


@bot.on(man_cmd(outgoing=True, pattern="install$"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            await event.edit("`Installing Modules...`")
            downloaded_file_name = (
                await event.client.download_media(  # pylint:disable=E0602
                    await event.get_reply_message(),
                    "userbot/modules/",  # pylint:disable=E0602
                )
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit(
                    "**Plugin** `{}` **Berhasil di install**".format(
                        os.path.basename(downloaded_file_name)
                    )
                )
            else:
                os.remove(downloaded_file_name)
                await event.edit("**Error!** Plugin ini sudah terinstall di userbot.")
        except Exception as e:
            await event.edit(str(e))
            os.remove(downloaded_file_name)


@bot.on(man_cmd(outgoing=True, pattern=r"psend ([\s\S]*)"))
async def send(event):
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./userbot/modules/{input_str}.py"
    if os.path.exists(the_plugin_file):
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            thumb="userbot/resources/logo.jpg",
            allow_cache=False,
            reply_to=reply_to_id,
            caption=f"➠ **Nama Plugin:** `{input_str}`",
        )
        await event.delete()
    else:
        await edit_or_reply(event, "**ERROR: Modules Tidak ditemukan**")


@bot.on(man_cmd(outgoing=True, pattern=r"uninstall (?P<shortname>\w+)"))
async def uninstall(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    dir_path = f"./userbot/modules/{shortname}.py"
    try:
        remove_plugin(shortname)
        os.remove(dir_path)
        await event.edit(f"**Berhasil Menghapus Modules** `{shortname}`")
    except OSError as e:
        await event.edit("**ERROR:** `%s` : %s" % (dir_path, e.strerror))


CMD_HELP.update(
    {
        "core": "**Plugin : **`core`\
        \n\n  •  **Syntax :** `.install` <reply ke file module>\
        \n  •  **Function : **Untuk Menginstall module userbot secara instan.\
        \n\n  •  **Syntax :** `.uninstall` <nama module>\
        \n  •  **Function : **Untuk Menguninstall / Menghapus module userbot secara instan.\
        \n\n  •  **Syntax :** `.psend` <nama module>\
        \n  •  **Function : **Untuk Mengirim module userbot secara instan.\
    "
    }
)
