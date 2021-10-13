# Recode By @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import importlib
import logging
import os
import sys
from pathlib import Path

from userbot import CMD_HELP, DEVS, LOGS, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot import CMD_HANDLER as cmd
from userbot.events import man_cmd
from userbot.utils import edit_or_reply

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in DEVS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/modules/{shortname}.py")
        name = "userbot.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("Successfully imported " + shortname)
    else:

        path = Path(f"userbot/modules/{shortname}.py")
        name = "userbot.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.LOGS = LOGS
        mod.CMD_HELP = CMD_HELP
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["userbot.modules." + shortname] = mod
        LOGS.info("Successfully imported " + shortname)


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
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./userbot/modules/{input_str}.py"
    if os.path.exists(the_plugin_file):
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
            caption=f"➠ **Nama Plugin:** `{input_str}`",
        )
        await event.delete()
    else:
        await edit_or_reply(event, "**ERROR: Modules Tidak ditemukan**")


CMD_HELP.update(
    {
        "core": f"**Plugin : **`core`\
        \n\n  •  **Syntax :** `{cmd}install` <reply ke file module>\
        \n  •  **Function : **Untuk Menginstall plugins userbot secara instan.\
        \n\n  •  **Syntax :** `{cmd}psend` <nama module>\
        \n  •  **Function : **Untuk Mengirim module userbot secara instan.\
    "
    }
)
