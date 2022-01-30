import asyncio

from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

import userbot.modules.sql_helper.antiflood_sql as sql
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd
from userbot.utils import edit_or_reply
from userbot.utils.tools import is_admin

CHAT_FLOOD = sql.__load_flood_settings()
# warn mode for anti flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@bot.on(events.NewMessage(incoming=True))
async def _(event):
    # logger.info(CHAT_FLOOD)
    if not CHAT_FLOOD:
        return
    admin_c = await is_admin(event.chat_id, event.message.from_id)
    if admin_c:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.from_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.from_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message="""**Automatic AntiFlooder**
[User](tg://user?id={}) Membanjiri obrolan.

`{}`""".format(
                event.message.from_id, str(e)
            ),
            reply_to=event.message.id,
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit("Sadly u don't have admin privilege")
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message="""**Automatic AntiFlooder**
[User](tg://user?id={}) Membanjiri obrolan.
**Aksi:** Saya membisukan dia 🔇""".format(
                event.message.from_id
            ),
            reply_to=event.message.id,
        )


@bot.on(man_cmd(outgoing=True, pattern="setflood(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await edit_or_reply(
            event,
            f"**Antiflood diperbarui menjadi** `{input_str}` **dalam obrolan saat ini**",
        )
    except Exception as e:
        await edit_or_reply(event, f"{e}")


CMD_HELP.update(
    {
        "antiflood": f"**Plugin : **`antiflood`\
        \n\n  •  **Syntax :** `{cmd}setflood` [jumlah pesan]\
        \n  •  **Function : **memperingatkan pengguna jika dia melakukan spam pada obrolan dan jika Anda adalah admin maka itu akan membisukan dia dalam grup itu.\
        \n\n  •  **NOTE :** Untuk mematikan setflood, atur jumlah pesan menjadi 0 » `.setflood 0`\
    "
    }
)
