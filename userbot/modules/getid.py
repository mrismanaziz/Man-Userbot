from telethon.utils import pack_bot_file_id

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, LOGS
from userbot.utils import edit_delete, edit_or_reply, man_cmd
from userbot.utils.logger import logging

LOGS = logging.getLogger(__name__)


@man_cmd(pattern="(get_id|id)(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"**User ID {input_str} adalah** `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"**ID {p.title} adalah** `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**Berikan Username atau Reply ke pesan pengguna**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                "**💬 Message ID:** `{}`\n**🙋‍♂️ From User ID:** `{}`\n**💎 Bot API File ID:** `{}`".format(
                    str(r_msg.id),
                    str(r_msg.sender_id),
                    bot_api_file_id,
                ),
            )

        else:
            await edit_or_reply(
                event,
                "**👥 Chat ID:** `{}`\n**💬 Message ID:** `{}`\n**🙋‍♂️ From User ID:** `{}`".format(
                    str(event.chat_id), str(r_msg.id), str(r_msg.sender_id)
                ),
            )

    else:
        await edit_or_reply(event, f"**👥 Chat ID: **`{event.chat_id}`")


CMD_HELP.update(
    {
        "id": f"**Plugin : **`id`\
        \n\n  •  **Syntax :** `{cmd}id` <username/reply>\
        \n  •  **Function : **Untuk Mengambil Chat ID obrolan saat ini\
        \n\n  •  **Syntax :** `{cmd}userid` <username/reply>\
        \n  •  **Function : **Untuk Mengambil ID & Username obrolan saat ini\
    "
    }
)
