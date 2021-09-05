import logging

from telethon.utils import pack_bot_file_id

from userbot import CMD_HELP, LOGS
from userbot.events import register
from userbot.utils import edit_delete, edit_or_reply

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

LOGS = logging.getLogger(__name__)


@register(outgoing=True, pattern=r"^\.(get_id|id)(?:\s|$)([\s\S]*)")
async def _(event):
    "To get id of the group or user."
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
                f"**👥 Chat ID : **`{event.chat_id}`\n**🙋‍♂️ From User ID : **`{r_msg.sender_id}`\n**📸 Media File ID: **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                event,
                f"**👥 Chat ID : **`{event.chat_id}`\n**🙋‍♂️ From User ID : **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(event, f"**👥 Chat ID : **`{event.chat_id}`")


CMD_HELP.update(
    {
        "id": "**Plugin : **`id`\
        \n\n  •  **Syntax :** `.id` <username/reply>\
        \n  •  **Function : **Untuk Mengambil Chat ID obrolan saat ini\
        \n\n  •  **Syntax :** `.userid` <username/reply>\
        \n  •  **Function : **Untuk Mengambil ID & Username obrolan saat ini\
    "
    }
)
