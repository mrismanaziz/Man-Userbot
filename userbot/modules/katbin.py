# Copyright (C) 2021 KenHV
# Recode by @mrismanaziz
# @SharingUserbot

from requests import post
from telethon.tl.types import MessageMediaWebPage

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import man_cmd


@bot.on(man_cmd(outgoing=True, pattern=r"katbin(?:\s|$)([\s\S]*)"))
async def paste(event):
    """Pastes given text to Katb.in"""
    await event.edit("**Processing...**")

    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.media and not isinstance(reply.media, MessageMediaWebPage):
            return await event.edit("**Reply to some text!**")
        message = reply.message

    elif event.pattern_match.group(1).strip():
        message = event.pattern_match.group(1).strip()

    else:
        return await event.edit("**Read** `.help katbin`**.**")

    response = post("https://api.katb.in/api/paste",
                    json={"content": message}).json()

    if response["msg"] == "Successfully created paste":
        await event.edit(
            f"**Pasted successfully:** [Katb.in](https://katb.in/{response['paste_id']})\n"
        )
    else:
        await event.edit("**Sepertinya Katb.in sedang down.**")


CMD_HELP.update(
    {
        "katbin": f"**Plugin : **`katbin`\
        \n\n  •  **Syntax :** `{cmd}katbin`\
        \n  •  **Function : **Paste teks yang diberikan ke web Katb.in\
    "
    }
)
